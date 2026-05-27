from flask import Flask, render_template, request, redirect, url_for, flash, abort
from datos import Inventario
from flask_mail import Mail, Message
import base64_python

app = Flask(__name__)
app.config["SECRET_KEY"] = "secreto"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'oyami7020@gmail.com'
app.config['MAIL_PASSWORD'] = 'hzraxcsdxftkxkon'
app.config['MAIL_DEFAULT_SENDER'] = 'oyami7020@gmail.com'
usuario = None
base64 = base64_python.Base64()
mail = Mail()
mail.init_app(app)
inventario = Inventario()

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
            return redirect(url_for("dashboard"))
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
        usuario_encontrado = inventario.obtener_con_email(email)
        if usuario_encontrado != None:
            msg = Message(
                subject = "Recuperacion de contraseña",
                sender = "sugaritisron@gmail.com", 
                recipients = [email],
            )
            mail.send(msg)
            flash("Se envio el correo")
            return redirect(url_for("index"))
        else:
            flash("No se pudo recuperar la contraseña", "error")
            return redirect(url_for("recuperar"))
        
@app.route("/dashboard")
def dashboard():
    global usuario
    if usuario != None:
        return render_template("dashboard.html")
    return redirect(url_for("index"))

@app.route("/añadir")
def añadir():
    global usuario
    cursor = list(inventario.productos.find({}))
    if usuario != None:
        return render_template("añadir_producto.html", cursor=cursor)
    return redirect(url_for("index"))

@app.route("/agregar-producto", methods=["POST", "GET"])
def agregar():
    inventario = Inventario()
    if request.method == "POST":
        name = request.form.get("nombre")
        categoria = request.form.get("categoria")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")
        inventario.crear_producto(name, precio, cantidad, categoria)
        flash("El producto es creo correctamente")
        return redirect(url_for("añadir"))
    else:
        flash("No se pudo añadir el producto", "error")
        return redirect(url_for("añadir"))
    
@app.route("/eliminar-producto", methods=["POST", "GET"])
def eliminar():
    inventario = Inventario()
    if request.method == "POST":
        id = request.form.get("producto_id")
        inventario.eliminar_producto(id)
        flash("El producto se elimino exitosamente")
        return redirect(url_for("añadir"))
    else:
        flash("No se pudo eliminar el producto", "error")
        return redirect(url_for("añadir"))
    
@app.route("/stock")
def stock():
    global usuario
    cursor = list(inventario.productos.find({}))
    if usuario != None:
        return render_template("stock.html", cursor=cursor)
    return redirect(url_for("index"))

@app.route("/actualizar-producto", methods=["POST", "GET"])
def actualizar():
    inventario = Inventario()
    try:
        if request.method == "POST":
            id = request.form.get("id")
            name = request.form.get("nombre")
            categoria = request.form.get("categoria")
            cantidad = request.form.get("cantidad")
            precio = request.form.get("precio")
            inventario.actualizar_producto(id, name, precio, cantidad, categoria)
            flash("El producto es actualizo correctamente")
            return redirect(url_for("añadir"))
        else:
            flash("No se pudo aztualizar el producto", "error")
            return redirect(url_for("añadir"))
    except Exception:
        flash("Ocurrio un error desconocido")
        return redirect(url_for("stock"))
if __name__ == '__main__':
    app.run(debug=True)