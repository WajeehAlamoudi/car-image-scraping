# 🚗 Car Image Scraper 🖼️

This project is a Python-based web scraper designed to download images of Toyota car models from `cars.com`. It leverages Selenium, BeautifulSoup, and requests to navigate the site, locate car listings, and save images locally in a well-organized folder structure.

---

## 📖 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Folder Structure](#folder-structure)
6. [Notes & Tips](#notes--tips)


---

## 🚀 Project Overview

The script scrapes images for various Toyota car models, saving up to 3 images per listing. It organizes the images by model and year, while handling exceptions and continuing the process in case of errors.

### Key Features:
- **Scrapes Toyota car images from cars.com** 🚗
- **Automatically downloads ChromeDriver** with `webdriver_manager`
- **Saves images in structured folders by model and year**
- **Runs in headless mode** (background execution)
- **Auto-resumes numbering** when new images are added later

---

## ⚙️ Prerequisites

Ensure you have the following installed:

- Python 3.8 or newer
- Google Chrome browser (latest version)

---

## 🛠️ Installation

1. Clone or download the code files.
2. Open a terminal in the project directory.
3. Run the following command to install required dependencies:

```bash
pip install -r requirements.txt
```

### `requirements.txt` contents:
```plaintext
selenium
beautifulsoup4
requests
webdriver_manager
```

---

## 🖥️ Usage

To run the scraper, execute:

```bash
python car_image_scraper.py
```

### Script Configuration:

- **Brands:** Currently set to `Toyota`.
- **Car Models:** Includes various Toyota models; you can update the `car_models` list.
- **Years:** 2015 to 2024.
- **Max Pages:** Scrapes up to 10 pages per model and year.

### Expected Output:
- URLs of visited pages.
- Console messages indicating saved images.
- Folders with downloaded images.

---

## 📂 Folder Structure

Images will be saved in the following folder hierarchy:

```
Toyota/
    Sienna/
        2015-2016/
            Sienna_15_1.png
            Sienna_15_2.png
            ...
    Supra/
        2017-2018/
            Supra_17_1.png
            Supra_17_2.png
            ...
```

The folder name uses the format:  
**`{model_name}/{year_period}/{file_name.png}`**

- **File names**: `{model}_{year_last_two_digits}_{image_number}.png`

---

## ⚠️ Notes & Tips

- **Avoid Rapid Requests:** The script uses `time.sleep()` to avoid potential IP bans.
- **Image Count:** The script saves **up to 3 images per car listing**.
- **Year Mapping:** Adjust the `year_mappings` dictionary if needed.
- **Folder Naming:** Modify `folder_mappings` to rename models differently.
- **STORAGE apx 20 free GB is needed for period between 2015-2024**

### Troubleshooting:

- **Images not saved?**  
  Check your internet connection or ensure `cars.com` structure hasn't changed.

- **Driver errors?**  
  Make sure your `webdriver_manager` is updated.

---

## 🛑 Disclaimer

This script is intended for educational purposes only.  
Ensure you comply with `cars.com` terms of service when using this tool.



