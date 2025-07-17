import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from cryptography.fernet import Fernet
import io

class VehicleApp:
    def __init__(self, master):
        self.master = master
        master.title("Vehicle Buyer & Analysis Tool")
        master.geometry("600x500")

        self.data = None

        # Mode selector
        self.mode = tk.StringVar(value="buyer")
        ttk.Label(master, text="Select Mode:").pack(pady=5)
        ttk.Radiobutton(master, text="Buyer Mode", variable=self.mode, value="buyer", command=self.setup_mode).pack()
        ttk.Radiobutton(master, text="Analysis Mode", variable=self.mode, value="analysis", command=self.setup_mode).pack()

        # Load encrypted file
        self.load_button = tk.Button(master, text="Load Encrypted File", command=self.load_encrypted_data)
        self.load_button.pack(pady=10)

        # Frame for mode content
        self.content_frame = tk.Frame(master)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def load_encrypted_data(self):
        file_path = filedialog.askopenfilename(title="Select Encrypted CSV File", filetypes=[("All files", "*.*")])
        if not file_path:
            return

        key = simpledialog.askstring("Decryption Key", "Enter the decryption key:")
        if not key:
            messagebox.showerror("Error", "Decryption key is required.")
            return

        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
            fernet = Fernet(key.encode())
            decrypted = fernet.decrypt(encrypted_data)
            self.data = pd.read_csv(io.StringIO(decrypted.decode('utf-8')))
            self.clean_data()
            messagebox.showinfo("Success", "Data loaded and decrypted successfully!")
            self.setup_mode()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt or load data:\n{e}")

    def clean_data(self):
        df = self.data

        # Price cleaning
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df.loc[df['Price'] > 500000, 'Price'] = None
        df['Price'].fillna("upon request", inplace=True)

        # Year cleaning
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df.loc[(df['Year'] < 1995) | (df['Year'] > 2025), 'Year'] = None

        # Color fill
        df['Color'].fillna('Autre', inplace=True)

        self.data = df

    def setup_mode(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.data is None:
            return

        if self.mode.get() == "buyer":
            self.setup_buyer_mode()
        else:
            self.setup_analysis_mode()

    def setup_buyer_mode(self):
        tk.Label(self.content_frame, text="Filter by features:", font=('Arial', 12, 'bold')).pack(pady=10)

        filters = {}
        options = {
            'State': self.data['State'].dropna().unique(),
            'Color': self.data['Color'].dropna().unique(),
            'Brand': self.data['Brand'].dropna().unique(),
            'Fuel': self.data['Fuel'].dropna().unique(),
            'Gearbox': self.data['Gearbox'].dropna().unique(),
        }

        for col, values in options.items():
            frame = tk.Frame(self.content_frame)
            frame.pack(pady=2)
            tk.Label(frame, text=col).pack(side=tk.LEFT)
            cb = ttk.Combobox(frame, values=sorted(values), state="readonly")
            cb.pack(side=tk.LEFT)
            filters[col] = cb

        def show_results():
            filtered = self.data.copy()
            for col, widget in filters.items():
                val = widget.get()
                if val:
                    filtered = filtered[filtered[col] == val]
            self.show_table(filtered)

        tk.Button(self.content_frame, text="Search", command=show_results).pack(pady=10)

    def setup_analysis_mode(self):
        tk.Button(self.content_frame, text="Show Price Distribution", command=self.plot_price_distribution).pack(pady=5)
        tk.Button(self.content_frame, text="Average Price by Brand", command=self.plot_avg_price_brand).pack(pady=5)
        tk.Button(self.content_frame, text="Offers per Brand", command=self.plot_offers_per_brand).pack(pady=5)

    def plot_price_distribution(self):
        price_data = pd.to_numeric(self.data['Price'], errors='coerce').dropna()
        plt.hist(price_data, bins=30, color='skyblue', edgecolor='black')
        plt.title("Price Distribution")
        plt.xlabel("Price (DT)")
        plt.ylabel("Number of Vehicles")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_avg_price_brand(self):
        df = self.data.copy()
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        avg_price = df.groupby('Brand')['Price'].mean().sort_values(ascending=False).dropna().head(10)
        avg_price.plot(kind='bar', color='orange')
        plt.title('Top 10 Brands by Avg Price')
        plt.xlabel('Brand')
        plt.ylabel('Avg Price')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def plot_offers_per_brand(self):
        offers = self.data['Brand'].value_counts().head(10)
        offers.plot(kind='bar', color='green')
        plt.title('Top 10 Brands by Number of Listings')
        plt.xlabel('Brand')
        plt.ylabel('Number of Vehicles')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def show_table(self, df):
        top = tk.Toplevel(self.master)
        top.title("Filtered Results")

        cols = list(df.columns)
        tree = ttk.Treeview(top, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for _, row in df.iterrows():
            tree.insert('', 'end', values=list(row))
        
        tree.pack(expand=True, fill='both')

# Run the app
root = tk.Tk()
app = VehicleApp(root)
root.mainloop()
