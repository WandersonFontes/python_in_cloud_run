from flask import Flask
from time import sleep

app = Flask(__name__)

@app.route('/')
def home():
    for _ in range(1,6):
        sleep(1)

    return "Script finalizado no Cloud Run!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)