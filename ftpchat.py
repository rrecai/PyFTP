from ftplib import FTP
import os
import threading
import time
import base64

#chatgpt kodu

def b64encode(input_string):
    bytes_input = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(bytes_input)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def b64decode(base64_string):
    base64_bytes = base64_string.encode('utf-8')
    bytes_output = base64.b64decode(base64_bytes)
    output_string = bytes_output.decode('utf-8')
    return output_string


#recai's juicy code(fr)

if os.path.isfile("creds.data"):
    print("Kaydedilen Bilgiler Kullanılıyor.")
    f = open("creds.data", "r")
    raw_data = f.read().split("-!")
    ftp_server = b64decode(raw_data[0])
    ftp_username = b64decode(raw_data[1])
    ftp_password = b64decode(raw_data[2])
    dosya_adi = b64decode(raw_data[3])
    chat_username = b64decode(raw_data[4])
else:
    print("PyFTP'ye Hoşgeldiniz! Lütfen gereken bilgileri giriniz.")
    ftp_server = input("FTP Sunucusu: ")
    ftp_username = input("FTP Sunucusu Kullanıcı Adı: ")
    ftp_password = input("FTP Sunucusu Şifresi: ")
    dosya_adi = input("FTP Sunucusundaki Sohbet Dosyası İsmi(chat.txt gibi): ")
    chat_username = input("Sohbet İsminiz: ")
    save = input("Veriler Kaydedilsin mi?(Evet yada Hayır):")
    while True:
        if save == "Evet":
            data = b64encode(ftp_server) + "-!" + b64encode(ftp_username) + "-!" + b64encode(ftp_password) + "-!" + b64encode(dosya_adi) + "-!" + b64encode(chat_username)
            f = open("creds.data", "a"); f.write(data); f.close()
            break
        if save == "Hayır":
            break
        print("Lütfen Evet Yada Hayır Cevabını Verin.")
        save = input("Veriler Kaydedilsin mi?(Evet yada Hayır):")

#normal kod

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

    # FTP bağlantısı oluştur
    ftp = FTP()
    ftp.connect(ftp_server)
    ftp.login(ftp_username, ftp_password)

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
