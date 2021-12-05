
from cvzone.HandTrackingModule import HandDetector  # Libabry Deteksi Tangan dan Jari
import cv2 # Library OpenCV
import cvzone # Libabry cvzone untuk mediapipe

cap = cv2.VideoCapture(0) # Menentukan kamera yang digunakan, nilai 0 artinya meggunakan webcam laptop
cap.set(3, 640) 
cap.set(4, 480)
detector = HandDetector(detectionCon=0.5, maxHands=2) # menentukan jumlah tangan yang dideteksi dalam box
fpsReader = cvzone.FPS() # Menampilkan nilai FPS

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

        totalFingers = fingers_data.count(1) # Perhitungan jumlah jari yang terdeteksi
        cv2.putText(img, f'Jumlah jari:{totalFingers}', (bbox[0], bbox[1] - 30),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2) # Menampilkan kotak hasil jumlah jari


    # Menampilkan nilai FPS
    fps, img = fpsReader.update(img,pos=(500,450),color=(0,0,255),scale=2,thickness=3)

    # Display
    cv2.imshow("Gambar Deteksi Tangan", img) # Menampilkan info di kotak deteksi
    if cv2.waitKey(1) & 0xFF == ord('q'): # Stop kode yang berjalan dengan menekan tombol 'q' pada keyboard
        break # keluar dari proses

cap.release()
cv2.destroyAllWindows() 