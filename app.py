from flask import Flask, request, jsonify, render_template, Request

import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="******",
    database="inventorymanagementsystem"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Define API endpoints


@app.route('/registeruser', methods=['POST'])
def register_user():
    data = request.json  # Assuming you receive JSON data in the request

    # Extract user registration data from the JSON request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Insert user data into the database
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500



@app.route('/getallproducts', methods=['GET'])
def get_all_products():
    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        product_list = []
        for product in products:
            product_dict = {
                "product_id": product[0],
                "name": product[1],
                "description": product[2],
                "price": float(product[3])
            }
            product_list.append(product_dict)
        return jsonify(product_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/order', methods=['POST'])
def create_order():
    data = request.json  # Assuming you receive JSON data in the request

    # Extract order data from the JSON request
    user_id = data.get('user_id')
    # Insert order data into the database
    try:
        cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (user_id,))
        db.commit()
        return jsonify({"message": "Order created successfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/allorders', methods=['GET'])
def get_all_orders():
    try:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        order_list = []
        for order in orders:
            order_dict = {
                "order_id": order[0],
                "user_id": order[1],
                "order_date": order[2].isoformat()
            }
            order_list.append(order_dict)
        return jsonify(order_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/addproduct', methods=['POST'])
def add_product():
    data = request.json  # Assuming you receive JSON data in the request

    # Extract product data from the JSON request
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    # Insert product data into the database
    try:
        cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)",
                       (name, description, price))
        db.commit()
        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/updateproduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json  # Assuming you receive JSON data in the request

    # Extract updated product data from the JSON request
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    try:
        cursor.execute("UPDATE products SET name=%s, description=%s, price=%s WHERE product_id=%s",
                       (name, description, price, product_id))
        db.commit()
        return jsonify({"message": f"Product with ID {product_id} updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500



@app.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        db.commit()
        return jsonify({"message": f"Product with ID {product_id} deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500



@app.route('/getuser/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        user = cursor.fetchone()
        if user:
            user_dict = {
                "user_id": user[0],
                "username": user[1],
                "email": user[2]
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"message": f"User with ID {user_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/getallusers', methods=['GET'])
def get_all_users():
    try:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        user_list = []
        for user in users:
            user_dict = {
                "user_id": user[0],
                "username": user[1],
                "email": user[2]
            }
            user_list.append(user_dict)
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
