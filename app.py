from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import os
from barcode import Code128
from barcode.writer import SVGWriter

app = Flask(__name__)
DATABASE = 'Inventery_management_2_0.db'
BARCODE_DIR = 'static/barcodes'

# Ensure barcode directory exists
os.makedirs(BARCODE_DIR, exist_ok=True)

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def generate_barcode(sku):
    """Generate barcode for product SKU"""
    try:
        # Create barcode using Code128 format (SVG format - no font issues)
        barcode_path = os.path.join(BARCODE_DIR, sku)
        code = Code128(sku, writer=SVGWriter())
        code.save(barcode_path)
        
        # Return relative path for storage
        return f'{BARCODE_DIR}/{sku}.svg'
    except Exception as e:
        print(f"Error generating barcode for SKU {sku}: {e}")
        return None

# ==================== PRODUCT ROUTES ====================

@app.route('/')
def index():
    """Home page - redirects to product listing"""
    return redirect(url_for('view_products'))

# ==================== CATEGORY ROUTES ====================

@app.route('/add_category', methods=['POST'])
def add_category():
    """Add new category"""
    category_name = request.form.get('category_name', '').strip()
    
    # Validation: name is not empty
    if not category_name:
        return redirect(url_for('view_products'))
    
    conn = get_db_connection()
    
    try:
        # Check if category already exists
        existing = conn.execute(
            'SELECT id FROM `CATEGORY TABLE` WHERE LOWER(name) = LOWER(?)',
            (category_name,)
        ).fetchone()
        
        if existing:
            # Category already exists, just redirect
            conn.close()
            return redirect(url_for('view_products'))
        
        # Insert new category
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute(
            'INSERT INTO `CATEGORY TABLE` (name, created_at) VALUES (?, ?)',
            (category_name, created_at)
        )
        conn.commit()
    finally:
        conn.close()
    
    return redirect(url_for('view_products'))

# ==================== PRODUCT ROUTES ====================

@app.route('/products')
def view_products():
    """View all products with filtering and search"""
    conn = get_db_connection()
    
    # Get filter and search parameters
    category_id = request.args.get('category_id')
    search_query = request.args.get('search', '').strip()
    
    # Build query based on filters
    base_query = '''
        SELECT p.*, c.name as category_name 
        FROM `PRODUCT TABLE (Core Table)` p
        LEFT JOIN `CATEGORY TABLE` c ON p.category_id = c.id
        WHERE 1=1
    '''
    params = []
    
    # Apply category filter
    if category_id and category_id != '':
        base_query += ' AND p.category_id = ?'
        params.append(category_id)
    
    # Apply search filter
    if search_query:
        base_query += ' AND LOWER(p.Name) LIKE LOWER(?)'
        params.append(f'%{search_query}%')
    
    base_query += ' ORDER BY p.ID DESC'
    
    products = conn.execute(base_query, params).fetchall()
    categories = conn.execute('SELECT * FROM `CATEGORY TABLE` ORDER BY name').fetchall()
    conn.close()
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category_id,
                         search_query=search_query)

@app.route('/products/add', methods=['POST'])
def add_product():
    """Add new product"""
    sku = request.form['sku']
    name = request.form['name']
    category_id = request.form.get('category_id') or None
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    shelf_number = request.form['shelf_number']
    reorder_level = int(request.form['reorder_level'])
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Generate barcode
    barcode_path = generate_barcode(sku)
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO `PRODUCT TABLE (Core Table)` 
        (sku, Name, category_id, price, quantity, shelf_number, reorder_level, barcode_path, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sku, name, category_id, price, quantity, shelf_number, reorder_level, barcode_path, created_at))
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_products'))

@app.route('/products/edit/<int:id>', methods=['POST'])
def edit_product(id):
    """Edit existing product"""
    sku = request.form['sku']
    name = request.form['name']
    category_id = request.form.get('category_id') or None
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    shelf_number = request.form['shelf_number']
    reorder_level = int(request.form['reorder_level'])
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE `PRODUCT TABLE (Core Table)`
        SET sku = ?, Name = ?, category_id = ?, price = ?, quantity = ?, 
            shelf_number = ?, reorder_level = ?
        WHERE ID = ?
    ''', (sku, name, category_id, price, quantity, shelf_number, reorder_level, id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_products'))

@app.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    """Delete product"""
    conn = get_db_connection()
    conn.execute('DELETE FROM `PRODUCT TABLE (Core Table)` WHERE ID = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('view_products'))

@app.route('/products/buy/<int:id>', methods=['POST'])
def buy_product(id):
    """Buy stock - increase quantity"""
    quantity = int(request.form.get('buy_quantity', 0))
    
    if quantity <= 0:
        return redirect(url_for('view_products'))
    
    conn = get_db_connection()
    
    try:
        # Update product quantity
        conn.execute(
            'UPDATE `PRODUCT TABLE (Core Table)` SET quantity = quantity + ? WHERE ID = ?',
            (quantity, id)
        )
        
        # Log stock movement
        conn.execute(
            'INSERT INTO `STOCK MOVEMENT` (product_id, type, quantity) VALUES (?, ?, ?)',
            (id, 'BUY', quantity)
        )
        
        conn.commit()
    finally:
        conn.close()
    
    return redirect(url_for('view_products'))

@app.route('/products/sell/<int:id>', methods=['POST'])
def sell_product(id):
    """Sell stock - decrease quantity with validation"""
    quantity = int(request.form.get('sell_quantity', 0))
    
    if quantity <= 0:
        return redirect(url_for('view_products'))
    
    conn = get_db_connection()
    
    try:
        # Get current quantity
        product = conn.execute(
            'SELECT quantity FROM `PRODUCT TABLE (Core Table)` WHERE ID = ?', (id,)
        ).fetchone()
        
        if not product:
            conn.close()
            return redirect(url_for('view_products'))
        
        current_qty = product['quantity']
        
        # Validate: prevent negative inventory
        if current_qty < quantity:
            conn.close()
            return redirect(url_for('view_products'))
        
        # Update product quantity
        conn.execute(
            'UPDATE `PRODUCT TABLE (Core Table)` SET quantity = quantity - ? WHERE ID = ?',
            (quantity, id)
        )
        
        # Log stock movement
        conn.execute(
            'INSERT INTO `STOCK MOVEMENT` (product_id, type, quantity) VALUES (?, ?, ?)',
            (id, 'SELL', quantity)
        )
        
        conn.commit()
    finally:
        conn.close()
    
    return redirect(url_for('view_products'))

@app.route('/products/return/<int:id>', methods=['POST'])
def return_product(id):
    """Return stock - increase quantity and log as RETURN"""
    quantity = int(request.form.get('return_quantity', 0))
    
    if quantity <= 0:
        return redirect(url_for('view_products'))
    
    conn = get_db_connection()
    
    try:
        # Update product quantity
        conn.execute(
            'UPDATE `PRODUCT TABLE (Core Table)` SET quantity = quantity + ? WHERE ID = ?',
            (quantity, id)
        )
        
        # Log stock movement as RETURN
        conn.execute(
            'INSERT INTO `STOCK MOVEMENT` (product_id, type, quantity) VALUES (?, ?, ?)',
            (id, 'RETURN', quantity)
        )
        
        conn.commit()
    finally:
        conn.close()
    
    return redirect(url_for('view_products'))

@app.route('/products/get/<int:id>')
def get_product(id):
    """Get single product (for AJAX edit form)"""
    conn = get_db_connection()
    product = conn.execute(
        'SELECT * FROM `PRODUCT TABLE (Core Table)` WHERE ID = ?', (id,)
    ).fetchone()
    conn.close()
    
    if product:
        return jsonify(dict(product))
    return jsonify({'error': 'Product not found'}), 404

# ==================== BARCODE SCANNING ROUTES ====================

@app.route('/scan')
def scan_product():
    """Barcode scanning page with camera interface"""
    return render_template('scan.html')

@app.route('/returns')
def returns_page():
    """Returns management page"""
    conn = get_db_connection()
    
    # Get recent returns with product info
    returns = conn.execute('''
        SELECT sm.id, sm.product_id, sm.type, sm.quantity, sm.timestamp,
               p.sku, p.Name, c.name as category_name
        FROM `STOCK MOVEMENT` sm
        JOIN `PRODUCT TABLE (Core Table)` p ON sm.product_id = p.ID
        LEFT JOIN `CATEGORY TABLE` c ON p.category_id = c.id
        WHERE sm.type = 'RETURN'
        ORDER BY sm.timestamp DESC
        LIMIT 50
    ''').fetchall()
    
    conn.close()
    
    return render_template('returns.html', returns=returns)

@app.route('/api/search_by_sku/<sku>')
def search_by_sku(sku):
    """Search product by SKU (barcode)"""
    conn = get_db_connection()
    product = conn.execute('''
        SELECT p.*, c.name as category_name 
        FROM `PRODUCT TABLE (Core Table)` p
        LEFT JOIN `CATEGORY TABLE` c ON p.category_id = c.id
        WHERE p.sku = ?
    ''', (sku,)).fetchone()
    conn.close()
    
    if product:
        return jsonify(dict(product))
    return jsonify({'error': f'Product with SKU {sku} not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
