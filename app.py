from flask import Flask, render_template, request, redirect, url_for, flash
from datos import Inventario
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
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
            return redirect(url_for("place"))
        elif usuario == None:
            flash("Error al iniciar sesión", "error")
            return redirect(url_for("index"))
        else:
            flash("Ya tienes una cuenta", "error")
            return redirect(url_for("index"))
        
@app.route('/registro')
def registro():
    if usuario != None:
        return redirect(url_for("place"))
    return render_template("registro.html")

@app.route("/registrar", methods=["POST", "GET"])
def registrar():
    error = None
    inventario = Inventario()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        inventario.crear_usuario(name, email, password)
        return redirect(url_for("index"))
    else:
        flash("No se pudo crear la cuenta", "error")
        return redirect(url_for("registro"))
    
@app.route("/place")
def place():
    if usuario == None:
        return redirect(url_for("index"))
    return render_template("placeholder.html")

@app.route("/recuperar")
def recuperar():
    if usuario != None:
        return redirect(url_for("place"))
    return render_template("recuperar.html")

@app.route("/recuperacion", methods=["POST", "GET"])
def recuperacion():
    global usuario 
    inventario = Inventario()
    if request.method == "POST":
        email = request.form.get("email")
        if email == inventario.obtener_con_email(email):
            msg = Message(
                subject = "Recuperacion de contraseña",
                sender = "oyami7020@gmail.com", 
                recipients = [email],
            )
            mail.send(msg)
        else:
            flash("No se pudo recuperar la contraseña", "error")
            return redirect(url_for("recuperar"))
if __name__ == '__main__':
    app.run(debug=True)