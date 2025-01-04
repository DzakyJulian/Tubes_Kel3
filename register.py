import bcrypt
import mysql.connector
import random
from admin_db_info import get_current_mysql_password
from datetime import datetime

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

def register_mahasiswa():
    print("\n=== Register Mahasiswa ===")
    # advance validation for NIM
    while True:
        try:
            nim = int(input("Masukkan NIM ('0' untuk kembali): "))
        except:
            print("NIM harus angka, tidak boleh kosong, tidak boleh huruf atau simbol lainnya.")
        else:
            break
    
    # Keluar dari register jika input '0'
    if nim == 0:
        return
    
    # Validasi Email kosong
    while True:
        email = input("Masukkan Email: ").strip().lower()
        if len(email) <= 0:
            print("Email tidak boleh kosong")
        else:
            break
        
    
    # Validasi Password kosong
    while True:
        password = input("Masukkan Password: ").strip()
        if len(password) <= 0:
            print("Password tidak boleh kosong")
        else:
            break
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    role = "mahasiswa"

    try:
        cursor.execute('''
        INSERT INTO users (nim, email, password, user_role)
        VALUES (%s, %s, %s, %s)
        ''', (nim, email, password_hashed.decode('utf-8'), role))
        conn.commit()
        print("Registrasi berhasil!")
    except mysql.connector.IntegrityError:
        print("Email atau NIM sudah digunakan!")

def register_admin():
    print("\n=== Register Admin ===")

    # Set value untuk NIM dengan angka acak
    # 2 digit pertama adalah 2 digit terakhir tahun sekarang
    tahun_sekarang = datetime.now().year
    dua_digit_terakhir = str(tahun_sekarang)[2:4]
    nim = str(dua_digit_terakhir+str(random.randrange(0,99999,1)))

    # Advance validation for Email
    while True:
        email = input("Masukkan Email: ").strip().lower()
        if len(email) <= 0:
            print("Email tidak boleh kosong.")
        else:
            break
    # Validasi Password kosong
    while True:
        password = input("Masukkan Password: ").strip()
        if len(password) <= 0:
            print("Password tidak boleh kosong")
        else:
            break
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # SET DEFAULT ROLE UNTUK ADMIN ADALAH MAHASISWA
    # KARENA AKAN BERBAHAYA JIKA SIAPAPUN DAPAT DAFTAR SEBAGAI ADMIN
    role = "mahasiswa"

    try:
        cursor.execute('''
        INSERT INTO users (nim, email, password, user_role)
        VALUES (%s, %s, %s, %s)
        ''', (nim, email, password_hashed.decode('utf-8'), role))
        conn.commit()
        print("")
        print("Registrasi admin berhasil.")
        print("Anda dapat mengakses sebagai administrator setelah developer menyetujui\ndan merubah hak akses akun anda.")
        print("")
    except mysql.connector.IntegrityError:
        print("Email sudah digunakan!")