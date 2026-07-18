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
    chrome_options.add_argument('--headless')  # Uruchomienie Chrome w trybie headless (bez interfejsu graficznego)
    chrome_options.add_argument('--no-sandbox') # Wymagane w środowiskach takich jak Google Colab
    chrome_options.add_argument('--disable-dev-shm-usage') # Wymagane w środowiskach takich jak Google Colab
    chrome_options.add_argument('--no-zygote') # Dodatkowa opcja
    chrome_options.add_argument('--disable-setuid-sandbox') # Dodatkowa opcja

    driver = None # Inicjalizacja drivera do None dla bloku finally
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(base_url)
        print(f"Otwarto stronę: {base_url}")
        time.sleep(5) # Zwiększone początkowe opóźnienie na załadowanie strony

        for page_num in range(num_pages):
            print(f"Przetwarzam stronę {page_num + 1}/{num_pages}...")

            # Czekaj, aż dokument będzie w pełni załadowany (readyState == 'complete')
            WebDriverWait(driver, 15).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            time.sleep(2) # Dodatkowe krótkie opóźnienie po załadowaniu dokumentu

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Znajdź wszystkie kontenery ogłoszeń, które mają atrybut onclick z linkiem
            listing_containers = soup.find_all('div', class_='promobox-body-right')

            for div_tag in listing_containers:
                onclick_attr = div_tag.get('onclick')
                if onclick_attr and 'window.location=' in onclick_attr:
                    match = re.search(r"window\.location='(/[^']+)'", onclick_attr) # Podwójne \ dla regex w stringu
                    if match:
                        relative_href = match.group(1)
                        full_link = f"https://www.rzeszowiak.pl{relative_href}"
                        all_links.add(full_link)

            print(f"Zebrano {len(listing_containers)} potencjalnych ogłoszeń ze strony {page_num + 1}. Łącznie unikalnych linków: {len(all_links)}")

            # Spróbuj znaleźć i kliknąć link do następnej strony
            if page_num < num_pages - 1: # Nie próbuj klikać 'Następna', jeśli to ostatnia strona do skrobania
                next_page_text = str(page_num + 2) # Przykładowo: dla page_num=0, next_page_text będzie '2'
                try:
                    # Użyj XPath, aby znaleźć link do następnej strony numerowanej
                    next_page_element_xpath = f"//div[@id='oDnno']//a[text()='{next_page_text}']"
                    next_page_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, next_page_element_xpath))
                    )
                    driver.execute_script("arguments[0].click();", next_page_element) # Użyj JS click dla większej niezawodności
                    print(f"Kliknięto w link do strony: {next_page_text}")
                    time.sleep(3) # Czekaj na załadowanie następnej strony
                except Exception as e:
                    print(f"Nie znaleziono linku do strony '{next_page_text}' lub wystąpił błąd nawigacji: {e}")
                    break # Przerwij, jeśli link do następnej strony nie został znaleziony (koniec stron lub błąd)

    except Exception as e:
        print(f"Wystąpił błąd podczas skrobania stron: {e}")
    finally:
        if driver:
            driver.quit()
            print("Przeglądarka Selenium została zamknięta.")

    return list(all_links)

# Uruchomienie skryptu
if __name__ == "__main__":
    base_url = "https://www.rzeszowiak.pl/Nieruchomosci-Sprzedam-3070011155?r=mieszkania"
    collected_links = scrape_rzeszowiak_links(base_url, num_pages=12) # Ustawione na 12 stron zgodnie z kontekstem

    print(f"Znaleziono łącznie {len(collected_links)} unikalnych linków:")
    for link in collected_links[:10]: # Wyświetl pierwsze 10 linków dla zwięzłości
        print(link)
    if len(collected_links) > 10:
        print(f"... oraz {len(collected_links) - 10} innych linków.")

    # Zapisz linki do pliku
    file_path = '/content/Pobieranie_danych_web_scraping/_3_linki_do_ogloszen.py'
    script_dir = os.path.dirname(file_path)
    output_file = os.path.join(script_dir, 'rzeszowiak_links.txt')

    with open(output_file, 'w') as f:
        for link in collected_links:
            f.write(link + '\n')
    print(f"Link do pliku z zapisanymi linkami: {output_file}")

# Zapisz ten kod do pliku _3_linki_do_ogloszen.py
with open('/content/Pobieranie_danych_web_scraping/_3_linki_do_ogloszen.py', 'w') as f:
    f.write('''
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
            listing_containers = soup.find_all('div', class_='promobox-body-right')
            for div_tag in listing_containers:
                onclick_attr = div_tag.get('onclick')
                if onclick_attr and 'window.location=' in onclick_attr:
                    match = re.search(r"window\\.location='(/[^']+)'", onclick_attr)
                    if match:
                        relative_href = match.group(1)
                        full_link = f"https://www.rzeszowiak.pl{relative_href}"
                        all_links.add(full_link)

            print(f"Zebrano {len(listing_containers)} potencjalnych ogłoszeń ze strony {page_num + 1}. Łącznie unikalnych linków: {len(all_links)}")

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

    file_path = '/content/Pobieranie_danych_web_scraping/_3_linki_do_ogloszen.py'
    script_dir = os.path.dirname(file_path)
    output_file = os.path.join(script_dir, 'rzeszowiak_links.txt')

    with open(output_file, 'w') as f:
        for link in collected_links:
            f.write(link + '\n')
    print(f"Link do pliku z zapisanymi linkami: {output_file}")
''')

print("Plik '_3_linki_do_ogloszen.py' został zaktualizowany.")