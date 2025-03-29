from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret_key"

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "root",  # Replace with your MySQL username
    "password": "V@msi158",  # Replace with your MySQL password
    "database": "ecommerce",
}

def get_db_connection():
    """Establishes and returns a MySQL database connection."""
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=products)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM products WHERE name LIKE %s OR description LIKE %s"
    params = (f"%{query}%", f"%{query}%")
    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=results)

@app.route("/product/<int:product_id>")
def product_details(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if product:
        return render_template("product_details.html", product=product)
    else:
        return "Product not found", 404 # handling product not found.

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = {}

    # Get the quantity from the form and convert it to an integer
    quantity = int(request.form.get("quantity", 1))  # Default value is 1

    # Add the quantity to the cart
    session["cart"][product_id] = session["cart"].get(product_id, 0) + quantity
    session.modified = True
    return redirect(url_for("index"))

@app.route("/cart")
def cart():
    cart_items = []
    total = 0
    if "cart" in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        for product_id, quantity in session["cart"].items():
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                cart_items.append({"product": product, "quantity": quantity})
                total += product["price"] * quantity
        conn.close()
    return render_template("cart.html", cart_items=cart_items, total=total)

@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    if "cart" in session and str(product_id) in session["cart"]: #change product_id to string.
        del session["cart"][str(product_id)] #change product_id to string.
        session.modified = True
    return redirect(url_for("cart"))



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return render_template("register.html", error="Username already exists")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)", (name, description, price))
        conn.commit()
        conn.close()
        return redirect(url_for("admin"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("admin.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)