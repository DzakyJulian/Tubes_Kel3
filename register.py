import bcrypt
import mysql.connector
from admin_db_info import get_current_mysql_password

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
    database="ebookingclass"
)
cursor = conn.cursor()

def valid_email(email):
    return email.endswith('@gmail.com')

def register_user():
    print("\n=== Register Mahasiswa ===")
    nim = input("Masukkan NIM: ").strip().lower()
    email = input("Masukkan Email: ").strip().lower()
    password = input("Masukkan Password: ").strip()
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    role = "mahasiswa"

    # if role not in ['admin', 'mahasiswa']:
    #     print("Role tidak valid. Silakan gunakan 'admin' atau 'mahasiswa'.")
    #     return

    try:
        cursor.execute('''
        INSERT INTO users (nim, email, password, user_role)
        VALUES (%s, %s, %s, %s)
        ''', (nim, email, password_hashed.decode('utf-8'), role))
        conn.commit()
        print("Registrasi berhasil!")
    except mysql.connector.IntegrityError:
        print("Email atau NIM sudah digunakan!")
    finally:
        cursor.close()
        conn.close()