from flask import Flask,render_template,request,redirect
import requests
from env import *
from models.UserModel import UserModel
app = Flask(__name__)
saved_user = None
def Convert(usermodel:UserModel):
    return usermodel
@app.route("/auth",methods=['POST','GET'])
def auth():
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
            global saved_user
            saved_user = Convert(response.json())
            return redirect("/home")
    return render_template("auth.html",message=message)
@app.route("/signup",methods=['POST','GET'])
def signup():
    message = ""
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        full_name = request.form.get("full_name")
        data = {
            "login":username,
            "password":password,
            "full_name":full_name
        }
        response = requests.post(f"{BACKEND_URL}signup",json=data)

        if response.status_code == 401:
            message = "Регистрация не успешна"
        else:
            return redirect("/auth")
    return render_template("signup.html",message=message)
@app.route("/",methods=["GET"])
def main():
    global saved_user
    if saved_user is None:
        return redirect("/auth")
    else:
        return redirect("/home")

@app.route("/home",methods=['POST','GET'])
def home():
    global saved_user
    if request.method == "GET":
        response = requests.get(f"{BACKEND_URL}all-note/{saved_user['id']}")
        notes = response.json()
        print(notes)
        return render_template("home-page.html",notes = notes)
    return render_template("home-page.html")
@app.route("/user-cabinet",methods=['POST','GET'])
def user_cabient():
    global saved_user
    if request.method == "GET":
        pass
    return render_template("user-cabinet.html",
                           username=saved_user["full_name"],
                           login=saved_user["login"]
                           )
def add_note():
    message = ""
    if request.method == "POST":
        user_id = request.form.get("user_id")
        note_name = request.form.get("note_name")
        note_content = request.form.get("note_content")
        data = {
            "user_id":user_id,
            "note_name":note_name,
            "note_content":note_content
        }
        response = requests.post(f"{BACKEND_URL}add-note",json=data)

        if response.status_code != 200:
            message = "Заметка не создана"

    return render_template("home-page.html",message=message)


if __name__ == "__main__":
    app.run()
