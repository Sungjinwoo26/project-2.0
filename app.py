from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'Inventery_management_2_0.db'

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO `PRODUCT TABLE (Core Table)` 
        (sku, Name, category_id, price, quantity, shelf_number, reorder_level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (sku, name, category_id, price, quantity, shelf_number, reorder_level, created_at))
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
