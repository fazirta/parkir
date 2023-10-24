import time
import datetime
import math
import pyqrcode
import cv2
import tkinter as tk

database = []
user = 0
PRICE = {"MOTOR": 2000, "MOBIL": 4000}


def masuk(img_lbl, txt_lbl, kendaraan: str):
    waktu_masuk = time.time()
    database.append([waktu_masuk, kendaraan])
    global user
    user += 1
    txt_lbl.configure(
        text=f"Nomor user anda adalah {user} \nKendaraan anda adalah {kendaraan.lower()}"
    )
    show_QR(img_lbl)


def keluar(txt_lbl):
    while True:
        global user
        user = scan_qr_code()
        if user is not None and database[user - 1] != None:
            waktu_masuk = database[user - 1][0]
            waktu_keluar = time.time()
            total_price = 0
            time_diff = waktu_keluar - waktu_masuk
            total_price = PRICE.get(database[user - 1][1]) * math.ceil(time_diff / 3600)
            kendaraan = database[user - 1][1]
            txt_lbl.configure(
                text=f"Lama anda adalah {datetime.timedelta(seconds=time_diff)} \nKendaraan anda adalah {kendaraan.lower()} \nTotal harga adalah {total_price}"
            )
            database[user - 1] = None
            break
        else:
            txt_lbl.configure(text="User telah keluar")
            break


def show_QR(img_lbl):
    global user
    qr = pyqrcode.create(user)
    img = tk.BitmapImage(data=qr.xbm(scale=8))
    img_lbl.configure(image=img)
    img_lbl.image = img


def scan_qr_code():
    cap = cv2.VideoCapture(1)
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        if img is None:
            continue

        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            cap.release()
            cv2.destroyAllWindows()
            return int(data)

        cv2.imshow("QRCODEscanner", img)
        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


root = tk.Tk()
root.title("Parkir")
root.geometry("500x500")

txt_lbl = tk.Label(root, text="Silakan pilih opsi")
txt_lbl.pack()

img_lbl = tk.Label(root)
img_lbl.pack()

button_masuk_motor = tk.Button(
    root, text="Masuk motor", command=lambda: masuk(img_lbl, txt_lbl, "MOTOR")
)
button_masuk_motor.pack()
button_masuk_mobil = tk.Button(
    root, text="Masuk mobil", command=lambda: masuk(img_lbl, txt_lbl, "MOBIL")
)
button_masuk_mobil.pack()
button_keluar = tk.Button(root, text="Keluar", command=lambda: keluar(txt_lbl))
button_keluar.pack()

root.mainloop()
