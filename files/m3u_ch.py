import requests
import os
from datetime import datetime


M3U_URL = "https://m3u.work/3xvhOsCM.m3u" 
OUTPUT_FILENAME = "playlist.m3u"

def download_m3u():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] M3U dosyasını indiriliyor: {M3U_URL}")
    
    try:
        response = requests.get(M3U_URL, timeout=30)
        response.raise_for_status()
        
        
        with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Başarıyla indirildi ve '{OUTPUT_FILENAME}' olarak kaydedildi.")

    except requests.exceptions.RequestException as e:
        print(f"Hata oluştu: M3U dosyası indirilemedi. Hata: {e}")
        exit(1)

if __name__ == "__main__":
    download_m3u()
  
