import requests
import json
import gzip
from io import BytesIO
import re # <-- Bu satırı ekliyoruz

def get_canli_tv_m3u():
    """"""
    
    url = "https://core-api.kablowebtv.com/api/channels"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJMSVZFIiwiaXBiIjoiMCIsImNnZCI6IjA5M2Q3MjBhLTUwMmMtNDFlZC1hODBmLTJiODE2OTg0ZmI5NSIsImNzaCI6IlRSS1NUIiwiZGN0IjoiM0VGNzUiLCJkaSI6ImE2OTliODNmLTgyNmItNGQ5OS05MzYxLWM4YTMxMzIxOGQ0NiIsInNnZCI6Ijg5NzQxZmVjLTFkMzMtNGMwMC1hZmNkLTNmZGFmZTBiNmEyZCIsInNwZ2QiOiIxNTJiZDUzOS02MjIwLTQ0MjctYTkxNS1iZjRiZDA2OGQ3ZTgiLCJpY2giOiIwIiwiaWRtIjoiMCIsImlhIjoiOjpmZmZmOjEwLjAuMC4yMDYiLCJhcHYiOiIxLjAuMCIsImFibiI6IjEwMDAiLCJuYmYiOjE3NDUxNTI4MjUsImV4cCI6MTc0NTE1Mjg4NSwiaWF0IjoxNzQ1MTUyODI1fQ.OSlafRMxef4EjHG5t6TqfAQC7y05IiQjwwgf6yMUS9E" # Güvenlik için normalde token burada gösterilmemeli
    }
    
    try:
        print("📡 CanliTV API'den veri alınıyor...")
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        try:
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz:
                content = gz.read().decode('utf-8')
        except:
            content = response.content.decode('utf-8')
        
        data = json.loads(content)
        
        if not data.get('IsSucceeded') or not data.get('Data', {}).get('AllChannels'):
            print("❌ CanliTV API'den geçerli veri alınamadı!")
            return False
        
        channels = data['Data']['AllChannels']
        print(f"✅ {len(channels)} kanal bulundu")
        
        with open("kablo1.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            kanal_sayisi = 0
            kanal_index = 1  
            
            for channel in channels:
                name = channel.get('Name')
                stream_data = channel.get('StreamData', {})
                hls_url = stream_data.get('HlsStreamUrl') if stream_data else None
                logo = channel.get('PrimaryLogoImageUrl', '')
                categories = channel.get('Categories', [])
                
                if not name or not hls_url:
                    continue
                
                group = categories[0].get('Name', 'Genel') if categories else 'Genel'
                
                if group == "Bilgilendirme":
                    continue

                tvg_id = str(kanal_index)

                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f'{hls_url}\n')

                kanal_sayisi += 1
                kanal_index += 1  
        
        print(f"📺 kablo1.m3u dosyası oluşturuldu! ({kanal_sayisi} kanal)")

        # --- YENİ EKLENECEK KOD BURADAN BAŞLIYOR ---
        m3u_baglantilarini_guncelle("kablo1.m3u")
        # --- YENİ EKLENECEK KOD BURADA BİTİYOR ---
        
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

# --- YENİ EKLENECEK KOD BURADAN BAŞLIYOR ---
def m3u_baglantilarini_guncelle(dosya_yolu="kablo1.m3u"):
    """
    kablo1.m3u dosyasını okur, .m3u8 bağlantılarının başına proxy URL'sini ekler
    ve güncellenmiş içeriği dosyaya geri yazar.
    """
    proxy_oneki = "http://live.artofknot.com:5080/proxy/channel?url="
    guncellenmis_satirlar = []

    try:
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            for satir in f:
                # Satırda bir .m3u8 bağlantısı olup olmadığını kontrol edin
                # ve henüz proxy önekiyle başlamadığından emin olun
                if ".m3u8" in satir and not satir.strip().startswith(proxy_oneki):
                    # URL'yi bulmak ve proxy'yi başına eklemek için regex kullanın
                    eslesme = re.search(r'(https?://[^\s]+\.m3u8[^\s]*)', satir)
                    if eslesme:
                        orijinal_url = eslesme.group(1)
                        # Orijinal URL'yi proxyli URL ile değiştirin
                        satir = satir.replace(orijinal_url, proxy_oneki + orijinal_url)
                guncellenmis_satirlar.append(satir)

        with open(dosya_yolu, 'w', encoding='utf-8') as f:
            f.writelines(guncellenmis_satirlar)

        print(f"🔗 {dosya_yolu} içindeki .m3u8 bağlantıları proxy önekiyle güncellendi.")

    except FileNotFoundError:
        print(f"❗ Hata: {dosya_yolu} bulunamadı, bağlantılar güncellenemedi.")
    except Exception as e:
        print(f"⁉️ Bağlantıları güncellerken bir hata oluştu: {e}")
# --- YENİ EKLENECEK KOD BURADA BİTİYOR ---

if __name__ == "__main__":
    get_canli_tv_m3u()
