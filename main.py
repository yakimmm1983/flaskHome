from flask import Flask,render_template,request,redirect
import requests
from env import *
app = Flask(__name__)
@app.route("/",methods=['POST','GET'])
def main():
    message = ""
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        data = {
            "username":username,
            "password":password
        }
        response = requests.post(f"{BACKEND_URL}auth",json=data)
        if response.status_code == 401:
            message = "Авторизация не успешна"
        else:
            return redirect("/home")
    return render_template("index.html",message=message)
@app.route("/home",methods=['POST','GET'])
def home():
    if request.method == "GET":
        pass
    return render_template("home-page.html")
if __name__ == "__main__":
    app.run()
