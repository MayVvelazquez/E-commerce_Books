'''
# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow


# Crea una instancia de la clase Flask con el nombre de la aplicación
app = Flask(__name__)
# Configura CORS para permitir el acceso desde el frontend al backend
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:EcommerceBooks@localhost/cruddos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Producto(db.Model):  # Producto hereda de db.Model

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, nombre,descripcion, precio, stock, imagen):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase Producto
class ProductoSchema(ma.Schema):

    class Meta:
        fields = ("id", "nombre","descripcion", "precio", "stock", "imagen")

producto_schema = ProductoSchema()  # Objeto para serializar/deserializar un producto
productos_schema = ProductoSchema(many=True)  # Objeto para serializar/deserializar múltiples productos


@app.route("/productos", methods=["GET"])
def get_Productos():

    all_productos = Producto.query.all()  # Obtiene todos los registros de la tabla de productos
    result = productos_schema.dump(all_productos)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla


@app.route("/productos/<id>", methods=["GET"])
def get_producto(id):

    producto = Producto.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    return producto_schema.jsonify(producto)  # Retorna el JSON del producto

@app.route("/productos/<id>", methods=["DELETE"])
def delete_producto(id):

    producto = Producto.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    db.session.delete(producto)  # Elimina el producto de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(producto)  # Retorna el JSON del producto eliminado

@app.route("/productos", methods=["POST"])  # Endpoint para crear un producto
def create_producto():
    nombre = request.json["nombre"]  # Obtiene el nombre del producto del JSON proporcionado
    descripcion = request.json["descripcion"]
    precio = request.json["precio"]  # Obtiene el precio del producto del JSON proporcionado
    stock = request.json["stock"]  # Obtiene el stock del producto del JSON proporcionado
    imagen = request.json["imagen"]  # Obtiene la imagen del producto del JSON proporcionado
    new_producto = Producto(nombre,descripcion, precio, stock, imagen)  # Crea un nuevo objeto Producto con los datos proporcionados
    db.session.add(new_producto)  # Agrega el nuevo producto a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(new_producto)  # Retorna el JSON del nuevo producto creado

@app.route("/productos/<id>", methods=["PUT"])  # Endpoint para actualizar un producto
def update_producto(id):
    producto = Producto.query.get(id)  # Obtiene el producto existente con el ID especificado

    # Actualiza los atributos del producto con los datos proporcionados en el JSON
    producto.nombre = request.json["nombre"]
    producto.descripcion = request.json["descripcion"]
    producto.precio = request.json["precio"]
    producto.stock = request.json["stock"]
    producto.imagen = request.json["imagen"]

    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(producto)  # Retorna el JSON del producto actualizado


# Programa Principal
if __name__ == "__main__":
#     # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
     app.run(debug=True, port=5000)
'''
