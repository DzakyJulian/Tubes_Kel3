import mysql.connector
import bcrypt
import unicodedata
import time
from admin_db_info import get_current_mysql_password

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
    database="ebookingclass"
)
cursor = conn.cursor()

def login_main():
    """Fungsi utama untuk memilih peran dan login."""
    from main_menu import mahasiswa_menu, admin_menu

    while True:
        print("\n=== Pilih Peran untuk Login ===")
        print("1. Login sebagai Mahasiswa")
        print("2. Login sebagai Admin")
        print("0. Kembali")
        role_choice = input("Masukkan pilihan (1/2/0): ").strip()

        if role_choice == '0':
            print("\n=== Sistem E-Booking Class ===")
            print("1. Login")
            print("2. Register")
            print("3. Keluar")
            return  # Kembali ke menu utama
        elif role_choice in ['1', '2']:
            role = 'mahasiswa' if role_choice == '1' else 'admin'
            login_by_role(role, mahasiswa_menu, admin_menu)
        else:
            print("Pilihan tidak valid! Silakan pilih 1 untuk Mahasiswa, 2 untuk Admin, atau 0 untuk kembali.")

def login_by_role(role, mahasiswa_menu, admin_menu):
    """
    Fungsi login berdasarkan peran (mahasiswa atau admin).
    
    Args:
        role (str): Peran login ('mahasiswa' atau 'admin').
        mahasiswa_menu (function): Fungsi untuk menu mahasiswa.
        admin_menu (function): Fungsi untuk menu admin.
    """
    attempts = 0  # Hitungan percobaan login

    while attempts < 3:
        print(f"\nAnda memilih untuk login sebagai {role.capitalize()}.")
        nim = input("Masukkan NIM ('0' untuk kembali): ").lower()
        if nim == '0':
            print("Kembali ke menu pilih peran...")
            return

        password = input("Masukkan Password: ").strip()

        # Normalisasi password
        password = unicodedata.normalize("NFKC", password).strip()

        # Check NIM di database dengan parameterized query untuk mencegah SQL injection
        cursor.execute("SELECT nim, email, password, user_role FROM users WHERE nim = %s", (nim,))
        result = cursor.fetchone()

        if result is None:
            print("Login gagal! NIM atau password salah.")
        else:
            nim_db, email, hashed_password, user_role = result
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                if user_role == role:
                    print(f"Login berhasil sebagai {role.capitalize()}.")

                    # Arahkan ke menu berdasarkan peran
                    if role == 'mahasiswa':
                        mahasiswa_menu(nim_db, email)
                    elif role == 'admin':
                        admin_menu()
                    return
                else:
                    print("Login gagal! NIM atau password salah.")
            else:
                print("Login gagal! NIM atau password salah.")

        attempts += 1
        if attempts < 3:
            print(f"Sisa percobaan login: {3 - attempts}")
        else:
            print("Terlalu banyak percobaan gagal. Program akan pending selama 30 detik.")
            time.sleep(30)  # Menunggu selama 30 detik setelah 3 kali gagal

# Tutup koneksi database setelah login selesai
def close_connection():
    cursor.close()
    conn.close()

# Panggil fungsi utama jika dijalankan langsung
if __name__ == "__main__":
    try:
        login_main()
    finally:
        close_connection()

