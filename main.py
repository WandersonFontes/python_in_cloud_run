from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    print("Iniciando projeto no cloud run")
    return "Script finalizado no Cloud Run!"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)