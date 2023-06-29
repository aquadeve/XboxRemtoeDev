# XboxRemtoeDev
A poorly made Xbox one/series x/series s dev mode remote access program that uses Capture Screenshot in the dev portal

# Why I made this
because its simple and Remote access no longer works in dev mdoe for me idk if anybody else has this issue too 



# What this supports
this is completely local so You can run OneGuide with this if you want or possibly port foward it to use it anywhere but why would you do that this is very slow
also you can run any app you can't with regular remote play


# Requirments 

Python: Make sure you have Python installed on your system. You can download the latest version of Python from the official Python website (https://www.python.org/downloads/). Follow the installation instructions specific to your operating system.

Required Packages: Install the necessary packages using pip, the package installer for Python. Open a terminal or command prompt and run the following command to install the required packages:

pip install flask requests

Configuration: Set the appropriate values for the download_url variable in the Python code. This URL should point to the location of the image you want to stream. Replace https://192.168.1.101:11443/ext/screenshot?download=true&hdr=false with your local IP and port the IP is the only thing you replace


The Flask application will start running on http://localhost:5500. Open a web browser on your PC and visit this URL to see the streaming of the most recent image.


# code:

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
