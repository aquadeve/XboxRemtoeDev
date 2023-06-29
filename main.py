import os
import time
import requests
from flask import Flask, Response

app = Flask(__name__)
download_url = "https://192.168.1.101:11443/ext/screenshot?download=true&hdr=false"

def stream_screenshot(frames_per_second):
    delay = 0.1 / frames_per_second
    while True:
        response = requests.get(download_url, verify=False)  # Set verify=False if you're using a self-signed certificate

        if response.status_code == 200:
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + response.content + b'\r\n\r\n')
        
        time.sleep(delay)

@app.route('/')
def serve_screenshot():
    frames_per_second = 60  # Change this value to set the desired frame rate
    return Response(stream_screenshot(frames_per_second), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost', port=5500, threaded=True)
