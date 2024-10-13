from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

@app.route('/')
def index():
    products = get_products()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
