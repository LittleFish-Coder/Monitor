import os
import cv2
import time
import threading
import picamera
import requests
import base64

# urlToWeb = 'http://192.168.97.167:4138/avatar'
urlToWeb = 'http://192.168.97.121:4138/monitor'
urlToModel = 'http://192.168.97.121:5000/images'
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

counter = 0

def FaceDetect():
    while True :
        global counter
        localcounter = counter
        try :
            filename = "./Image/image"+str(localcounter)+".jpg"
            image = cv2.imread(filename , cv2.IMREAD_COLOR)
            image = cv2.rotate(image, cv2.ROTATE_180)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)      # Convert to grayscale
            faces = face_cascade.detectMultiScale(gray, 1.1, 5 , minSize=(40,40)) # Detect the faces
            if len(faces) >= 1 :
                print('Detect Face')
                postdata = {
                    'img' : base64.b64encode(cv2.imencode('.jpg',image)[1]).decode(),
                    }   
                r = requests.post(urlToModel,data=postdata)
                time.sleep(3)
        except :
            pass

def cam() :
    with picamera.PiCamera() as camera:
        camera.start_preview()
        # Camera warm-up time
        time.sleep(1)
        try :
            while True :
                global counter
                counter += 1
                if counter > 100 :
                    counter = 1
                filename = "./Image/image"+str(counter)+".jpg"
                camera.capture(filename)
                image = cv2.imread(filename)
                image = cv2.rotate(image, cv2.ROTATE_180)
                cv2.imshow('Instant',image)
                try :
                    postdata = {
                        'img' : base64.b64encode(cv2.imencode('.jpg',image)[1]).decode(),
                        'name':"1"
                    }   
                    r = requests.post(urlToWeb,data=postdata)
                except ValueError :
                    print(ValueError)
                cv2.waitKey(500)
                # time.sleep(0.5)
        except KeyboardInterrupt:
            print("interrupt")
        finally:
            camera.close()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    if os.path.exists('Image') is False :
        os.mkdir('Image')
    else :
        dir = os.listdir('./Image')
        for file in dir :
            os.remove('./Image/'+str(file))

    threading.Thread(target=cam).start()
    time.sleep(1)
    threading.Thread(target=FaceDetect).start()
