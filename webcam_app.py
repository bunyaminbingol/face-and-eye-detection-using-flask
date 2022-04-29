from flask import Flask, render_template, Response, request
import cv2
app = Flask(__name__)
camera = cv2.VideoCapture(0) 
def generate_frames(): # bu fonksiyon her bir frame için çağırılır
    camera = cv2.VideoCapture(0)
    fase_cascade = cv2.CascadeClassifier('cascade/frontalface.xml')
    eyes_cascade = cv2.CascadeClassifier('cascade/eye.xml')
    while True:
        ret, frame = camera.read()
        if ret:
            frame = cv2.flip(frame,1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = fase_cascade.detectMultiScale(gray, 1.3, 7)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                frame2 = frame[y:y+h,x:x+w]
                gray2 = gray[y:y+h,x:x+w]
                eyes = eyes_cascade.detectMultiScale(gray2,1.3,7)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(frame2,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
        else:
            camera.release()
            break
        # yield ile frame'i gönderiyoruz
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
@app.route('/') # route ile url'yi tanımlıyoruz
def index(value=0):
    return  render_template('camera/index.html',value=value)

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/',methods=['POST','GET']) # bu kısımda post ile gönderilen verileri alıyoruz
def submit():
    if request.method == 'POST':
        value =  request.values.get("StartStop")
        if value == "0":
            print("Stop")
            camera.release()
        return  render_template('camera/index.html',value=value)
    
if __name__ == '__main__':
    app.run()
