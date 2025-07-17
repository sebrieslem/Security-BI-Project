from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Setup Chrome with headless option (remove headless if you want to see it run)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Path to ChromeDriver (you can modify if needed)
service = Service()

driver = webdriver.Chrome(service=service, options=options)

# URL base
base_url = 'https://www.tayara.tn/ads/c/V%C3%A9hicules/?page='

# Data container
data = []

# Loop over 20 pages
for page in range(1, 21):
    driver.get(base_url + str(page))
    time.sleep(2)  # Let the page load

    # Get all listings
    listings = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/item/"]')

    for listing in listings:
        try:
            title = listing.find_element(By.TAG_NAME, 'h2').text
            price = listing.find_element(By.TAG_NAME, 'data').text

            # Get last span with neutral-500 (contains location and time)
            location_time = listing.find_elements(By.CSS_SELECTOR, 'span.text-neutral-500')[-1].text
            location = location_time.split(',')[0].strip()

            # Build full link
            partial_link = listing.get_attribute('href')

            data.append({
                'Title': title,
                'Price': price,
                'Location': location,
                'Link': partial_link
            })
        except Exception as e:
            # Skip any listings that are malformed
            continue

    print(f'✅ Page {page} scraped')

# Close browser
driver.quit()

# Save to CSV
df = pd.DataFrame(data)
df.to_csv('tayara_vehicles.csv', index=False, encoding='utf-8-sig')
print("✅ Scraping completed and data saved to 'tayara_vehicles.csv'")

