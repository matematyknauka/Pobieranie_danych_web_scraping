import json
import os
import requests

# Użyj swojego klucza "AQ..."
# Zamiast wklejać klucz jawnie, pobierasz go z ukrytej zmiennej systemowej:
api_key = os.environ.get("GEMINI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"

headers = {"Content-Type": "application/json"}

# Przykładowa treść ogłoszenia, którą pobierasz ze strony
tresc_ogloszenia = (
    "Sprzedam mieszkanie 3-pokojowe, 52m2 na osiedlu Baranówka w Rzeszowie."
)

# Prompt instruujący model, jakich pól oczekujesz
prompt = (
    "Przeanalizuj poniższe ogłoszenie nieruchomości i zwróć dane w formacie JSON "
    "zawierające dokładnie te klucze: 'miejscowosc', 'dzielnica', 'cena_za_m2'.\n\n"
    f"Treść ogłoszenia:\n{tresc_ogloszenia}"
)

data = {
    "contents": [{"parts": [{"text": prompt}]}],
    # Wymuszenie czystego JSON-a na poziomie serwera Google
    "generationConfig": {"responseMimeType": "application/json"},
}

response = requests.post(url, headers=headers, json=data)
odpowiedz_api = response.json()

try:
  # Wyciągamy czysty tekst z odpowiedzi API i zamieniamy go na słownik Pythona
  tekst_json = odpowiedz_api["candidates"][0]["content"]["parts"][0]["text"]
  dane_ogloszenia = json.loads(tekst_json)

  # Dodatkowe zabezpieczenie (filtrowanie kluczy w Pythonie)
  czysty_rekord = {
      "miejscowosc": dane_ogloszenia.get("miejscowosc"),
      "dzielnica": dane_ogloszenia.get("dzielnica"),
      "cena_za_m2": dane_ogloszenia.get("cena_za_m2"),
  }

  print("Sukces! Gotowy słownik do dodania do listy:")
  print(czysty_rekord)
  print(type(czysty_rekord))  # <class 'dict'>

  # Tutaj możesz wrzucić do swojej listy, np.:
  # lista_wynikowa.append(czysty_rekord)

except (KeyError, IndexError, json.JSONDecodeError) as e:
  print(f"Błąd podczas parsowania odpowiedzi AI: {e}")
  print("Surowa odpowiedź:", odpowiedz_api)