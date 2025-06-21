import requests
import json
import gzip
from io import BytesIO
import os

def get_canli_tv_m3u():
    url = "https://core-api.kablowebtv.com/api/channels"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://tvheryerde.com",
        "Origin": "https://tvheryerde.com",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJMSVZFIiwiaXBiIjoiMCIsImNnZCI6IjA5M2Q3MjBhLTUwMmMtNDFlZC1hODBmLTJiODE2OTg0ZmI5NSIsImNzaCI6IlRSS1NUIiwiZGN0IjoiM0VGNzUiLCJkaSI6ImE2OTliODNmLTgyNmItNGQ5OS05MzYxLWM4YTMxMzIxOGQ0NiIsInNnZCI6Ijg5NzQxZmVjLTFkMzMtNGMwMC1hZmNkLTNmZGFmZTBiNmEyZCIsInNwZ2QiOiIxNTJiZDUzOS02MjIwLTQ0MjctYTkxNS1iZjRiZDA2OGQ3ZTgiLCJpY2giOiIwIiwiaWRtIjoiMCIsImlhIjoiOjpmZmZmOjEwLjAuMC4yMDYiLCJhcHYiOiIxLjAuMCIsImFibiI6IjEwMDAiLCJuYmYiOjE3NDUxNTI4MjUsImV4cCI6MTc0NTE1Mjg4NSwiaWF0IjoxNzQ1MTUyODI1fQ.OSlafRMxef4EjHG5t6TqfAQC7y05IiQjwwgf6yMUS9E"  # Güvenlik için normalde token burada gösterilmemeli
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
            print("❌ API'den geçerli veri alınamadı!")
            return False

        channels = data['Data']['AllChannels']
        print(f"✅ {len(channels)} kanal bulundu")

        existing_lines = []
        existing_names = set()
        if os.path.exists("kablo.m3u"):
            with open("kablo.m3u", "r", encoding="utf-8") as f:
                existing_lines = f.readlines()
                for line in existing_lines:
                    if line.startswith("#EXTINF:") and ',' in line:
                        name = line.split(',')[-1].strip()
                        existing_names.add(name)

        with open("kablo.m3u", "w", encoding="utf-8") as f:
            if not any("#EXTM3U" in line for line in existing_lines):
                f.write("#EXTM3U\n")

            for line in existing_lines:
                f.write(line)

            yeni_kanal_sayisi = 0
            for index, channel in enumerate(channels, start=1):
                name = channel.get('Name')
                stream_data = channel.get('StreamData', {})
                hls_url = stream_data.get('HlsStreamUrl')
                logo = channel.get('PrimaryLogoImageUrl', '')
                categories = channel.get('Categories', [])
                group = categories[0].get('Name', 'Genel') if categories else 'Genel'

                if not name or not hls_url or group == "Bilgilendirme":
                    continue

                if name in existing_names:
                    continue  # Zaten eklenmişse atla

                f.write(f'#EXTINF:-1 tvg-id="{index}" tvg-logo="{logo}" group-title="{group}",{name}\n')
                f.write(f'{hls_url}\n')
                yeni_kanal_sayisi += 1

        print(f"📺 kablo.m3u dosyası güncellendi! (+{yeni_kanal_sayisi} yeni kanal eklendi)")
        return True

    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    get_canli_tv_m3u()
