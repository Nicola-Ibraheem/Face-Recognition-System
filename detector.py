import cv2
import sqlite3


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

recognizer = cv2.face_LBPHFaceRecognizer.create()
recognizer.read('trainner/trainner.yml')

def getProfile(Id):

    conn = sqlite3.connect("face_base.db")

    cmd = "SELECT * FROM People WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    profile=None

    for row in cursor:
        profile = row
    conn.close()

    return profile






while True:
    ret, img =cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



    faces=faceCascade.detectMultiScale(gray, 1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
        print (conf)

        if(conf<74):
            profile = getProfile(Id)

            if(profile!=None):
                cv2.putText(img, str(profile[1]),(x, y + h+30),cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 255))
                cv2.putText(img, str(profile[2]), (x, y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))


        else:
            cv2.putText(img, str("Unknown"), (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

    cv2.imshow('img',img)

    if (cv2.waitKey(10)==ord('q')):
        break
cam.release()
cv2.destroyAllWindows()
