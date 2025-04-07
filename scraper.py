import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

def get_assessment_links(driver):
    url = "https://www.shl.com/solutions/products/product-catalog/"
    driver.get(url)

    try:
        # Wait until the product tiles (assessments) are visible
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "shl-card"))
        )
        print("✅ Assessment cards loaded")

        # Find all <a> tags inside those tiles
        cards = driver.find_elements(By.CLASS_NAME, "shl-card")
        links = []

        for card in cards:
            try:
                a_tag = card.find_element(By.TAG_NAME, "a")
                link = a_tag.get_attribute("href")
                if link and "/en/assessments/" in link:
                    links.append(link)
            except:
                continue

        unique_links = list(set(links))
        print(f"🔗 Found {len(unique_links)} assessment links")
        return unique_links

    except Exception as e:
        print("❌ Failed to find assessment cards:", str(e))
        return []


def parse_assessment_page(url):
    print(f"Scraping: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    name = soup.find("h1").text.strip() if soup.find("h1") else "N/A"
    description_tag = soup.find("div", class_="c-product-detail__content")
    description = description_tag.get_text(strip=True) if description_tag else "N/A"
    
    detail_fields = soup.select("li.c-product-detail__fact")
    
    test_type = duration = remote = adaptive = "N/A"
    
    for field in detail_fields:
        label = field.select_one("strong")
        if label:
            label_text = label.text.strip().lower()
            value = field.text.replace(label.text, "").strip()
            
            if "test type" in label_text:
                test_type = value
            elif "duration" in label_text:
                duration = value
            elif "remote" in label_text:
                remote = value
            elif "adaptive" in label_text:
                adaptive = value

    return {
        "Assessment Name": name,
        "URL": url,
        "Description": description,
        "Test Type": test_type,
        "Duration": duration,
        "Remote Testing Support": remote,
        "Adaptive Support": adaptive
    }
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # 👈 Add this line
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    chrome_path = os.path.join(os.getcwd(), "chromedriver.exe")
    service = Service(executable_path=chrome_path)

    driver = webdriver.Chrome(service=service, options=options)
    return driver
def scrape_catalog():
    scraped_data = []
    driver = get_driver()
    links = get_assessment_links(driver)

    for link in links:
        try:
            data = parse_assessment_page(driver, link)
            scraped_data.append(data)
        except Exception as e:
            print(f"❌ Error scraping {link}: {e}")
            continue

    driver.quit()
    return scraped_data


if __name__ == "__main__":
    scraped_data = scrape_catalog()
    new_df = pd.DataFrame(scraped_data)

    try:
        existing_df = pd.read_csv("shl_data.csv")
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=["Assessment Name", "URL"])
        print(f"🧩 Existing rows: {len(existing_df)} | Scraped new rows: {len(new_df)}")
    except FileNotFoundError:
        print("🔔 Existing dataset not found. Creating new one...")
        combined_df = new_df

    combined_df.to_csv("shl_data.csv", index=False)
    print(f"✅ Final dataset saved with {len(combined_df)} total assessments.")
