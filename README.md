# Security-BI-Project
🔐 Encrypted Car Listings Scraper & Analyzer
A complete data pipeline for securely scraping, storing, and analyzing car listings from Tayara.tn — one of Tunisia’s most popular e-commerce platforms for classified ads.

Developed by Oumayma Abayed and Eslem Sebri
📅 Project Date: May 2025

📌 Project Overview
This project builds a secure, end-to-end workflow:

Scrape vehicle listings from the “Véhicules” section of Tayara.tn.

Clean and structure the extracted data.

Encrypt the dataset to protect sensitive information.

Analyze the data via a simple, user-friendly interface.

The goal was to extract real-time insights from Tunisia’s used car market while respecting data security and responsible scraping practices.

🔧 Tech Stack
Python

Selenium (Web scraping)

Pandas, NumPy (Data cleaning)

cryptography (Data encryption via Fernet)

Tkinter (Graphical User Interface)

🧩 Features
✅ Web Scraper
Scrapes listings from the first 18 pages of Tayara.tn’s car section.

Dynamically loads JavaScript-rendered content using Selenium with a headless browser.

Extracts:

Title

Price

Mileage

Year, Brand, Model

Gearbox, Fuel, Color, State, Engine capacity, Body type

✅ Data Pipeline
Cleans and exports the data to CSV.

Encrypts the dataset using AES-based Fernet encryption.

Secures sensitive information by storing the key in a separate file.

✅ Interface (Tkinter GUI)
User Mode: Filter listings by brand, fuel type, state, color, and gearbox.

Analysis Mode: Visualize:

Price distributions

Average price per brand

Frequency of listings

🛡️ Encryption & Security
Generates a symmetric key (encryption.key) used with Fernet for both encryption and decryption.

Prevents unauthorized access to data while maintaining usability via a secure decryption flow.
