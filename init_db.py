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
    
    conn.commit()
    print("✓ Database initialized successfully!")
    print("✓ CATEGORY TABLE created")
    print("✓ PRODUCT TABLE (Core Table) created")
    
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
