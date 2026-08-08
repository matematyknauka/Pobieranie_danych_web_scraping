from geopy.geocoders import Nominatim

def pobierz_osiedle(ulica, miasto):
    # Inicjalizacja geocodera (wymagany unikalny user_agent)
    geolocator = Nominatim(user_agent="moj_skrypt_geokodowania")
    
    # Przeszukiwanie adresu
    lokalizacja = geolocator.geocode(f"{ulica}, {miasto}", addressdetails=True, language="pl")
    
    if lokalizacja and 'address' in lokalizacja.raw:
        adres = lokalizacja.raw['address']
        
        # Nominatim zwraca różne klucze w zależności od struktury danych (suburb, district, quarter)
        osiedle = adres.get('suburb') or adres.get('district') or adres.get('quarter')
        
        if osiedle:
            return f"Znalezione osiedle/dzielnica: {osiedle}"
        else:
            return "Nie udało się wyodrębnić nazwy osiedla dla tego adresu."
    else:
        return "Nie znaleziono adresu."

# Przykład użycia:
ulica = "Sondeja"
miasto = "Rzeszów"

wynik = pobierz_osiedle(ulica, miasto)
print(wynik)