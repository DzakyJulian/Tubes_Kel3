import mysql.connector
from main_features_admin import (
    add_mata_kuliah, proses_pembatalan_kelas_admin, view_dosen, view_datakelas, proses_pengajuan_kelas,
    input_jadwal_dosen, buat_kelas, edit_jadwal_dosen, view_jadwal_dosen,
    tampilkan_kelas, add_ruang_kelas, add_dosen, view_mata_kuliah, edit_kelas
)
from main_features_mhs import ajukan_kelas, lihat_pesanan_saya, batal_kelas
from register import register_user
from login import login_main
from admin_db_info import get_current_mysql_password
from prettytable import PrettyTable

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
    database="ebookingclass"
)
cursor = conn.cursor()

# Menu untuk admin
def admin_menu():
    while True:

        table = PrettyTable()
        table.field_names = ["No", "Menu Admin"]
        table.add_row([1, "Lihat Pengajuan Kelas"])
        table.add_row([2, "Lihat Pengajuan Pembatalan Kelas"])
        table.add_row([3, "Tambah Mata Kuliah"])
        table.add_row([4, "Lihat Data Mata Kuliah"])
        table.add_row([5, "Tambah Data Dosen"])
        table.add_row([6, "Lihat Data Dosen"])
        table.add_row([7, "Input Jadwal Kosong Dosen"])
        table.add_row([8, "Lihat Jadwal Kosong Seluruh Dosen"])
        table.add_row([9, "Edit Jadwal Kosong Dosen"])
        table.add_row([10, "Tambah Ruang Kelas"])
        table.add_row([11, "Lihat Data Ruang Kelas"])
        table.add_row([12, "Buat Kelas Baru"])
        table.add_row([13, "Edit Kelas"])
        table.add_row([14, "Lihat Kelas yang Telah Dibuat"])
        table.add_row([15, "Logout"])
        print(table)
        
        choice = input("Pilih menu: ").strip()

        if choice == '1':
            proses_pengajuan_kelas()
        elif choice == '2':
            proses_pembatalan_kelas_admin()
        elif choice == '3':
            add_mata_kuliah()
        elif choice == '4':
            view_mata_kuliah()
        elif choice == '5':
            add_dosen()
        elif choice == '6':
            view_dosen()
        elif choice == '7':
            input_jadwal_dosen()
        elif choice == '8':
            view_jadwal_dosen()
        elif choice == '9':
            edit_jadwal_dosen()
        elif choice == '10':
            add_ruang_kelas()
        elif choice == '11':
            view_datakelas()
        elif choice == '12':
            buat_kelas()
        elif choice == '13':
            edit_kelas()
        elif choice == '14':
            tampilkan_kelas()
        elif choice == '15':
            print("Logout berhasil! Sampai jumpa lagi.")
            break  # Keluar dari menu admin setelah logout
        else:
            print("Pilihan tidak valid! Silakan pilih menu dari 1 sampai 15.")

def mahasiswa_menu(nim, email):
    while True:
        table = PrettyTable()
        table.field_names = ["No", "Menu Mahasiswa"]
        table.add_row([1, "Lihat Kelas"])
        table.add_row([2, "Ajukan Kelas"])
        table.add_row([3, "Lihat Profil (maintenance)"])
        table.add_row([4, "Lihat Pesanan Saya"])
        table.add_row([5, "Batalkan Kelas"])
        table.add_row([6, "Logout"])
        print(table)
        
        pilihan = input("\nMasukkan pilihan (1-6): ").strip()

        if pilihan == '1':
            tampilkan_kelas()
        elif pilihan == '2':
            ajukan_kelas(nim, email)
        elif pilihan == '4':
            lihat_pesanan_saya(nim)
        elif pilihan == '5':
            batal_kelas(nim)  # Memanggil fungsi untuk membatalkan kelas
        elif pilihan == '6':
            print("Anda telah logout.")
            break  # Keluar dari menu mahasiswa setelah logout
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def main():
    while True:
        table = PrettyTable()
        table.field_names = ["No", "Sistem E-Booking Class"]
        table.add_row([1, "Login"])
        table.add_row([2, "Register"])
        table.add_row([3, "Keluar"])
        print(table)
    
        choice = input("Pilih menu: ").strip()

        if choice == '1':
            # Pilihan login
            result = login_main()  # Memanggil fungsi login

            if result is not None:
                user_nim, user_email, _, user_role = result
                # Menampilkan menu sesuai dengan peran
                if user_role == 'admin':
                    admin_menu(user_nim, user_email)  # Menu admin
                elif user_role == 'mahasiswa':
                    mahasiswa_menu(user_nim, user_email)  # Menu mahasiswa
                else:
                    print("Role tidak ditemukan!")
                    continue  # Kembali ke menu login jika role tidak ditemukan

        elif choice == '2':
            register_user()  # Fungsi untuk register user
        elif choice == '3':
            print("Terima kasih telah menggunakan program ini.")
            break  # Ini akan keluar dari program
        else:
            print("Pilihan tidak valid!")

# Jalankan program utama
if __name__ == "__main__":
    main()

# Tutup koneksi
cursor.close()
conn.close()
