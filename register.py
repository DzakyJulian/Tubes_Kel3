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

def email_validation_algorithm(email):
    e_arr = []

    atsym_count = 0
    atsym_pass = False

    dot_count = 0
    dot_pass = False

    is_valid = None

    # Ubah text email menjadi sebuah array, dengan elemennya huruf atau angka
    for i in range(len(email)):
        e_arr.append(email[i])

    # Check apakah ada symbol @?
    for i in range(len(e_arr)):
        if e_arr[i] == "@":
            atsym_count += 1
        else:
            if i == (len(e_arr) - 1):
                atsym_pass = False
                break
            else:
                continue

    # Jika '@' ada 1, maka valid. Lebih dari 1 atau kurang dari 1, maka tidak valid.
    atsym_pass = atsym_count == 1

    # Check apakah ada domain name?
    for i in range(len(e_arr)):
        if e_arr[i] == ".":
            dot_count += 1
        else:
            if i == (len(e_arr) - 1):
                dot_pass = False
            else:
                continue

    # Jika '.' ada lebih dari 1, maka valid. Jika tidak ada, maka tidak valid.
    dot_pass = dot_count >= 1

    # Bagi menjadi 2 bagian email, @ ke kiri, dan @ ke kanan.
    if (atsym_pass and dot_pass):
        em_split = email.split("@")
        kiri_at = em_split[0]
        kanan_at = em_split[1]
        domain = kanan_at.split('.')

        # Check panjang masing2 subdomain dan domain
        # Jika lebih dari 1, maka valid. Jika kurang, maka tidak valid.
        for i in domain:
            if len(i) >= 1:
                is_valid = True
                continue
            else:
                is_valid = False
                break
    else:
        is_valid = False

    return is_valid

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
    
    # Validasi Email
    while True:
        email = input("Masukkan Email: ").strip().lower()
        if len(email) <= 0:
            print("Email tidak boleh kosong.")
        else:
            email_valid = email_validation_algorithm(email)
            if (email_valid == True):
                break
            else:
                print("Email tidak valid!")
        
    
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
            email_valid = email_validation_algorithm(email)
            if (email_valid == True):
                break
            else:
                print("Email tidak valid!")
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