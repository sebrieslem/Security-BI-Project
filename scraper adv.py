from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import random

# Setup Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36")

service = Service()
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(120)

# Base URL
base_url = 'https://www.tayara.tn/ads/c/V%C3%A9hicules/?page='

# Collected data
data = []

for page in range(4, 21):
    try:
        driver.get(base_url + str(page))
        time.sleep(random.uniform(2, 4))  # Random delay between pages
    except Exception as e:
        print(f"⏱️ Timeout or error while loading page {page}: {e}")
        continue

    listings = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/item/"]')
    links = [l.get_attribute('href') for l in listings]

    for link in links:
        try:
            driver.get(link)
            time.sleep(random.uniform(2, 4))  # Delay per listing

            # Title
            title = driver.find_element(By.TAG_NAME, 'h1').text

            # Price
            price = driver.find_element(By.TAG_NAME, 'data').text

            # Location
            try:
                location_elements = driver.find_elements(By.CSS_SELECTOR, 'span.text-neutral-500')
                location_time = location_elements[-1].text
                location = location_time.split(',')[0].strip()
            except IndexError:
                location = "N/A"

            # Start record
            car_details = {
                'Title': title,
                'Price': price,
                'Location': location,
                'Link': link
            }

            # Detailed attributes
            detail_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="px-4"][class*="py-2"][class*="bg-gray-100"]')
            for block in detail_blocks:
                try:
                    label = block.find_element(By.CSS_SELECTOR, 'span span:nth-child(1)').text.strip()
                    value = block.find_element(By.CSS_SELECTOR, 'span span:nth-child(2)').text.strip()
                    car_details[label] = value
                except:
                    continue

            data.append(car_details)
            print(f"✅ Scraped: {title}")

        except TimeoutException:
            print(f"⏱️ Timeout while loading listing: {link}")
            continue
        except Exception as e:
            print(f"⚠️ Failed to scrape: {link} — {e}")
            continue

    # ✅ Save after each page
    df = pd.DataFrame(data)
    df.to_csv("tayara_vehicles_partial1.csv", index=False, encoding='utf-8-sig')
    print(f"✅ Page {page} completed and data saved.")

driver.quit()

# Final save (optional duplicate)
df = pd.DataFrame(data)
df.to_csv("tayara_vehicles_detailed.csv", index=False, encoding='utf-8-sig')
print("✅ All data saved to 'tayara_vehicles_detailed.csv'")

