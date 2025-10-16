import time
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Remove if you want to see browser UI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Create driver
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Storage for all scraped data
all_data = []

# Loop through first 3 pages
for page_number in range(1, 11):
    url = f"https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults/EntityName/aaa/Page{page_number}?searchNameOrder=AAA"
    driver.get(url)

    time.sleep(3)  # Allow page to fully load (can be replaced with WebDriverWait)

    rows = driver.find_elements(By.XPATH, '//h2[contains(text(),"Entity Name List")]/parent::div//table/tbody/tr')

    for row in rows:
        try:
            name_element = row.find_element(By.XPATH, './td[1]/a')
            document_number = row.find_element(By.XPATH, './td[2]').text.strip()
            status = row.find_element(By.XPATH, './td[3]').text.strip()

            company_name = name_element.text.strip()
            company_url = name_element.get_attribute("href")

            all_data.append({
                "Company Name": company_name,
                "Document Number": document_number,
                "Status": status,
                "URL": company_url
            })
        except Exception as e:
            print(f"Skipping row due to error on page {page_number}: {e}")

# Close the driver
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(all_data)
print(df)

# Optional: Save to CSV
try:
    df.to_csv("sunbiz_data_page1_10.csv", index=False)
    print("✅ CSV saved successfully!")
except Exception as e:
    print("❌ Error saving CSV:", e)

import os
print("Saving CSV to:", os.getcwd())