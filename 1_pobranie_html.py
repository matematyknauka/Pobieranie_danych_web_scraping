import requests

# URL strony do pobrania
url = "https://www.rzeszowiak.pl/Nieruchomosci-Sprzedam-3070011155?r=mieszkania"

# Nagłówki, które udają prawdziwą przeglądarkę (zapobiegają blokowaniu przez serwer)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # Wysłanie żądania GET do serwera
    response = requests.get(url, headers=headers)
    
    # Sprawdzenie, czy żądanie zakończyło się sukcesem (kod 200)
    if response.status_code == 200:
        # Wymuszenie poprawnego kodowania znaków (przydatne dla polskich liter)
        response.encoding = response.apparent_encoding
        
        html_content = response.text
        
    else:
        print(f"Błąd! Serwer zwrócił kod statusu: {response.status_code}")

except Exception as e:
    print(f"Wystąpił błąd podczas próby połączenia: {e}")

