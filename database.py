import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect("business_manager.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mijozlar (id INTEGER PRIMARY KEY AUTOINCREMENT, ism TEXT NOT NULL, telefon TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ombor (id INTEGER PRIMARY KEY AUTOINCREMENT, mahsulot_nomi TEXT UNIQUE NOT NULL, narxi REAL NOT NULL, miqdori INTEGER NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS buyurtmalar (id INTEGER PRIMARY KEY AUTOINCREMENT, mijoz_id INTEGER, umumiy_summa REAL, sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS qarzdorlik (id INTEGER PRIMARY KEY AUTOINCREMENT, mijoz_id INTEGER, qarz_summasi REAL, izoh TEXT, sana TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Ombor funksiyalari
def add_product(nomi, narxi, miqdori):
    conn = connect_db()
    try:
        conn.execute('INSERT INTO ombor (mahsulot_nomi, narxi, miqdori) VALUES (?, ?, ?)', (nomi, narxi, miqdori))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_products():
    conn = connect_db()
    prods = conn.execute('SELECT id, mahsulot_nomi, narxi, miqdori FROM ombor').fetchall()
    conn.close()
    return prods

def get_product_by_id(p_id):
    conn = connect_db()
    prod = conn.execute('SELECT id, mahsulot_nomi, narxi, miqdori FROM ombor WHERE id = ?', (p_id,)).fetchone()
    conn.close()
    return prod

# Mijoz funksiyalari
def add_customer(ism, telefon):
    conn = connect_db()
    try:
        conn.execute('INSERT INTO mijozlar (ism, telefon) VALUES (?, ?)', (ism, telefon))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_customers():
    conn = connect_db()
    custs = conn.execute('SELECT id, ism, telefon FROM mijozlar').fetchall()
    conn.close()
    return custs

def get_customer_by_id(c_id):
    conn = connect_db()
    cust = conn.execute('SELECT id, ism, telefon FROM mijozlar WHERE id = ?', (c_id,)).fetchone()
    conn.close()
    return cust

# Buyurtma
def create_order(c_id, p_id, qty, total_price):
    conn = connect_db()
    try:
        stock = conn.execute('SELECT miqdori FROM ombor WHERE id = ?', (p_id,)).fetchone()[0]
        if stock < qty: return False, "Yetarli mahsulot yo'q"
        conn.execute('UPDATE ombor SET miqdori = miqdori - ? WHERE id = ?', (qty, p_id))
        conn.execute('INSERT INTO buyurtmalar (mijoz_id, umumiy_summa) VALUES (?, ?)', (c_id, total_price))
        conn.commit()
        return True, "Saqlandi!"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()

# Qarz
def add_debt(c_id, summa, izoh):
    conn = connect_db()
    conn.execute('INSERT INTO qarzdorlik (mijoz_id, qarz_summasi, izoh) VALUES (?, ?, ?)', (c_id, summa, izoh))
    conn.commit()
    conn.close()

def get_all_debts():
    conn = connect_db()
    debts = conn.execute('SELECT q.id, m.ism, m.telefon, q.qarz_summasi, q.izoh, q.sana FROM qarzdorlik q JOIN mijozlar m ON q.mijoz_id = m.id WHERE q.qarz_summasi > 0').fetchall()
    conn.close()
    return debts

def pay_debt(d_id, summa):
    conn = connect_db()
    row = conn.execute('SELECT qarz_summasi FROM qarzdorlik WHERE id = ?', (d_id,)).fetchone()
    if not row: return False, "Qarz topilmadi"
    qoldiq = row[0] - summa
    if qoldiq <= 0:
        conn.execute('UPDATE qarzdorlik SET qarz_summasi = 0 WHERE id = ?', (d_id,))
        msg = "Qarz uzildi!"
    else:
        conn.execute('UPDATE qarzdorlik SET qarz_summasi = ? WHERE id = ?', (qoldiq, d_id))
        msg = f"Qoldi: {qoldiq}"
    conn.commit()
    conn.close()
    return True, msg

# --- HISOBOT FUNKSIYASI ---
def get_reports():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Bugungi sana (YYYY-MM-DD formatida)
    today = datetime.now().strftime('%Y-%m-%d')
    # Joriy oy (YYYY-MM formatida)
    current_month = datetime.now().strftime('%Y-%m')
    
    # Kunlik savdo
    cursor.execute("SELECT SUM(umumiy_summa) FROM buyurtmalar WHERE date(sana) = ?", (today,))
    kunlik = cursor.fetchone()[0] or 0
    
    # Oylik savdo
    cursor.execute("SELECT SUM(umumiy_summa) FROM buyurtmalar WHERE strftime('%Y-%m', sana) = ?", (current_month,))
    oylik = cursor.fetchone()[0] or 0
    
    conn.close()
    return kunlik, oylik