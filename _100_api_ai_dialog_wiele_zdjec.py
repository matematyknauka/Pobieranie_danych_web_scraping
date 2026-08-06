import base64
import json
import os
import requests
from _101_dane_dla_api_parts import prepare_part 

# Twój klucz API, który działa
api_key = os.environ.get("GEMINI_API_KEY") 
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"
headers = {'Content-Type': 'application/json'}

# Historia dialogu
history = []

parts = []

print("Rozpocznij dialog (wpisz 'koniec' aby wyjść):")

while True:
    user_input = input("\nJa: ")
    if user_input.lower() == 'koniec':
        break
    if user_input.lower() == 'pliki':
        wpisz_plik_input = input("\nPlik: ")
        while not wpisz_plik_input == 'tyle':
              inp_plik = wpisz_plik_input.lower()
              parts.append(prepare_part(inp_plik))
              wpisz_plik_input = input("\nPlik: ")

        continue

    parts.append({"text": user_input})
    """
    # 2. Wczytujemy zdjęcie i kodujemy je do formatu base64
    with open("_8_foto.jpg", "rb") as uchwyt:
         encoded = base64.b64encode(uchwyt.read()).decode("utf-8")
    parts.append(
            {
                    "inline_data": 
                    {
                        "mime_type": "image/jpeg",
                        "data": encoded
                    }
             }
                )
    with open("_2_foto.jpg", "rb") as uchwyt:
         encoded = base64.b64encode(uchwyt.read()).decode("utf-8")

    parts.append(
            {
                    "inline_data": 
                    {
                        "mime_type": "image/jpeg",
                        "data": encoded
                    }
             }
                )

    with open("roboczy.py", 'r', encoding='utf-8') as f:
            content = f.read()

    parts.append({"text": content})
    """
            

    # Dodaj pytanie użytkownika do historii
    history.append({"role": "user", "parts": parts})

    # Wyślij całą historię w polu contents
    data = {"contents": history}

    # Wykonaj zapytanie
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    parts = []

    # Sprawdź odpowiedź[cite: 1]
    if 'candidates' in response_data:
        model_text = response_data['candidates'][0]['content']['parts'][0]['text']
        print(f"Gemini: {model_text}")
        
        # Dodaj odpowiedź modelu do historii, aby pamiętał kontekst[cite: 1]
        history.append({"role": "model", "parts": [{"text": model_text}]})
    else:
        print("\nBłąd API:", response_data) #[cite: 1]