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
    # Pilihan untuk login sebagai admin atau mahasiswa
    print("\n=== Pilih Peran untuk Login ===")
    print("1. Login sebagai Mahasiswa")
    print("2. Login sebagai Admin")
    role_choice = input("Masukkan pilihan (1/2): ").strip()
    
    if role_choice == '1':
        role = 'mahasiswa'
        login_by_role(role)
    elif role_choice == '2':
        role = 'admin'
        login_by_role(role)
    else:
        print("Pilihan tidak valid! Silakan pilih 1 untuk Mahasiswa atau 2 untuk Admin.")

    print("Login gagal setelah 3 kali percobaan.")

# FUNGSI BIAR ATTEMPT LOGIN NYA BEDA DI MASING2 ROLE
def login_by_role(role):
    from main_menu import admin_menu, mahasiswa_menu

    attempts = 0  # Hitungan percobaan login
    
    while attempts < 3:  # Memberikan 3 kali kesempatan login
        print(f"Anda memilih untuk login sebagai {role.capitalize()}.")

        # Masukkan NIM dan password sesuai dengan role yang dipilih
        nim = input("Masukkan NIM: ").lower()
        password = input("Masukkan Password: ").strip()

        # Normalisasi password
        password = unicodedata.normalize("NFKC", password).strip()

        # Check NIM di database dengan parameterized query untuk mencegah SQL injection
        cursor.execute("SELECT nim, email, password, user_role FROM users WHERE nim = %s", (nim,))
        result = cursor.fetchone()
        if result is None:
            print("Login gagal! NIM atau password salah.")
            attempts += 1
            if attempts < 3:
                print(f"Sisa percobaan login: {3 - attempts}")
            else:
                print("Terlalu banyak percobaan gagal. Program akan pending selama 30 detik.")
                time.sleep(30)  # Menunggu selama 30 detik setelah 3 kali gagal
        else:
            nim, email, hashed_password, user_role = result
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                if user_role == role:
                    print(f"Login berhasil sebagai {role.capitalize()}.")

                    # Menjaga koneksi tetap terbuka dan mengarahkan ke menu yang tepat
                    if role == 'mahasiswa':
                        print("Masuk ke menu mahasiswa...")
                        cursor.close()
                        conn.close()
                        mahasiswa_menu(nim, email)  # Memanggil mahasiswa_menu dengan nim dan email
                        return  # Keluar dari login setelah berhasil masuk ke menu mahasiswa
                    else:
                        print("Masuk ke menu admin...")
                        cursor.close()
                        conn.close()
                        admin_menu()  # Panggil fungsi admin_menu() atau yang sesuai jika login sebagai admin
                        return  # Keluar dari login setelah berhasil masuk ke menu admin
                else:
                    print(f"Login gagal! NIM atau password salah.")
            else:
                print("Login gagal! NIM atau password salah.")
            attempts += 1