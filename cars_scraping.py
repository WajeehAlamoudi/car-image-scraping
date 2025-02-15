import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import glob

# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in the background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Auto-download ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# Get the highest existing file number
def get_last_image_number(folder, prefix):
    existing_files = glob.glob(os.path.join(folder, f"{prefix}_*.png"))
    numbers = []

    for file in existing_files:
        try:
            number = int(file.split("_")[-1].split(".")[0])  # Extract number from filename
            numbers.append(number)
        except ValueError:
            continue  # Ignore if filename is incorrect

    return max(numbers) if numbers else 0  # Return max number or start from 0


# Function to scrape Ford F-150 2015-2016 images (first 3 images per ad)
def scrape(max_pages, brand, car_model, folder_name, year, year_period):
    encoded_model = car_model.lower().replace("-", "_").replace(" ", "_")
    encoded_brand = brand.lower().replace("-", "_").replace(" ", "_")

    save_folder = fr"{brand}\{folder_name}\{year_period}"  # put the year mapp!
    os.makedirs(save_folder, exist_ok=True)

    for page in range(1, max_pages + 1):
        search_url = f"https://www.cars.com/shopping/results/?dealer_id=&include_shippable=false&keyword=&list_price_max=&list_price_min=&makes[]={encoded_brand}&maximum_distance=all&mileage_max=&models[]={encoded_brand}-{encoded_model}&monthly_payment=&page={page}&page_size=100&sort=best_match_desc&stock_type=all&year_max={year}&year_min={year}&zip="
        print(search_url)

        try:
            driver.get(search_url)
            time.sleep(5)  # Wait for page to load

            print(f"📄 Scraping Page {page} for {car_model} ({year_period})...")

            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find all car listings
            listings = soup.find_all("div", class_="vehicle-card")

            if not listings:  # ✅ If no listings exist, stop and move to the next model/year
                print(f"⚠ No listings found on page {page}. Skipping to next model/year.")
                break  # Exit loop and move to the next model/year

            # Scroll down to load images
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)

            for listing in listings:
                try:
                    # Extract all available images in the listing
                    img_elements = listing.find_all("img")  # Get all images
                    img_urls = [img["src"] for img in img_elements if "src" in img.attrs]  # Extract URLs
                    m = year[-2:]  # Extracts last two

                    prefix = f"{folder_name}_{m}"
                    # Get the last image number and continue
                    image_count = get_last_image_number(save_folder, prefix) + 1

                    # Save only the first two images
                    for i, img_url in enumerate(img_urls[:3]):  # First 3 images only
                        img_filename = os.path.join(save_folder, f"{folder_name}_{m}_{image_count}.png")
                        img_data = requests.get(img_url).content
                        with open(img_filename, "wb") as img_file:
                            img_file.write(img_data)
                        print(f"Saved: {img_filename}")
                        image_count += 1  # Increment image counter

                except Exception as e:
                    print(f"Error processing listing: {e}")

        except Exception as e:
            print(f"⚠ Error loading page {page}: {e}. Skipping to next model/year.")
            break  # Stop checking more pages for this model/year


brands = ['Toyota']
"""
    '4Runner', '86', 'Avalon Hybrid', 'Avalon', 'bZ4X', 'C-HR', 'Camry', 'Camry Hybrid', 'Camry Solara',
    'Corolla iM', 'Corolla Hybrid', 'Corolla Hatchback', 'Corolla Cross Hybrid', 'Corolla Cross', 'Corolla',
    'Crown', 'Crown Signia', 'FJ Cruiser', 'GR86', 'GR Corolla', 'GR Supra', 'Highlander Hybrid', 'Highlander',
    'Grand Highlander Hybrid', 'Grand Highlander', 'Land Cruiser', 'Prius v', 'Prius Prime', 'Prius Plug-In Hybrid',
    'Prius Plug-in', 'Prius c', 'Prius', 'RAV4 Prime', 'RAV4 Plug-In Hybrid', 'RAV4 Hybrid', 'RAV4 EV', 'RAV4',
    'Sequoia',
"""
car_models = [

    'Sienna', 'Supra', 'Tacoma Hybrid', 'Tacoma', 'Tundra Hybrid', 'Tundra', 'Venza', 'Yaris Sedan',
    'Yaris iA', 'Yaris'
]

folder_mappings = {
    '4Runner': '4Runner',

    '86': '86',

    'Avalon Hybrid': 'Avalon',
    'Avalon': 'Avalon',

    'bZ4X': 'bZ4X',

    'C-HR': 'C-HR',

    'Camry': 'Camry',
    'Camry Hybrid': 'Camry',
    'Camry Solara': 'Camry',

    'Corolla iM': 'Corolla',
    'Corolla Hybrid': 'Corolla',
    'Corolla Hatchback': 'Corolla',
    'Corolla Cross Hybrid': 'Corolla',
    'Corolla Cross': 'Corolla',
    'Corolla': 'Corolla',

    'Crown': 'Crown',
    'Crown Signia': 'Crown',

    'FJ Cruiser': 'FJ',

    'GR86': 'GR',
    'GR Corolla': 'GR',
    'GR Supra': 'GR',

    'Highlander Hybrid': 'Highlander',
    'Highlander': 'Highlander',
    'Grand Highlander Hybrid': 'Highlander',
    'Grand Highlander': 'Highlander',

    'Land Cruiser': 'Land Cruiser',

    'Prius v': 'Prius',
    'Prius Prime': 'Prius',
    'Prius Plug-In Hybrid': 'Prius',
    'Prius Plug-in': 'Prius',
    'Prius c': 'Prius',
    'Prius': 'Prius',

    'RAV4 Prime': 'RAV4',
    'RAV4 Plug-In Hybrid': 'RAV4',
    'RAV4 Hybrid': 'RAV4',
    'RAV4 EV': 'RAV4',
    'RAV4': 'RAV4',

    'Sequoia': 'Sequoia',

    'Sienna': 'Sienna',

    'Supra': 'Supra',

    'Tacoma Hybrid': 'Tacoma',
    'Tacoma': 'Tacoma',

    'Tundra Hybrid': 'Tundra',
    'Tundra': 'Tundra',

    'Venza': 'Venza',

    'Yaris Sedan': 'Yaris',
    'Yaris iA': 'Yaris',
    'Yaris': 'Yaris'
}

year_mappings = {
    '2015': '2015-2016',
    '2016': '2015-2016',

    '2017': '2017-2018',
    '2018': '2017-2018',

    '2019': '2019-2020',
    '2020': '2019-2020',

    '2021': '2021-2022',
    '2022': '2021-2022',

    '2023': '2023-2024',
    '2024': '2023-2024'
}

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

for brand in brands:
    for car_model in car_models:
        folder_name = folder_mappings[car_model]
        for year in years:
            year = str(year)
            year_period = year_mappings[year]
            # Run scraper
            scrape(max_pages=10, brand=brand, car_model=car_model, folder_name=folder_name,
                   year=year, year_period=year_period)

# Close WebDriver
driver.quit()

# 21models × 5year periods = 105classes
