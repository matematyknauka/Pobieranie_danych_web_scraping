import os
project_directory = '/content/Pobieranie_danych_web_scraping'

# 1. Zmień bieżący katalog roboczy na katalog projektu
os.chdir(project_directory)
print(f"Zmieniono katalog roboczy na: {os.getcwd()}")

# 2. Zainstaluj zależności z requirements.txt
!pip install -r requirements.txt

# 3. Dodanie klucza GPG Google Chrome
!wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Dodanie repozytorium Google Chrome
!echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Aktualizacja listy pakietów i instalacja Google Chrome
!apt-get update
!apt-get install -y google-chrome-stable

print("Wszystkie wymagane pakiety i Google Chrome zostały pomyślnie zainstalowane.")