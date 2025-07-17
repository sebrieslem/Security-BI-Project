# 🔐 Encrypted Car Listings Scraper & Analyzer

A complete data pipeline for securely scraping, storing, and analyzing car listings from [Tayara.tn](https://www.tayara.tn) — one of Tunisia’s most popular e-commerce platforms for classified ads.

Developed by **Oumayma Abayed** and **Eslem Sebri**  
📅 Project Date: May 2025

---

## 📌 Project Overview

This project builds a secure, end-to-end workflow:

1. **Scrape** vehicle listings from the “Véhicules” section of Tayara.tn.  
2. **Clean** and structure the extracted data.  
3. **Encrypt** the dataset to protect sensitive information.  
4. **Analyze** the data via a user-friendly interface.

The goal was to extract real-time insights from Tunisia’s used car market while maintaining security and ethical scraping practices.

---

## 🔧 Tech Stack

- **Python**
  - `Selenium` — Web scraping
  - `Pandas`, `NumPy` — Data cleaning & structuring
  - `cryptography` — AES-based Fernet encryption
  - `Tkinter` — Desktop GUI interface

---

## 🧩 Features

### ✅ Web Scraper

- Targets the first 18 pages of Tayara.tn's “Véhicules” section.
- Loads JavaScript-rendered content with Selenium (headless Chrome).
- Extracts:
  - Title
  - Price
  - Mileage
  - Brand, Model, Year
  - Gearbox, Fuel, Color, State
  - Engine capacity, Body type
  - URL link to listing

### ✅ Data Pipeline

- Clean and structure the raw data using Pandas.
- Export to CSV for accessibility.
- Encrypt CSV using Fernet (AES-based symmetric encryption).

### ✅ GUI Interface (Tkinter)

Two modes available:

- **User Mode**:  
  - Filter listings by brand, fuel, state, color, and gearbox.

- **Analysis Mode**:  
  - Visualize:
    - Price distributions
    - Average price per brand
    - Listing frequency over time

---

## 🛡️ Encryption & Security

- Uses a generated Fernet key (`encryption.key`) for all encryption/decryption.
- Data is encrypted before storage and can only be decrypted via the interface using the correct key.
- Ensures privacy and prevents unauthorized access.

---

## 📁 Project Structure

```text
.
├── scraper/
│   └── tayara_scraper.py
├── data/
│   ├── tayara_vehicles_cleaned.csv
│   └── tayara_vehicles_cleaned_encrypted.csv
├── encryption/
│   ├── encrypt.py
│   ├── decrypt.py
│   └── encryption.key
├── interface/
│   └── gui_app.py
├── requirements.txt
└── README.md
