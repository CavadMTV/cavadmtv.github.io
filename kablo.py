import requests
import json
import gzip
from io import BytesIO

def add_proxy_to_url(url, proxy_base_url):
    """
    Bir URL'ye proxy adresini ekler.
    
    Args:
        url (str): Proxy'siz orijinal URL.
        proxy_base_url (str): Proxy adresinin temel URL'si (örneğin, "http://proxy.com/proxy?url=").
    
    Returns:
        str: Proxy eklenmiş yeni URL.
    """
    
    if not proxy_base_url.endswith('url='):
        if proxy_base_url.endswith('?'):
            proxy_base_url += 'url='
        else:
            proxy_base_url += '?url='
    return f"{proxy_base_url}{url}"

def get_canli_tv_m3u(proxy_url):
    """
    CanliTV API'sinden M3U listesini alır ve proxy adresini ekler.
    
    Args:
        proxy_url (str): Kullanılacak proxy adresinin temel URL'si.
    
    Returns:
        bool: İşlem başarılıysa True, aksi takdirde False.
    """
    
    url = "https://core-api.kablowebtv.com/api/channels"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJMSVZFIiwiaXBiIjoiMCIsImNnZCI6IjA5M2Q3MjBhLTUwMmMtNDFlZC1hODBmLTJiODE2OTg0ZmI5NSIsImNzaCI6IlRSS1NUIiwiZGN0IjoiM0VGNzUiLCJkaSI6ImE2OTliODNmLTgyNmItNGQ5OS05MzYxLWM4YTMxMzIxOGQ0NiIsInNnZCI6Ijg5NzQxZmVjLTFkMzMtNGMwMC1hZmNkLTNmZGFmZTBiNmEyZCIsInNwZ2QiOiIxNTJiZDUzOS02MjIwLTQ0MjctYTkxNS1iZjRiZDA2OGQ3ZTgiLCJpYyI6IjAiLCJpZG0iOiIwIiwiaWEiOiI6OmZmZmY6MTAuMC4wLjIwNiIsImFwdiI6IjEuMC4wIiwiYWJuIjoiMTAwMCIsIm5iZiI6MTc0NTE1MjgyNSwiZXhwIjoxNzQ1MTUyODg1LCJpYXQiOjE3NDUxNTI4MjV9.OSlafRMxef4EjHG5t6TqfAQC7y05IiQjwwgf6yMUS9E"  # Güvenlik için normalde token burada gösterilmemeli
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
                
                # Proxy adresini URL'ye ekle
                proxied_hls_url = add_proxy_to_url(hls_url, proxy_url)

                f.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f'{proxied_hls_url}\n')

                kanal_sayisi += 1
                kanal_index += 1  
            
            print(f"📺 kablo1.m3u dosyası oluşturuldu! ({kanal_sayisi} kanal)")
            return True
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    PROXY_URL = "http://live.artofknot.com:5080/proxy/channel?url="  
    get_canli_tv_m3u(PROXY_URL)
