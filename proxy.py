import re
import os

def proxy_m3u_list_with_param(input_m3u_file, output_m3u_file, proxy_base_url):
  """
  Bir M3U dosyasındaki tüm M3U8 yayın URL'lerine, 'url=' parametresi ile proxy başlığı ekler.

  Args:
    input_m3u_file (str): Proxy uygulanacak M3U dosyasının yolu.
    output_m3u_file (str): Proxy uygulanmış yeni M3U dosyasının kaydedileceği yol.
    proxy_base_url (str): Proxy'nin temel URL'si (örneğin "http://live.artofknot.com:5080/proxy/channel?url=").
  """
  
  # Proxy URL'sinin sonunda 'url=' olup olmadığını kontrol et.
  # Eğer yoksa ve eklenmesi gerekiyorsa ekle.
  if not proxy_base_url.endswith('url='):
    # Eğer sonunda sadece '?' varsa, 'url=' ekle.
    if proxy_base_url.endswith('?'):
        proxy_base_url += 'url='
    else: # Ne 'url=' ne de '?' varsa, '?url=' ekle.
        proxy_base_url += '?url='


  proxied_lines = []
  try:
    with open(input_m3u_file, 'r', encoding='utf-8') as f:
      for line in f:
        # http:// veya https:// ile başlayıp .m3u8 ile biten URL'leri yakalarız.
        match = re.search(r'(https?://[^\s]+\.m3u8)', line)
        
        if match:
          original_url = match.group(1)
          # Zaten bu proxy_base_url ile proxy'lenmiş mi kontrol et.
          # Bu kontrol, gereksiz proxy eklemeyi engeller.
          if not original_url.startswith(proxy_base_url):
            proxied_url = f"{proxy_base_url}{original_url}"
            # Orijinal satırdaki URL'yi proxy'li URL ile değiştir
            new_line = line.replace(original_url, proxied_url)
            proxied_lines.append(new_line)
          else:
            proxied_lines.append(line) # Zaten proxy'liyse olduğu gibi ekle
        else:
          proxied_lines.append(line) # URL içermeyen veya m3u8 olmayan satırları olduğu gibi ekle

    with open(output_m3u_file, 'w', encoding='utf-8') as f:
      f.writelines(proxied_lines)

    print(f"'{input_m3u_file}' dosyasındaki M3U8 URL'lerine proxy uygulandı ve '{output_m3u_file}' olarak kaydedildi.")

  except FileNotFoundError:
    print(f"Hata: '{input_m3u_file}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
  except Exception as e:
    print(f"Bir hata oluştu: {e}")

# --- Örnek Kullanım ---
# Adım 1: Test için örnek bir M3U dosyası oluşturalım.
# Gerçek uygulamanızda bu kısmı kendi M3U dosyanızla değiştireceksiniz.
sample_m3u_content = """#EXTM3U
#EXTINF:-1 tvg-id="Kanal1" tvg-name="Kanal 1",Kanal 1
http://cdn.zerocdn.com/cdn.m3u8
#EXTINF:-1 tvg-id="Kanal2" tvg-name="Kanal 2",Kanal 2
http://anothercdn.com/stream/playlist.m3u8
#EXTINF:-1 tvg-id="NonM3U8" tvg-name="Video",Non M3U8 Link
http://somevideo.com/video.mp4
#EXTINF:-1 tvg-id="AlreadyProxied" tvg-name="Already Proxied",Proxied Channel
http://live.artofknot.com:5080/proxy/channel?url=http://oldcdn.com/old.m3u8
"""

input_m3u_path = "input_param.m3u"
output_m3u_path = "output_proxied_param.m3u"
# Buradaki proxy adresi 'url=' ile bitiyor, bu yüzden kontrol mekanizması devreye girer.
proxy_url = "http://live.artofknot.com:5080/proxy/channel?url=" 

# Örnek M3U dosyasını oluştur
with open(input_m3u_path, 'w', encoding='utf-8') as f:
    f.write(sample_m3u_content)
print(f"'{input_m3u_path}' örnek M3U dosyası oluşturuldu.")

# Fonksiyonu çalıştır
proxy_m3u_list_with_param(input_m3u_path, output_m3u_path, proxy_url)

# Oluşturulan dosyayı oku ve içeriğini yazdır (isteğe bağlı)
print("\n--- Oluşturulan 'output_proxied_param.m3u' dosyasının içeriği ---")
try:
    with open(output_m3u_path, 'r', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print("Çıktı dosyası bulunamadı.")
