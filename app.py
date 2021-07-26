from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# This is how to create a route and return json data
# @app.route("/", methods=["GET"])
# def get():
#    return jsonify({'msg': 'hello world'})

#  Init app
app = Flask(__name__)
basedir =os.path.abspath(os.path.dirname(__file__))# This is the file we're currently in

# Database (my database is a file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This takes away warning in the console
# Init db
db = SQLAlchemy (app)
# Init db
ma = Marshmallow(app)

# Product Class/Model 
# We create fields with .Column then we pass parameters, first data type
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty =db.Column(db.Integer)

    def __init__ (self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema() 
products_schema = ProductSchema(many=True) 

# Create a Product
# Create route with an end point
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    # Here we are instantiating an object
    new_product = Product (name, description, price, qty) # this is stuff coming in from the client  such as (react, vue, postman, wherever!)
    
    db.session.add(new_product)
    # Save to the data base
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get ALL Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

    # Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)


# Update a product
# use PUT request to update products
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()


# Run server
if __name__ == '__main__':
    app.run(debug=True)
