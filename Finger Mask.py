import cv2
import mediapipe as mp
import math as m
import serial as s

kamera=cv2.VideoCapture(0)
cizim_modul=mp.solutions.drawing_utils
el_modul=mp.solutions.hands
arduino=s.Serial('com3',9600)

def sinyal_yolla(x):
    if x>4.77:
        arduino.write(b'A')
    elif 3.71<=x<=4.77:
        arduino.write(b'B')
    elif 2.385 <= x <3.71:
        arduino.write(b'C')
    elif 1.325<=x<2.385:
        arduino.write(b'D')
    elif 1<=x<1.325:
        arduino.write(b'E')
    elif 1>x:
        arduino.write(b'F')



with el_modul.Hands(static_image_mode=True) as eller:
    while True:
        kontrol, resim=kamera.read()
        sonuc=eller.process(cv2.cvtColor(resim,cv2.COLOR_BGR2RGB))
        mesafeCm=0
        mesafe=0
        yukseklik ,genislik, _ =resim.shape
        if sonuc.multi_hand_landmarks !=None:
            for ellandmark in sonuc.multi_hand_landmarks:
                for koordinat in el_modul.HandLandmark:
                    sinyal_yolla(mesafeCm)
                    koordinat1=ellandmark.landmark[4]
                    koordinat2=ellandmark.landmark[20]
                    cv2.circle(resim,(int(koordinat1.x*genislik),int(koordinat1.y*yukseklik)),4,(255,0,0),4)
                    cv2.circle(resim,(int(koordinat2.x*genislik),int(koordinat2.y*yukseklik)),4,(255,0,0),4)
                    mesafe=(m.sqrt(m.pow((koordinat2.x-koordinat1.x)*genislik,2)+m.pow((koordinat2.y-koordinat1.y)*yukseklik,2)))
                    mesafeCm=mesafe*0.0265
                    sinyal_yolla(mesafeCm)
                    cv2.putText(resim,"Distance: "+f"{int(mesafeCm)}",(50,50),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)
                    cv2.line(resim,(int(koordinat1.x*genislik),int(koordinat1.y*yukseklik)),(int(koordinat2.x*genislik),int(koordinat2.y*yukseklik)),(0,255,0),3)
                    break
        else:
            sinyal_yolla(0)
            cv2.putText(resim, "Distance:0 " , (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

        cv2.imshow("Goruntu",resim)
        if cv2.waitKey(20) == 27:
            break

