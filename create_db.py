import mysql.connector
from admin_db_info import get_current_mysql_password

def create_database():
    # Koneksi ke MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",   # Username default XAMPP
        password=get_current_mysql_password()
    )
    
    cursor = conn.cursor()
    
    # Mengecek apakah database sudah ada
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    
    db_exists = False
    for db in databases:
        if db[0] == 'ebookingclass':
            db_exists = True
            break
        
    if not db_exists:
        # Membuat database jika belum ada
        cursor.execute("CREATE DATABASE ebookingclass")
        print("Database 'ebookingclass' berhasil dibuat.")
    else:
        print("Database 'ebookingclass' sudah ada.")