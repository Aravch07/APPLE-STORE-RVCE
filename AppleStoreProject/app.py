from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="arav",
        database="apple"
    )
    return conn

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Show products table
@app.route('/table/<table_name>')
def show_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name}")
    products = cursor.fetchall()
    
    # Get column names
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return render_template('table.html', 
                         table_name=table_name, 
                         products=products, 
                         columns=columns)

# Add product
@app.route('/add/<table_name>', methods=['POST'])
def add_product(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if table_name in ['iphone', 'ipad', 'mac']:
        product_name = request.form['product_name']
        processor = request.form['processor']
        memory = request.form['memory']
        storage = request.form['storage']
        quantity = request.form['quantity']
        price = request.form['price']
        
        cursor.execute(f"""INSERT INTO {table_name} 
                          (product_name, processor, memory, storage, quantity, price) 
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                      (product_name, processor, memory, storage, quantity, price))
    
    elif table_name == 'airpods':
        product_name = request.form['product_name']
        chipset = request.form['chipset']
        fit = request.form['fit']
        battery = request.form['battery']
        quantity = request.form['quantity']
        price = request.form['price']
        
        cursor.execute(f"""INSERT INTO {table_name} 
                          (product_name, chipset, fit, battery, quantity, price) 
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                      (product_name, chipset, fit, battery, quantity, price))
    
    elif table_name == 'accessories':
        product_name = request.form['product_name']
        device = request.form['device']
        quantity = request.form['quantity']
        price = request.form['price']
        
        cursor.execute(f"""INSERT INTO {table_name} 
                          (product_name, device, quantity, price) 
                          VALUES (%s, %s, %s, %s)""",
                      (product_name, device, quantity, price))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Product added successfully!')
    return redirect(url_for('show_table', table_name=table_name))

# Delete product
@app.route('/delete/<table_name>', methods=['POST'])
def delete_product(table_name):
    product_number = request.form['product_number']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"DELETE FROM {table_name} WHERE product_number = %s", (product_number,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Product deleted successfully!')
    return redirect(url_for('show_table', table_name=table_name))

# Add to cart
@app.route('/cart/add/<table_name>', methods=['POST'])
def add_to_cart(table_name):
    product_number = request.form['product_number']
    cart_quantity = int(request.form['cart_quantity'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get product details
    cursor.execute(f"SELECT * FROM {table_name} WHERE product_number = %s", (product_number,))
    product = cursor.fetchone()
    
    # Check if enough quantity available
    current_quantity = product[5] if table_name == 'accessories' else product[6]  # quantity column position
    
    if current_quantity >= cart_quantity:
        # Create cart table if it doesn't exist
        cursor.execute("""CREATE TABLE IF NOT EXISTS cart (
                         id INT AUTO_INCREMENT PRIMARY KEY,
                         product_name VARCHAR(255),
                         price DECIMAL(10,2),
                         quantity INT,
                         table_source VARCHAR(50))""")
        
        # Add to cart
        product_name = product[1]  # product_name is always at index 1
        price = product[-1]  # price is always the last column
        
        cursor.execute("""INSERT INTO cart (product_name, price, quantity, table_source) 
                         VALUES (%s, %s, %s, %s)""",
                      (product_name, price, cart_quantity, table_name))
        
        conn.commit()
        flash('Added to cart successfully!')
    else:
        flash('Not enough quantity available!')
    
    cursor.close()
    conn.close()
    
    return redirect(url_for('show_table', table_name=table_name))

# View cart
@app.route('/cart')
def view_cart():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create cart table if it doesn't exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS cart (
                     id INT AUTO_INCREMENT PRIMARY KEY,
                     product_name VARCHAR(255),
                     price DECIMAL(10,2),
                     quantity INT,
                     table_source VARCHAR(50))""")
    
    cursor.execute("SELECT * FROM cart")
    cart_items = cursor.fetchall()
    
    # Calculate total
    total = sum(item[2] * item[3] for item in cart_items)  # price * quantity
    
    cursor.close()
    conn.close()
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# Remove from cart
@app.route('/cart/remove/<int:cart_id>')
def remove_from_cart(cart_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Item removed from cart!')
    return redirect(url_for('view_cart'))

# Purchase (checkout)
@app.route('/purchase', methods=['POST'])
def purchase():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all cart items
    cursor.execute("SELECT * FROM cart")
    cart_items = cursor.fetchall()
    
    if not cart_items:
        flash('Cart is empty!')
        return redirect(url_for('view_cart'))
    
    # Create purchases table if it doesn't exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS purchases (
                     id INT AUTO_INCREMENT PRIMARY KEY,
                     product_name VARCHAR(255),
                     price DECIMAL(10,2),
                     quantity INT,
                     total DECIMAL(10,2),
                     purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    
    # Process each cart item
    for item in cart_items:
        product_name = item[1]
        price = item[2]
        quantity = item[3]
        table_source = item[4]
        total = price * quantity
        
        # Add to purchases
        cursor.execute("""INSERT INTO purchases (product_name, price, quantity, total) 
                         VALUES (%s, %s, %s, %s)""",
                      (product_name, price, quantity, total))
        
        # Update product quantity in original table
        if table_source == 'accessories':
            cursor.execute(f"""UPDATE {table_source} 
                             SET quantity = quantity - %s 
                             WHERE product_name = %s""", (quantity, product_name))
        else:
            cursor.execute(f"""UPDATE {table_source} 
                             SET quantity = quantity - %s 
                             WHERE product_name = %s""", (quantity, product_name))
    
    # Clear cart
    cursor.execute("DELETE FROM cart")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Purchase completed successfully!')
    return redirect(url_for('purchases'))

# View purchases
@app.route('/purchases')
def purchases():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create purchases table if it doesn't exist
    cursor.execute("""CREATE TABLE IF NOT EXISTS purchases (
                     id INT AUTO_INCREMENT PRIMARY KEY,
                     product_name VARCHAR(255),
                     price DECIMAL(10,2),
                     quantity INT,
                     total DECIMAL(10,2),
                     purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    
    cursor.execute("SELECT * FROM purchases ORDER BY purchase_date DESC")
    purchase_list = cursor.fetchall()
    
    # Calculate total spent
    cursor.execute("SELECT SUM(total) FROM purchases")
    total_spent = cursor.fetchone()[0] or 0
    
    cursor.close()
    conn.close()
    
    return render_template('purchases.html', purchases=purchase_list, total_spent=total_spent)

if __name__ == '__main__':
    app.run(debug=True)


