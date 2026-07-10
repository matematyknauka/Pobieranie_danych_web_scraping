import time
import requests
from bs4 import BeautifulSoup

# Adres URL strony z ogłoszeniami mieszkań
url = "https://www.rzeszowiak.pl/Nieruchomosci-Sprzedam-3070011155?r=mieszkania"

# Definiujemy nagłówek User-Agent, aby nasza zapytanie wyglądało jak z przeglądarki internetowej
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Pobieranie danych ze strony...")

try:
    # Wysyłamy zapytanie GET do serwera
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Rzuci błąd w przypadku problemów z połączeniem (np. 404 lub 500)
    
    # Wymuszamy poprawne kodowanie znaków, ponieważ rzeszowiak.pl używa specyficznego kodowania (często ISO-8859-2 lub Windows-1250)
    response.encoding = response.apparent_encoding

    # Parsujemy pobraną treść HTML za pomocą BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Na portalu rzeszowiak.pl ogłoszenia są często elementami tekstowymi, 
    # w których cena oznaczona jest bezpośrednio tekstem "cena:"
    # Szukamy wszystkich elementów tekstowych/kontenerów zawierających słowo "cena:"
    promoted_and_regular_ads = soup.find_all(text=lambda text: text and "cena:" in text.lower())

    if not promoted_and_regular_ads:
        print("Nie znaleziono ogłoszeń. Struktura strony mogła ulec zmianie.")
    else:
        print(f"Znaleziono potencjalnych ogłoszeń: {len(promoted_and_regular_ads)}\n")

    # Przechodzimy pętlą przez znalezione elementy z cenami
    for i, ad_text in enumerate(promoted_and_regular_ads, start=1):
        # Pobieramy rodzica elementu tekstowego, aby wyciągnąć pełny kontekst ogłoszenia
        parent_element = ad_text.parent
        
        # Wyciągamy linijkę z ceną i oczyszczamy ją ze zbędnych białych znaków
        cena_raw = ad_text.strip()
        
        # Pobieramy opis ogłoszenia. Zazwyczaj na rzeszowiaku opis znajduje się w kolejnym elemencie 
        # lub bezpośrednio pod linią z ceną w tym samym bloku.
        # Pobieramy tekst z otoczenia elementu i usuwamy z niego powtórzoną linię ceny, aby uzyskać czysty opis.
        pelny_tekst_bloku = parent_element.get_text(separator="\n").strip()
        opis = pelny_tekst_bloku.replace(cena_raw, "").strip()
        
        # Skracamy wyświetlanie opisu w konsoli, jeśli jest bardzo długi
        krotki_opis = opis[:150].replace('\n', ' ') + "..." if len(opis) > 150 else opis
        
        # Wyświetlamy sformatowane wyniki
        print(f"--- Ogłoszenie nr {i} ---")
        print(f"Cena: {cena_raw}")
        print(f"Opis: {krotki_opis}")
        print("-" * 30)

        # Dodajemy opóźnienie (np. 1 sekunda) między przetwarzaniem kolejnych elementów,
        # aby nie wysyłać lawiny zapytań w pętli i zachować tzw. "dobrą praktykę scrapingu"
        # (W przypadku przetwarzania jednej strony opóźnienie wewnątrz pętli jest opcjonalne, 
        # ale kluczowe, jeśli w przyszłości dodasz przechodzenie między stronami 1, 2, 3...)
        time.sleep(1.0)

except requests.exceptions.RequestException as e:
    print(f"Wystąpił błąd podczas pobierania strony: {e}")

print("\nZakończono działanie skryptu.")

