import mysql.connector
import os
from main_features_admin import add_mata_kuliah, view_dosen, view_datakelas, proses_pengajuan_kelas, input_jadwal_dosen, buat_kelas, edit_jadwal_dosen, view_jadwal_dosen, tampilkan_kelas, add_ruang_kelas, add_dosen, view_mata_kuliah,edit_kelas
from main_features_mhs import ajukan_kelas, lihat_pesanan_saya
from register import register_user
from login import login
from admin_db_info import get_current_mysql_password

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
    database="ebookingclass"
)
cursor = conn.cursor()

# global variable untuk kredensial user
nim = ""
email = ""
role = ""

# Menu untuk admin
def admin_menu():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Lihat Pengajuan Kelas")
        print("2. Lihat Pengajuan Pembatalan Kelas")
        print("2. Tambah Mata Kuliah")
        print("3. Lihat Data Mata Kuliah")
        print("4. Tambah Data Dosen")
        print("5. Lihat Data Dosen")
        print("6. Input Jadwal Kosong Dosen")
        print("7. Lihat Jadwal Kosong Seluruh Dosen")
        print("8. Edit Jadwal Kosong Dosen")
        print("9. Tambah Ruang Kelas")
        print("10. Lihat Data Ruang Kelas")
        print("11. Buat Kelas Baru")
        print("12. Edit Kelas")
        print("13. Lihat Kelas yang Telah Dibuat")
        print("14. Logout")
        
        choice = input("Pilih menu: ").strip()

        if choice == '1':
            proses_pengajuan_kelas()
        elif choice == '2':
            add_mata_kuliah()
        elif choice == '3':
            view_mata_kuliah()
        elif choice == '4':
            add_dosen()
        elif choice == '5':
            view_dosen()
        elif choice == '6':
            input_jadwal_dosen()
        elif choice == '7':
            view_jadwal_dosen()
        elif choice == '8':
            edit_jadwal_dosen()
        elif choice == '9':
            add_ruang_kelas()
        elif choice == '10':
            view_datakelas()
        elif choice == '11':
            buat_kelas()
        elif choice == '12':
            edit_kelas()
        elif choice == '13':
            tampilkan_kelas()
        elif choice == '14':
            print("Logout berhasil! Sampai jumpa lagi.")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih menu dari 1 sampai 14.")

# Menu untuk mahasiswa
def mahasiswa_menu():
    while True:
        print("\n=== Menu Mahasiswa ===")
        print("1. Lihat Kelas")
        print("2. Ajukan Kelas")
        print("3. Lihat Profil (maintenance)")
        print("4. Lihat Pesanan Saya")
        print("5. Logout")
        
        choice = input("Pilih menu: ").strip()

        if choice == '1':
            tampilkan_kelas()
        elif choice == '2':
            ajukan_kelas(nim=nim, email=email)
        elif choice == '4':
            lihat_pesanan_saya(NIM=nim)
        elif choice == '5':
            print("Logout berhasil!")
            break
        else:
            print("Pilihan tidak valid!")

# Main program
def main():
    
    os.system('cls')
    
    # Ambil variabel global kredensial pengguna
    global nim
    global email
    global role

    while True:
        print("\n=== Sistem E-Booking Class ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        
        choice = input("Pilih menu: ").strip()

        if choice == '1':
            result = login()
            
            # Masukkin ke dalem global variable kalau login nya berhasil
            if (result != None):
                # Ambil kredensial dari hasil percobaan login
                user_nim = result[0]
                user_email = result[1]
                user_role = result[3]

                # Simpan value hasil login ke dalam global variabel kredensial
                nim = user_nim
                email = user_email
                role = user_role
            
                if user_role == 'admin':
                    admin_menu()  # Arahkan ke menu admin setelah login admin
                elif user_role == 'mahasiswa':
                    mahasiswa_menu()  # Arahkan ke menu mahasiswa setelah login mahasiswa
                else:
                    print("Role tidak ditemukan!")
        elif choice == '2':
            register_user()
        elif choice == '3':
            print("Terima kasih telah menggunakan program ini.")
            break
        else:
            print("Pilihan tidak valid!")

# Jalankan program utama
main()

# Tutup koneksi
cursor.close()
conn.close()
