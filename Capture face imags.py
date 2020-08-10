import cv2
import sqlite3

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def InserOrUpdate(Id,name,job):

    conn = sqlite3.connect("face_base.db")
    cmd = "SELECT * FROM People WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    isRecordExist=0

    for row in cursor:
        isRecordExist=1

    if(isRecordExist==1):
        cmd = "UPDATE people SET Name=' "+str(name)+" ' WHERE ID="+str(Id)
    else:
        cmd = "INSERT INTO people(ID,Name,job) Values("+str(Id)+",' "+str(name)+"' ,'"+str(job)+" ' )"

    conn.execute(cmd)
    conn.commit()
    conn.close()




Id = input('enter your id:')
name = input('enter your name:')
job = input('enter your job:')

InserOrUpdate(Id,name,job)
sampleNum = 0
while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # incrementing sample number
        sampleNum = sampleNum + 1
        # saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

    cv2.imshow('frame', img)


    # wait for 100 miliseconds
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum > 20:
        break
cam.release()
cv2.destroyAllWindows()
