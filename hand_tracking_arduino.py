
'''
Created By  : Code and Robot ID
Project     : Turn ON/Off Lamp Using Hand Tracking
Version     : 01
Date        : 06 Agustus 2021
'''

from cvzone.HandTrackingModule import HandDetector  # Libabry Deteksi Tangan dan Jari
import cv2 # Library OpenCV
import cvzone # Libabry cvzone untuk mediapipe
import serial # Library untuk komunikasi python di laptop dengan Arduino Uno
import time

serialComm = serial.Serial('COM3', 9600)
serialComm.timeout = 1

cap = cv2.VideoCapture(0) # Menentukan kamera yang digunakan, nilai 0 artinya meggunakan webcam laptop
cap.set(3, 680) 
cap.set(4, 480)
detector = HandDetector(detectionCon=0.5, maxHands=1) # menentukan jumlah tangan yang dideteksi dalam box
fpsReader = cvzone.FPS() # Menampilkan nilai FPS
pTime = 0

while True:
    # Get image frame
    success, img = cap.read() # membaca gambar hasil capture

    # Find the hand and its landmarks
    img = detector.findHands(img) # menemukan tangan dalam box
    lmList, bboxInfo = detector.findPosition(img) # menentukan posisi tangan

    if len(lmList) != 0:
            print(lmList[4])

    if lmList:
        bbox = bboxInfo['bbox'] # menampilakn box deteksi tangan
        fingers_data = detector.fingersUp() # Ambil data jumlah jari yang terdeteksi
        fingers_data_serial = (list(map(int, fingers_data))) # mengambil data jumlah jari yang terdeteksi 
                                                            # yang nantinya dikirm via serial ke Arduino

        # Info tracking box
        totalFingers = fingers_data.count(1)
        cv2.putText(img, f'Jumlah jari:{totalFingers}', (bbox[0], bbox[1] - 30),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)

        # Info samping kiri
        cv2.putText(img, f'Jumlah jari: {totalFingers}', (20, 440), cv2.FONT_HERSHEY_PLAIN,
                1.3, (0, 255, 255), 2)

        # Find Hand Type
        myHandType = detector.handType() # menentukan tangan kiri atau tangan kanan yang di deteksi
        cv2.putText(img, f'Tangan:{myHandType}', (bbox[0], bbox[1] - 50),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)
        cv2.putText(img, f'Tangan: {myHandType}', (20, 420), cv2.FONT_HERSHEY_PLAIN,
                1.3, (0, 255, 255), 2)

        # Menampilkan teks Code Robot ID
        cv2.putText(img, 'Created by: Code and Robot ID', (20, 460), cv2.FONT_HERSHEY_PLAIN,
                1.3, (0, 255, 255), 2)

        # variabel counter
        counter = 0 # Variabel counter  untuk jari 1 - 5
        hand_mode = 0 # variabel tangan kiri atau kanan

        if myHandType == "Right":
            hand_mode = "1" # jika tangan kanan maka kirim kode 1 ke serial Arduino
        elif myHandType == "Left":
            hand_mode = "2"  # jika tangan kiri maka kirim kode 2 ke serial Arduino

        print("Nilai hand Mode: ", hand_mode) # Baris untuk menampilkan mode tangan pada Promptshell
        e='\n'
        serialComm.write(str(hand_mode).encode()) # mengirim kode mode tangan kiri atau kanan ke serial

        # Mengirim angka 1-5 via serial
        for i in fingers_data_serial:
            counter += i
            print("Nilai Counter: ", counter) # untuk menampilkan jumlah jari yang terdeteksi di Promptshell
        e='\n'
        serialComm.write(str(counter).encode()) # Mengirim jumlah jari yang terdeteksi ke serial Arduino
        serialComm.write(e.encode()) # untuk baris baru, agar tidak tercampur data serialnya

        # Menampilkan pilihan Text "Nyala/Mati"
        if counter > 0:
            text = " ON / Nyala"
        else:
            text = " OFF / Mati"

        cv2.putText(img, f'Lampu:{text}', (20, 400), cv2.FONT_HERSHEY_PLAIN,
                1.3, (255, 255, 0), 2) # box nampilin lampu mati atau hidup


    # Menampilkan nilai FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 0, 255), 2)
    
    # Nilai FPS from cvzone
    fps, img = fpsReader.update(img,pos=(500,450),color=(0,0,255),scale=2,thickness=3)

    # Menampilkan IG
    cv2.putText(img, f'IG: @coderobot_id', (40, 40), cv2.FONT_HERSHEY_PLAIN,
                1.5, (0, 255, 255), 2)
    
    # Display
    cv2.imshow("On/Off Lamp Using Hand Tracking, by: Code Robot ID", img) # Menampilkan info di kotak deteksi
    if cv2.waitKey(1) & 0xFF == ord('q'): # Stop kode yang berjalan dengan menekan tombol 'q' pada keyboard
        break # keluar dari proses

cap.release()
cv2.destroyAllWindows()