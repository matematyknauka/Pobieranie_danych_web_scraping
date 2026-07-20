import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import os

def scrape_rzeszowiak_links(base_url, num_pages=12):
    all_links = set()

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-zygote')
    chrome_options.add_argument('--disable-setuid-sandbox')

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(base_url)
        print(f"Otwarto stronę: {base_url}")
        time.sleep(5)

        for page_num in range(num_pages):
            print(f"Przetwarzam stronę {page_num + 1}/{num_pages}...")
            WebDriverWait(driver, 15).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            current_page_links_count = 0

            # --- Ekstrakcja linków z ogłoszeń promowanych (promobox-body-right) ---
            promoted_listing_containers = soup.find_all('div', class_='promobox-body-right')
            for div_tag in promoted_listing_containers:
                onclick_attr = div_tag.get('onclick')
                if onclick_attr and 'window.location=' in onclick_attr:
                    match = re.search(r"window\.location='(/[^']+)'", onclick_attr)
                    if match:
                        relative_href = match.group(1)
                        full_link = f"https://www.rzeszowiak.pl{relative_href}"
                        all_links.add(full_link)
                        current_page_links_count += 1

            # --- Ekstrakcja linków z ogłoszeń niepromowanych (normalbox) ---
            normal_listing_containers = soup.find_all('div', class_='normalbox')
            for ogloszenie_normalne in normal_listing_containers:
                # Link znajduje się w div.normalbox-title-left > a
                link_container = ogloszenie_normalne.find('div', class_='normalbox-title-left')
                if link_container:
                    link_tag = link_container.find('a', href=True)
                    if link_tag:
                        relative_href = link_tag['href']
                        full_link = f"https://www.rzeszowiak.pl{relative_href}"
                        all_links.add(full_link)
                        current_page_links_count += 1

            print(f"Zebrano {current_page_links_count} potencjalnych ogłoszeń ze strony {page_num + 1}. Łącznie unikalnych linków: {len(all_links)}")

            if page_num < num_pages - 1:
                next_page_text = str(page_num + 2)
                try:
                    next_page_element_xpath = f"//div[@id='oDnno']//a[text()='{next_page_text}']"
                    next_page_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, next_page_element_xpath))
                    )
                    driver.execute_script("arguments[0].click();", next_page_element)
                    print(f"Kliknięto w link do strony: {next_page_text}")
                    time.sleep(3)
                except Exception as e:
                    print(f"Nie znaleziono linku do strony '{next_page_text}' lub wystąpił błąd nawigacji: {e}")
                    break

    except Exception as e:
        print(f"Wystąpił błąd podczas skrobania stron: {e}")
    finally:
        if driver:
            driver.quit()
            print("Przeglądarka Selenium została zamknięta.")

    return list(all_links)

if __name__ == "__main__":
    base_url = "https://www.rzeszowiak.pl/Nieruchomosci-Sprzedam-3070011155?r=mieszkania"
    collected_links = scrape_rzeszowiak_links(base_url, num_pages=12)

    print(f"Znaleziono łącznie {len(collected_links)} unikalnych linków:")
    for link in collected_links[:10]:
        print(link)
    if len(collected_links) > 10:
        print(f"... oraz {len(collected_links) - 10} innych linków.")

    file_path = '/content/Pobieranie_danych_web_scraping/_3_linki_do_ogloszen.py' # Zakładamy, że ten plik istnieje
    script_dir = os.path.dirname(file_path)
    output_file = os.path.join(script_dir, 'rzeszowiak_links.txt')

    with open(output_file, 'w') as f:
        for link in collected_links:
            f.write(link + '\n')
    print(f"Link do pliku z zapisanymi linkami: {output_file}")
