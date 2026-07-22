import re
import requests
from bs4 import BeautifulSoup


def pobierz_tresc_ogloszenia(url):


    # Nagłówki, które udają prawdziwą przeglądarkę (zapobiegają blokowaniu przez serwer)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0                Safari/537.36"
    }
    
    try:
        # Wysłanie żądania GET do serwera
        response = requests.get(url, headers=headers)
        
        # Sprawdzenie, czy żądanie zakończyło się sukcesem (kod 200)
        if response.status_code == 200:
            # Wymuszenie poprawnego kodowania znaków (przydatne dla polskich liter)
            response.encoding = response.apparent_encoding
            
            html_content = response.text
            # Sparsowanie HTML za pomocą BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")
            
            
    
            # Zakładając, że masz już sparsowany obiekt 'soup'
            # Znajdujemy kontener, który zawiera nagłówek "Treść ogłoszenia"
            # Następnym elementem po nagłówku jest interesujący nas div
            content_box = soup.find('div', class_='ogloszeniebox-top', string=lambda text: text and 'Treść ogłoszenia' in text)
            target_div = content_box.find_next_sibling('div', class_='ogloszeniebox-content').find('div', class_='content')

    
            # Pobieramy czysty tekst
            # separator='\n' zapewnia czytelność, a strip=True usuwa zbędne białe znaki
            czysta_tresc = target_div.get_text(separator='\n', strip=True)



            # !!!!!!!!!!!!!!!!!!!!!Dodac komentarze!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!!
            tytulowy = soup.find('div', class_='ogloszeniebox-top', string=lambda text: text and 'Dane dodatkowe' in text)
            wiersz_1 = tytulowy.find_next_sibling('div', class_='ogloszeniebox-content')
            wiersz_1_text = wiersz_1.get_text(separator='\n', strip=True)

            wiersz_2 = wiersz_1.find_next_sibling('div', class_='ogloszeniebox-content')
            wiersz_2_text = wiersz_2.get_text(separator='\n', strip=True)

            wiersz_3 = wiersz_2.find_next_sibling('div', class_='ogloszeniebox-content')
            wiersz_3_text = wiersz_3.get_text(separator='\n', strip=True)

            wiersz_4 = wiersz_3.find_next_sibling('div', class_='ogloszeniebox-content')
            wiersz_4_text = wiersz_4.get_text(separator='\n', strip=True)

            dane_dodatkowe = f"{wiersz_1_text}\n{wiersz_2_text}\n{wiersz_3_text}\n{wiersz_4_text}"

            
    
            return f"Tresc:\n\n{czysta_tresc}\n\nDane dodatkowe\n\n{dane_dodatkowe}"
            # return czysta_tresc
    
            
        else:
            print(f"Błąd! Serwer zwrócił kod statusu: {response.status_code}")
            
    except Exception as e:
             print(f"Wystąpił błąd podczas próby połączenia: {e}")





