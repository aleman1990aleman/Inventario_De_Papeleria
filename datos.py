from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import base64_python
import os

base64 = base64_python.Base64()
class Inventario:
    def __init__(self, uri: str = 'mongodb+srv://Zanon:ewrp9HvElnKBwwXL@cluster0.gtw8gje.mongodb.net/?appName=Cluster0'):
        """Inicializar conexión a MongoDB"""
        try:
            self.cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.cliente.admin.command('ping')
            self.db = self.cliente['inventario_papeleria']
            self.productos = self.db['productos']
            self.usuarios = self.db['usuarios']
            self.clientes = self.db['clientes']
            self.compras = self.db['compras']
            self.ventas = self.db['ventas']
            self.proveedores = self.db['proveedores']
            self.cursor = self.productos.find()
            
            # Crear índices necesarios
            self._crear_indices()
            print("✅ Conectado a MongoDB")
        except ConnectionFailure:
            print("❌ Error: No se pudo conectar a MongoDB")
            raise
    
    def _crear_indices(self):
        """Crear índices para mejorar rendimiento"""
        self.usuarios.create_index("email", unique=True)
    
    def crear_usuario(self, nombre: str, email: str, password: str) -> Optional[str]:
        """Crear un nuevo usuario"""
        try:
            resultado = self.usuarios.insert_one({
                "_id": ObjectId(),
                "nombre": nombre,
                "email": email,
                "contraseña": base64.encode(password),
                "fecha_registro": datetime.now()
            })
            return str(resultado.inserted_id)
        except DuplicateKeyError:
            print(f"❌ Error: El email {email} ya está registrado")
            return None
    
    def obtener_usuario(self, usuario_id: str) -> Optional[Dict]:
        """Obtener usuario por ID"""
        try:
            usuario = self.usuarios.find_one({"_id": ObjectId(usuario_id)})
            if usuario:
                usuario['_id'] = str(usuario['_id'])
            return usuario
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def acceder(self, email: str, password: str) -> Optional[Dict]:
        """Obtener usuario por e-mail"""
        try:
            usuario = self.usuarios.find_one({"email": email, "contraseña": base64.encode(password)})
            if usuario:
                usuario['email'] = str(usuario['email'])
                usuario["contraseña"] = str(base64.encode(password))
            return usuario
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return None
        
    def obtener_con_email(self, email: str) -> Optional[Dict]:
        """Obtener usuario por e-mail"""
        try:
            usuario = self.usuarios.find_one({"email": email})
            if usuario:
                usuario['email'] = str(usuario['email'])
                usuario["contraseña"] = str(base64.encode(usuario["contraseña"]))
            return usuario
        except Exception as e:
            print(f"Error al obtener usuario por email: {e}")
            return None
        
    def crear_producto(self, nombre: str, precio: float, stock: int, categoria: str) -> Optional[str]:
        """Crear un nuevo usuario"""
        try:
            resultado = self.productos.insert_one({
                "_id": ObjectId(),
                "nombre": nombre,
                "precio": precio,
                "stock": stock,
                "categoria": categoria,
                "fecha_agregado": datetime.now()
            })
            return str(resultado.inserted_id)
        except DuplicateKeyError:
            print(f"❌ Error: El email {email} ya está registrado")
            return None