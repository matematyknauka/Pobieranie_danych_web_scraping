import mimetypes
import base64

def prepare_part(file_path):
    """
    Automatycznie przygotowuje obiekt part dla API Gemini.
    Rozpoznaje obrazy i pliki tekstowe/kod.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Obsługa obrazów
    if mime_type and mime_type.startswith("image"):
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return {
            "inline_data": {
                "mime_type": mime_type,
                "data": encoded
            }
        }
    
    # Obsługa plików tekstowych (domyślnie traktowane jako tekst)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"text": f"Plik {file_path} Jego treść {content} Koniec pliku {file_path}"}