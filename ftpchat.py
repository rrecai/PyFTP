from ftplib import FTP
import os
import threading
import time

# Dosya içeriğini tutacak değişken
dosya_icerik = ""
# Dosya işlemleri için kilitleme (lock) kullanımı
dosya_lock = threading.Lock()

def ekran_temizle_ve_yenile():
    # Ekranı temizle ve mesajları yeniden göster
    time.sleep(2)
    os.system("cls" if os.name == "nt" else "clear")
    print("Mevcut mesajlar:")
    print(dosya_icerik.strip())

def dosya_guncelle(mesaj):
    global dosya_icerik
    with dosya_lock:
        dosya_icerik += f"{chat_username}: {mesaj}\n"
        with open(dosya_adi, "wb") as dosya:
            dosya.write(dosya_icerik.encode())
        with open(dosya_adi, "rb") as dosya:
            ftp.storbinary("STOR " + dosya_adi, dosya)

def mesaj_alma_ve_gosterme():
    global dosya_icerik
    while True:
        with open(dosya_adi, "wb") as dosya:
            ftp.retrbinary("RETR " + dosya_adi, dosya.write)

        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            dosya_icerik = dosya.read()

        ekran_temizle_ve_yenile()

try:
    # FTP sunucu bilgileri
    ftp_server = "ftpupload.net"
    ftp_username = "your_ftp_username"
    ftp_password = "your_ftp_password"
    chat_username = "Your-Chat-Username"

    # FTP bağlantısı oluştur
    ftp = FTP()
    ftp.connect(ftp_server)
    ftp.login(ftp_username, ftp_password)

    dosya_adi = "chat.txt"

    t1 = threading.Thread(target=mesaj_alma_ve_gosterme)
    t1.start()
    while True:
        mesaj = input("\nMesaj (Çıkmak için 'q' tuşuna basın): ")
        if mesaj.lower() == 'q':
            break
        dosya_guncelle(mesaj)

except Exception as e:
    print("Hata:", e)

finally:
    if 'ftp' in locals():
        ftp.quit()

    print("Son.")
