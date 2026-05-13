from flask import Flask, render_template, request, redirect, url_for, flash
from datos import Inventario

app = Flask(__name__)
app.config["SECRET_KEY"] = "secreto"
usuario = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    inventario = Inventario()
    global usuario
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password")
        usuario = inventario.acceder(email, password)
        if usuario != None:
            return redirect(url_for("gestor"))
        elif usuario == None:
            flash("Error al iniciar sesión", "error")
            return redirect(url_for("index"))
        else:
            flash("Ya tienes una cuenta", "error")
            return redirect(url_for("index"))
    
if __name__ == '__main__':
    app.run(debug=True)