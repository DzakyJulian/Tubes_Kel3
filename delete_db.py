import mysql.connector
from admin_db_info import get_current_mysql_password

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
)

cursor = conn.cursor()

def delete_database():
    # Mengecek apakah database sudah ada
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    
    db_exists = False
    for db in databases:
        if db[0] == 'ebookingclass':
            db_exists = True
            break
        
    if db_exists == True:
        cursor.execute("""
        DROP DATABASE ebookingclass;
        """)
        print("Database berhasil dihapus.")
    else:
        print("Terjadi suatu masalah. Database sudah dihapus atau tidak ada.")
        