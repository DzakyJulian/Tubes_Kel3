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
        print("\n=== Menu Admin ===")
        print("1. Lihat Pengajuan Kelas")
        print("2. Lihat Pengajuan Pembatalan Kelas")
        print("3. Tambah Mata Kuliah")
        print("4. Lihat Data Mata Kuliah")
        print("5. Tambah Data Dosen")
        print("6. Lihat Data Dosen")
        print("7. Input Jadwal Kosong Dosen")
        print("8. Lihat Jadwal Kosong Seluruh Dosen")
        print("9. Edit Jadwal Kosong Dosen")
        print("10. Tambah Ruang Kelas")
        print("11. Lihat Data Ruang Kelas")
        print("12. Buat Kelas Baru")
        print("13. Edit Kelas")
        print("14. Lihat Kelas yang Telah Dibuat")
        print("15. Logout")
        
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
            print("Pilihan tidak valid! Silakan pilih menu dari 1 sampai 14.")

def mahasiswa_menu(nim, email):
    while True:
        print("\n=== Menu Mahasiswa ===")
        print("1. Lihat Kelas")
        print("2. Ajukan Kelas")
        print("3. Lihat Profil (maintenance)")
        print("4. Lihat Pesanan Saya")
        print("5. Batalkan Kelas")
        print("6. Logout")
        
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
        print("\n=== Sistem E-Booking Class ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        
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
