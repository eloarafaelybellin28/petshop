from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from data import products

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "123"
jwt = JWTManager(app)

@app.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    preco_asc = request.args.get("preco_asc")
    preco_desc = request.args.get("preco_desc")
    description_part = request.args.get("description_part")

    filtered_products = products.copy()

    if preco_asc:
        filtered_products.sort(key=lambda x: x["product_price"])
    elif preco_desc:
        filtered_products.sort(key=lambda x: x["product_price"], reverse=True)
    elif description_part:
        filtered_products = [p for p in products if description_part.lower() in p["product_description"].lower()]

    return jsonify(filtered_products)

@app.route("/products/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product_by_id(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify(msg="Produto não encontrado"), 404

if __name__ == "__main__":
    app.run(debug=True)
