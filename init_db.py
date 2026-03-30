import sqlite3
from datetime import datetime

DATABASE = 'Inventery_management_2_0.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create CATEGORY TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `CATEGORY TABLE` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create PRODUCT TABLE (Core Table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `PRODUCT TABLE (Core Table)` (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL UNIQUE,
            Name TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            shelf_number TEXT NOT NULL,
            reorder_level INTEGER NOT NULL,
            barcode_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES `CATEGORY TABLE`(id)
        )
    ''')
    
    # Create STOCK MOVEMENT TABLE (Audit Trail)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `STOCK MOVEMENT` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES `PRODUCT TABLE (Core Table)`(ID)
        )
    ''')
    
    conn.commit()
    print("✓ Database initialized successfully!")
    print("✓ CATEGORY TABLE created")
    print("✓ PRODUCT TABLE (Core Table) created")
    print("✓ STOCK MOVEMENT TABLE created")
    
    # Add barcode_path column if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE `PRODUCT TABLE (Core Table)` ADD COLUMN barcode_path TEXT")
        conn.commit()
        print("✓ Added barcode_path column to PRODUCT TABLE")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ barcode_path column already exists")
        else:
            print(f"⚠ Migration error: {e}")
    
    # Add buy_price column if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE `PRODUCT TABLE (Core Table)` ADD COLUMN buy_price REAL NOT NULL DEFAULT 0")
        conn.commit()
        print("✓ Added buy_price column to PRODUCT TABLE")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ buy_price column already exists")
        else:
            print(f"⚠ Migration error: {e}")
    
    # Add sell_price column if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE `PRODUCT TABLE (Core Table)` ADD COLUMN sell_price REAL NOT NULL DEFAULT 0")
        conn.commit()
        print("✓ Added sell_price column to PRODUCT TABLE")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ sell_price column already exists")
        else:
            print(f"⚠ Migration error: {e}")
    
    # Add discount column to STOCK MOVEMENT if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE `STOCK MOVEMENT` ADD COLUMN discount REAL DEFAULT 0")
        conn.commit()
        print("✓ Added discount column to STOCK MOVEMENT")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ discount column already exists")
        else:
            print(f"⚠ Migration error: {e}")
    
    # Add final_price column to STOCK MOVEMENT if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE `STOCK MOVEMENT` ADD COLUMN final_price REAL")
        conn.commit()
        print("✓ Added final_price column to STOCK MOVEMENT")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ final_price column already exists")
        else:
            print(f"⚠ Migration error: {e}")
    
    # Add profit column to STOCK MOVEMENT if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE `STOCK MOVEMENT` ADD COLUMN profit REAL")
        conn.commit()
        print("✓ Added profit column to STOCK MOVEMENT")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("✓ profit column already exists")
        else:
            print(f"⚠ Migration error: {e}")
    
    # Create TRANSACTIONS TABLE (POS Billing)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `TRANSACTIONS` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subtotal REAL NOT NULL,
            total_discount REAL DEFAULT 0,
            total_tax REAL DEFAULT 0,
            total_profit REAL DEFAULT 0,
            round_off REAL DEFAULT 0,
            final_amount REAL NOT NULL,
            payment_method TEXT,
            amount_received REAL,
            change_return REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create TRANSACTION_ITEMS TABLE (Line Items)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS `TRANSACTION_ITEMS` (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit_type TEXT DEFAULT 'pcs',
            unit_price REAL NOT NULL,
            buy_price REAL NOT NULL,
            discount_type TEXT DEFAULT 'flat',
            discount_value REAL DEFAULT 0,
            final_unit_price REAL NOT NULL,
            line_total REAL NOT NULL,
            gst_percentage REAL DEFAULT 0,
            cgst REAL DEFAULT 0,
            sgst REAL DEFAULT 0,
            profit_per_unit REAL NOT NULL,
            total_profit REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_id) REFERENCES `TRANSACTIONS`(id),
            FOREIGN KEY (product_id) REFERENCES `PRODUCT TABLE (Core Table)`(ID)
        )
    ''')
    
    conn.commit()
    print("✓ TRANSACTIONS TABLE created")
    print("✓ TRANSACTION_ITEMS TABLE created")
    
    # Insert sample categories
    cursor.execute("SELECT COUNT(*) FROM `CATEGORY TABLE`")
    if cursor.fetchone()[0] == 0:
        sample_categories = [
            ('Electronics', datetime.now()),
            ('Furniture', datetime.now()),
            ('Office Supplies', datetime.now()),
            ('Tools', datetime.now()),
        ]
        cursor.executemany(
            "INSERT INTO `CATEGORY TABLE` (name, created_at) VALUES (?, ?)",
            sample_categories
        )
        conn.commit()
        print("✓ Sample categories added")
    
    conn.close()

if __name__ == '__main__':
    init_db()
