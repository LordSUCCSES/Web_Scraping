import argparse
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import platform
from os import system

class color:
    SİYAH = "\033[0;30m"
    KIRMIZI = "\033[0;31m"
    YEŞİL = "\033[0;32m"
    KAHVERENGİ = "\033[0;33m"
    MAVİ = "\033[0;34m"
    PEMBE = "\033[0;35m"
    CAMGÖBEĞİ = "\033[0;36m"
    SARI = "\033[1;33m"
    SON = "\033[0m"

banner = color.MAVİ + r"""
 _____ _   _ _____  _____  _____ _____ _____ 
/  ___| | | /  __ \/  __ \|  ___/  ___/  ___|
\ `--.| | | | /  \/| /  \/| |__ \ `--.\ `--. 
 `--. \ | | | |    | |    |  __| `--. \`--. \
/\__/ / |_| | \__/\| \__/\| |___/\__/ /\__/ /
\____/ \___/ \____/ \____/\____/\____/\____/ 
""" + color.SON

osismi = platform.system()

proxy_ip = '123.45.67.89'
proxy_port = 8080

def url_cek(url, kullanici_agenti, cikis_dosyasi=None, proxy=None):
    if osismi == "Windows":
        system("cls")
    elif osismi == "Linux":
        system("clear")
    print(banner)
    basliklar = {'User-Agent': kullanici_agenti}
    proxy = {'http': f'http://{proxy_ip}:{proxy_port}'}
    try:
        cevap = requests.get(url, headers=basliklar, proxies=proxy)

        if cevap.status_code == 200:
            soup = BeautifulSoup(cevap.text, 'html.parser')
            linkler = soup.find_all('a')

            if cikis_dosyasi:
                with open(cikis_dosyasi, 'w', encoding='utf-8') as dosya:
                    for link in linkler:
                        href = link.get('href')
                        if href:
                            dosya.write(href + '\n')
                    print(color.CAMGÖBEĞİ + f"Veriler {cikis_dosyasi} dosyasına kaydedildi." + color.SON)
                    for link in linkler:
                        href = link.get('href')
                        if href:
                            print(color.MAVİ + href + color.SON)
            else:
                for link in linkler:
                    href = link.get('href')
                    if href:
                        print(href)
        else:
            print(color.KIRMIZI + "Sayfa çekilemedi. Hata kodu:", cevap.status_code + color.SON)

    except requests.exceptions.RequestException as e:
        print(color.KIRMIZI + "İstek hatası:", e + color.SON)

def main():
    arguman_analizcisi = argparse.ArgumentParser(description='URL üzerinde web scraping yapma')
    arguman_analizcisi.add_argument('-u', '--url', type=str, required=True, help='Web scraping yapılacak URL')
    arguman_analizcisi.add_argument('-o', "--output", required=False, help="Çıktı Parametresi")

    argumanlar = arguman_analizcisi.parse_args()

    kullanici_agenti = UserAgent().random

    if argumanlar.url:
        url_cek(argumanlar.url, kullanici_agenti, argumanlar.output)
    else:
        print(color.KIRMIZI + "Lütfen bir URL belirtin. Örneğin: -u https://www.example.com" + color.SON)

if __name__ == "__main__":
    main()