import mysql.connector
import re
from datetime import datetime
from admin_db_info import get_current_mysql_password
from enum import Enum
from prettytable import PrettyTable


# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
    database="ebookingclass"
)

def add_ruang_kelas():
    cursor = conn.cursor()
    print("\n=== Tambah Ruang Kelas ===")
    print("Tekan Enter pada kolom 'Kode Kelas' jika ingin berhenti.\n")
    
    try:
        while True:
            # Input kode kelas dan informasi ruang kelas
            kode_kelas = input("Masukkan Kode Kelas: ").strip()
            if not kode_kelas:  # Hentikan jika input kosong
                print("Proses penambahan ruang kelas selesai.\n")
                break
            
            informasi_kelas = input("Masukkan Informasi Kelas: ").strip()
            
            # Menambahkan data ke tabel kelas
            query = "INSERT INTO kelas (kode_kelas, informasi_kelas) VALUES (%s, %s)"
            cursor.execute(query, (kode_kelas, informasi_kelas))
            conn.commit()
            print(f"Ruang kelas '{kode_kelas}' berhasil ditambahkan!\n")
    
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

# Fungsi tambahan untuk admin
def add_mata_kuliah():
    cursor = conn.cursor()
    print("\n=== Tambah Mata Kuliah ===")
    
    try:
        while True:
            kode_matkul = input("Masukkan Kode Mata Kuliah Baru (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not kode_matkul:  
                print("Kode mata kuliah tidak boleh kosong. Silakan ulangi.")
                continue
            elif kode_matkul == '0':
                print("Kembali ke menu utama...")
                return

            cursor.execute("SELECT (kode_matkul) FROM mata_kuliah WHERE kode_matkul = %s", (kode_matkul.upper(),))
            cek_matkul = cursor.fetchone()

            if cek_matkul:
                print(f"Kode mata kuliah '{kode_matkul}/{kode_matkul.upper()}' sudah ada. Silakan gunakan kode yang lain.")
                continue
            else:
                break

        while True:   
            nama_matkul = input("Masukkan Nama Mata Kuliah Baru (Ketik '0' untuk kembali ke Menu utama): ").strip()
            if not nama_matkul:  # Validasi nama mata kuliah kosong
                print("Nama mata kuliah tidak boleh kosong. Silakan ulangi.")
                continue
            elif nama_matkul == '0':
                print("Kembali ke menu utama...")
                return
            else:
                break
            
        # Insert data ke database
        cursor.execute("INSERT INTO mata_kuliah (kode_matkul, nama_matkul) VALUES (%s, %s)", (kode_matkul.upper(), nama_matkul.capitalize()))
        conn.commit()
        print(f"Mata kuliah {nama_matkul} berhasil ditambahkan!\n")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def view_mata_kuliah():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT kode_matkul, nama_matkul FROM mata_kuliah")
        matkul = cursor.fetchall()
        if matkul:
            print("\n=== Data Mata Kuliah ===")
            for mk in matkul:
                print("-" * 30)
                print(f"Kode Mata Kuliah: {mk[0]}")
                print(f"Nama Mata Kuliah: {mk[1]}")
                print("-" * 30)
        else:
            print("Tidak ada data mata kuliah.")
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def edit_mata_kuliah():
    cursor = conn.cursor()
    print("\n=== Edit Mata Kuliah ===")

    try:
        # Tampilkan data mata kuliah yang sudah ada
        cursor.execute("SELECT kode_matkul, nama_matkul FROM mata_kuliah ORDER BY kode_matkul")
        mata_kuliah_list = cursor.fetchall()

        if mata_kuliah_list:
            print("\nMata Kuliah yang Tersedia:")
            print("-" * 40)
            print(f"{'Kode Mata Kuliah':<15} {'Nama Mata Kuliah':<20}")
            print("-" * 40)
            for kode, nama in mata_kuliah_list:
                print(f"{kode:<15} {nama:<20}")
            print("-" * 40)
        else:
            print("\nBelum ada mata kuliah yang terdaftar.")

        while True:
            kode_matkul = input("Masukkan Kode Mata Kuliah yang akan diedit (tekan Enter untuk kembali): ").strip()
            if not kode_matkul:  # Jika input kosong, berhenti
                break

            try:
                # Periksa apakah kode mata kuliah ada di database
                cursor.execute("SELECT nama_matkul FROM mata_kuliah WHERE kode_matkul = %s", (kode_matkul.upper(),))
                mata_kuliah = cursor.fetchone()

                if not mata_kuliah:
                    print("Kode mata kuliah tidak ditemukan. Silakan coba lagi.")
                    continue

                print(f"Mata kuliah saat ini: {mata_kuliah[0]}")

                # Input kode mata kuliah baru
                while True:
                    kode_baru = input("Masukkan Kode Mata Kuliah Baru (tekan Enter untuk tidak mengubah): ").strip().upper()

                    if not kode_baru:
                        break  # Tidak mengubah kode

                    # Periksa apakah kode baru sudah digunakan
                    cursor.execute("SELECT kode_matkul FROM mata_kuliah WHERE kode_matkul = %s", (kode_baru,))
                    if cursor.fetchone():
                        print("Kode mata kuliah baru sudah digunakan. Silakan coba lagi.")
                    else:
                        break

                # Input nama mata kuliah baru
                nama_baru = input("Masukkan Nama Mata Kuliah Baru (tekan Enter untuk tidak mengubah): ").strip()

                # Update data di database
                if kode_baru:
                    cursor.execute("UPDATE mata_kuliah SET kode_matkul = %s WHERE kode_matkul = %s", (kode_baru, kode_matkul.upper()))
                    kode_matkul = kode_baru  # Perbarui kode untuk proses berikutnya

                if nama_baru:
                    cursor.execute("UPDATE mata_kuliah SET nama_matkul = %s WHERE kode_matkul = %s", (nama_baru.capitalize(), kode_matkul.upper()))

                conn.commit()
                print(f"Mata kuliah dengan kode {kode_matkul.upper()} berhasil diperbarui!\n")

            except mysql.connector.Error as err:
                print(f"Terjadi kesalahan: {err}")

    except mysql.connector.Error as err:
            print(f"Terjadi kesalahan: {err}")
    print("Proses pengeditan mata kuliah selesai.")

    cursor.close()

def delete_mata_kuliah():
    cursor = conn.cursor()
    print("\n=== Hapus Mata Kuliah ===")

    try:
        # Tampilkan data mata kuliah yang sudah ada
        cursor.execute("SELECT kode_matkul, nama_matkul FROM mata_kuliah ORDER BY kode_matkul")
        mata_kuliah_list = cursor.fetchall()

        if mata_kuliah_list:
            print("\nMata Kuliah yang Tersedia:")
            print("-" * 40)
            print(f"{'Kode Mata Kuliah':<15} {'Nama Mata Kuliah':<20}")
            print("-" * 40)
            for kode, nama in mata_kuliah_list:
                print(f"{kode:<15} {nama:<20}")
            print("-" * 40)
        else:
            print("\nBelum ada mata kuliah yang terdaftar.")
            return

        while True:
            kode_matkul = input("Masukkan Kode Mata Kuliah yang akan dihapus (tekan Enter untuk kembali): ").strip()
            if not kode_matkul:  # Jika input kosong, berhenti
                break

            # Periksa apakah kode mata kuliah ada di database
            cursor.execute("SELECT nama_matkul FROM mata_kuliah WHERE kode_matkul = %s", (kode_matkul.upper(),))
            mata_kuliah = cursor.fetchone()

            if not mata_kuliah:
                print("Kode mata kuliah tidak ditemukan. Silakan coba lagi.")
                continue
        
            while True:
                # Konfirmasi penghapusan
                konfirmasi = input(f"Apakah Anda yakin ingin menghapus mata kuliah '{mata_kuliah[0]}'? ('Y'/ 'N'): ").strip().upper()
                if konfirmasi == 'Y':
                    cursor.execute("DELETE FROM mata_kuliah WHERE kode_matkul = %s", (kode_matkul.upper(),))
                    conn.commit()
                    print(f"Mata kuliah dengan kode {kode_matkul.upper()} berhasil dihapus!\n")
                    return
                elif konfirmasi == 'N':
                    print("Penghapusan dibatalkan.")
                    return
                else:
                    print("Input tidak valid. Silakan coba lagi.")
                    continue

        print("Proses penghapusan mata kuliah selesai.")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def add_dosen():
    cursor = conn.cursor()
    print("\n=== Tambah Data Dosen ===")
    print("Tekan Enter pada 'Kode Dosen' jika ingin berhenti.\n")
    
    try:
        while True:
            # Input Kode Dosen
            kode_dosen = input("Masukkan Kode Dosen (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not kode_dosen:  # Hentikan jika input kosong
                print("Kode Dosen tidak boleh kosong!\n")
                continue
            elif kode_dosen == '0':
                print("Kembali ke menu utama...")
                return
            
            cursor.execute("SELECT * FROM dosen WHERE kode_dosen = %s", (kode_dosen,))
            dosen = cursor.fetchone()

            if dosen:
                print(f"kode_dosen '{kode_dosen}' sudah terdaftar. Silakan masukkan kode_dosen yang berbeda.")
                continue
            else:
                break

        while True:
            # Input data lainnya
            nama = input("Masukkan Nama Dosen (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not nama:
                print("Nama dosen tidak boleh kosong.")
                continue
            elif nama == '0':
                print("Kembali ke menu utama...")
                return
            else:
                break

        while True:
            alamat = input("Masukkan Alamat Dosen (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not alamat:
                print("Alamat dosen tidak boleh kosong.")
                continue
            elif alamat == '0':
                print("Kembali ke menu utama...")
                return
            else:
                break

        # Validasi email
        while True:
            email = input("Masukkan Email Dosen (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not email:
                print("Email tidak boleh kosong.")
                continue
            elif email == '0':
                print("Kembali ke menu utama...")
                return
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Email tidak valid. Harap periksa format email Anda.")
                continue
            else:
                break

        # Validasi nomor telepon
        while True:
            no_telp = input("Masukkan No. Telepon Dosen (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not no_telp:
                print("No. telepon tidak boleh kosong.")
                continue
            elif no_telp == '0':
                print("Kembali ke menu utama...")
                return
            elif not re.match(r"^\d{10,15}$", no_telp):
                print("No. telepon tidak valid. Harap masukkan no. telepon yang benar (10-15 digit).")
                continue
            else:
                break

        # Query untuk menambahkan data ke tabel dosen
        query = """
        INSERT INTO dosen (kode_dosen, nama, alamat, email, no_tlp)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (kode_dosen, nama, alamat, email, no_telp))
        conn.commit()
        print(f"Data dosen dengan kode_dosen '{kode_dosen}' berhasil ditambahkan!\n")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def view_dosen():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dosen")
        dosens = cursor.fetchall()
        if dosens:
            table = PrettyTable()
            table.field_names = ["kode_dosen", "Nama", "Alamat", "Email", "No. Telp"]

            for dosen in dosens:
                table.add_row([dosen[0], dosen[1], dosen[2], dosen[3], dosen[4]])
            print(table)
        else:
            print("Tidak ada data dosen.")
            
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat mengambil data dosen: {err}")
    finally:
        cursor.close()

def edit_dosen():
    cursor = conn.cursor()
    print("\n=== Edit Data Dosen ===")

    try:
        cursor.execute("SELECT * FROM dosen")
        dosens = cursor.fetchall()
        if dosens:
            table = PrettyTable()
            table.field_names = ["kode_dosen", "Nama", "Alamat", "Email", "No. Telp"]

            for dosen in dosens:
                table.add_row([dosen[0], dosen[1], dosen[2], dosen[3], dosen[4]])
            print(table)
        else:
            print("Tidak ada data dosen.")
            
        while True:
            kode_dosen = input("Masukkan kode_dosen Dosen yang ingin diubah (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not kode_dosen:
                print("kode_dosen Dosen tidak boleh kosong!")
                continue
            elif kode_dosen == '0':
                print("Kembali ke menu utama...")
                return

            cursor.execute("SELECT * FROM dosen WHERE kode_dosen = %s", (kode_dosen,))
            dosen = cursor.fetchone()

            if not dosen:
                print(f"Dosen dengan kode_dosen '{kode_dosen}' tidak ditemukan. Silakan masukkan kode_dosen yang valid.")
                continue
            else:
                break

        print("Tekan Enter jika tidak ingin mengubah data pada kolom tertentu.")

        while True:
            kode_dosen_baru = input(f"Masukkan kode_dosen Baru (Saat ini: {dosen[0]}): ").strip() or dosen[0]
            if kode_dosen_baru != dosen[0]:
                cursor.execute("SELECT * FROM dosen WHERE kode_dosen = %s", (kode_dosen_baru,))
                if cursor.fetchone():
                    print(f"kode_dosen '{kode_dosen_baru}' sudah terdaftar. Silakan masukkan kode_dosen yang berbeda.")
                    continue
            break

        nama = input(f"Masukkan Nama Baru (Saat ini: {dosen[1]}): ").strip() or dosen[1]
        alamat = input(f"Masukkan Alamat Baru (Saat ini: {dosen[2]}): ").strip() or dosen[2]

        while True:
            email = input(f"Masukkan Email Baru (Saat ini: {dosen[3]}): ").strip() or dosen[3]
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Email tidak valid. Harap periksa format email Anda.")
                continue
            else:
                break

        while True:
            no_telp = input(f"Masukkan No. Telepon Baru (Saat ini: {dosen[4]}): ").strip() or dosen[4]
            if not re.match(r"^\d{10,15}$", no_telp):
                print("No. telepon tidak valid. Harap masukkan no. telepon yang benar (10-15 digit).")
                continue
            else:
                break

        query = """
        UPDATE dosen
        SET nama = %s, alamat = %s, email = %s, no_tlp = %s
        WHERE kode_dosen = %s
        """
        cursor.execute(query, (nama, alamat, email, no_telp, kode_dosen))
        conn.commit()
        print(f"Data dosen dengan kode dosen '{kode_dosen}' berhasil diperbarui!\n")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def hapus_dosen():
    cursor = conn.cursor()
    print("\n=== Hapus Data Dosen ===")
    try:
        while True:
            kode_dosen = input("Masukkan Kode Dosen yang ingin dihapus (Ketik '0' untuk kembali ke menu utama): ").strip()
            if not kode_dosen:
                print("Kode Dosen tidak boleh kosong!")
                continue
            elif kode_dosen == '0':
                print("Kembali ke menu utama...")
                return

            cursor.execute("SELECT * FROM dosen WHERE kode_dosen = %s", (kode_dosen,))
            dosen = cursor.fetchone()

            if not dosen:
                print(f"Dosen dengan kode dosen '{kode_dosen}' tidak ditemukan. Silakan masukkan kode_dosen yang valid.")
                continue
            else:
                konfirmasi = input(f"Apakah Anda yakin ingin menghapus data dosen dengan kode dosen '{kode_dosen}'? (y/n): ").strip().lower()
                if konfirmasi == 'y':
                    cursor.execute("DELETE FROM dosen WHERE kode_dosen = %s", (kode_dosen,))
                    conn.commit()
                    print(f"Data dosen dengan kode dosen '{kode_dosen}' berhasil dihapus!\n")
                    break
                else:
                    print("Penghapusan dibatalkan.")
                    break

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

# Fungsi untuk input jadwal kosong dosen
def input_jadwal_dosen():
    cursor = conn.cursor()
    print("\n=== Input Jadwal Kosong Dosen ===")
    while True:
        kode_dosen = input("Masukkan Kode Dosen (Ketik '0' untuk kembali ke menu utama): ").strip()
        if kode_dosen == '0':
            print("Kembali ke menu utama.")
            return  # Keluar dari fungsi
        
        cursor.execute("SELECT kode_dosen FROM dosen WHERE kode_dosen = %s",(kode_dosen,))
        kode_dosen_result = cursor.fetchone()
        
        if kode_dosen_result is None:
            print("Dosen dengan kode dosen tersebut tidak ditemukan. Silakan mencoba lagi.")
            continue
        
        kode_dosen = kode_dosen_result[0]  # Ambil nilai kode_dosen dari tuple
        
        try:
            while True:
                print("\nKetik '0' untuk kembali tanpa menyimpan.")
                hari = input("Masukkan hari (contoh: Senin): ").strip()
                if hari == '0':
                    print("Proses dibatalkan. Kembali ke input kode dosen.")
                    break  # Kembali ke input kode dosen
                if hari.capitalize() not in ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']:
                    print("Hari tidak valid!.")
                    continue

                if not hari:
                    print("Hari tidak boleh kosong!")
                    continue  # Minta input ulang jika hari kosong

                jam_mulai = input("Masukkan jam mulai (format 24 jam, contoh: 08:00): ").strip()
                if jam_mulai == '0':
                    print("Proses dibatalkan. Kembali ke input kode dosen.")
                    break
                jam_selesai = input("Masukkan jam selesai (format 24 jam, contoh: 12:00): ").strip()
                if jam_selesai == '0':
                    print("Proses dibatalkan. Kembali ke input kode dosen.")
                    break

                # Validasi agar jam mulai tidak lebih dari jam selesai
                if jam_mulai >= jam_selesai:
                    print("Jam mulai harus lebih awal daripada jam selesai.")
                    continue

                # Menyimpan jadwal dosen
                query = "INSERT INTO jadwal_dosen (kode_dosen, hari, jam_mulai, jam_selesai) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (kode_dosen, hari.capitalize(), jam_mulai, jam_selesai))
                conn.commit()  # Menyimpan data setelah setiap jadwal
                print("Jadwal kosong dosen berhasil ditambahkan.")

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            
def view_jadwal_dosen():
    cursor = conn.cursor()
    try:
        while True:
            table = PrettyTable()
            table.field_names = ["No", "Lihat Jadwal Kosong Dosen"]
            table.add_row([1, "Lihat semua jadwal dosen"])
            table.add_row([2, "Lihat jadwal berdasarkan kode dosen"])
            table.add_row([3, "Kembali ke menu utama"])
            print(table)
             
            choice = input("Pilih menu: ").strip()

            if choice == "1":  # Lihat semua jadwal dosen
                query = """
                SELECT jadwal_dosen.kode_dosen, dosen.nama, jadwal_dosen.hari, jadwal_dosen.jam_mulai, jadwal_dosen.jam_selesai
                FROM jadwal_dosen
                INNER JOIN dosen ON jadwal_dosen.kode_dosen = dosen.kode_dosen
                """
                cursor.execute(query)
                jadwal = cursor.fetchall()

                if jadwal:
                    print("\n=== Jadwal Kosong Seluruh Dosen ===")
                    table = PrettyTable()
                    table.field_names = ["Kode Dosen", "Nama Dosen", "Hari", "Jam Mulai", "Jam Selesai"]

                    for j in jadwal:
                        table.add_row([ 
                            j[0],  # kode Dosen
                            j[1],  # Nama Dosen
                            j[2],  # Hari
                            j[3],  # Jam Mulai
                            j[4]   # Jam Selesai
                        ])
                    print(table)    
                        
                else:
                    print("Tidak ada jadwal kosong dosen.")

            elif choice == "2":  # Lihat jadwal berdasarkan kode_dosen
                kode_dosen = input("Masukkan kode_dosen dosen: ").strip()
                query_dosen = "SELECT nama FROM dosen WHERE kode_dosen = %s"
                cursor.execute(query_dosen, (kode_dosen,))
                result_dosen = cursor.fetchone()

                if result_dosen:  # Jika dosen ditemukan
                    nama_dosen = result_dosen[0]
                    query_jadwal = """
                    SELECT jadwal_dosen.hari, jadwal_dosen.jam_mulai, jadwal_dosen.jam_selesai
                    FROM jadwal_dosen
                    WHERE kode_dosen = %s
                    """
                    cursor.execute(query_jadwal, (kode_dosen,))
                    jadwal_dosen = cursor.fetchall()

                    if jadwal_dosen:
                        print(f"\n=== Jadwal Kosong untuk Dosen kode dosen {kode_dosen} ({nama_dosen}) ===")
                        table = PrettyTable()
                        table.field_names = ["Hari", "Jam Mulai", "Jam Selesai"]
                        for j in jadwal_dosen:
                            table.add_row([
                                j[0],  # Hari
                                j[1],  # Jam Mulai
                                j[2]   # Jam Selesai
                            ])
                        print(table)    
                           
                    else:
                        print(f"Tidak ada jadwal kosong untuk dosen dengan kode dosen {kode_dosen} ({nama_dosen}).")
                else:
                    print(f"Dosen dengan kode dosen {kode_dosen} tidak ditemukan.")

            elif choice == "3":  # Kembali ke menu utama
                print("Kembali ke menu utama.")
                break

            else:
                print("Pilihan tidak valid! Silakan pilih 1, 2, atau 3.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cursor.close()

def edit_jadwal_dosen():
    cursor = conn.cursor()
    print("\n=== Edit Jadwal Kosong Dosen ===")
    kode_dosen = input("Masukkan Kode Dosen yang ingin diedit jadwalnya (Ketik '0' untuk kembali): ").strip()
    if kode_dosen == '0':
        print("Kembali ke menu utama.")
        return  # Keluar dari fungsi

    try:
        # Menampilkan jadwal yang ada untuk dosen tersebut
        cursor.execute("SELECT id, hari, jam_mulai, jam_selesai FROM jadwal_dosen WHERE kode_dosen = %s", (kode_dosen,))
        jadwal = cursor.fetchall()

        if not jadwal:
            print(f"Tidak ada jadwal kosong untuk dosen dengan kode_dosen {kode_dosen}.")
            return

        # Menampilkan jadwal yang ada
        print("\nJadwal Kosong yang Ada:")
        for j in jadwal:
            print(f"ID: {j[0]} - Hari: {j[1]} - Jam Mulai: {j[2]} - Jam Selesai: {j[3]}")

        # Memilih jadwal untuk diedit
        id_jadwal = input("\nMasukkan ID jadwal yang ingin diedit (Ketik '0' untuk kembali): ").strip()
        if id_jadwal == '0':
            print("Kembali ke menu sebelumnya.")
            return

        # Memeriksa apakah ID yang dimasukkan valid
        cursor.execute("SELECT * FROM jadwal_dosen WHERE id = %s", (id_jadwal,))
        jadwal_edit = cursor.fetchone()

        if not jadwal_edit:
            print(f"Jadwal dengan ID {id_jadwal} tidak ditemukan.")
            return

        # Mengedit data jadwal
        print("Masukkan data baru untuk jadwal ini. Ketik '0' untuk membatalkan.")
        hari_baru = input(f"Masukkan hari baru (sebelumnya {jadwal_edit[1]}): ").strip()
        if hari_baru == '0':
            print("Proses pembaruan dibatalkan.")
            return

        jam_mulai_baru = input(f"Masukkan jam mulai baru (sebelumnya {jadwal_edit[2]}): ").strip()
        if jam_mulai_baru == '0':
            print("Proses pembaruan dibatalkan.")
            return

        jam_selesai_baru = input(f"Masukkan jam selesai baru (sebelumnya {jadwal_edit[3]}): ").strip()
        if jam_selesai_baru == '0':
            print("Proses pembaruan dibatalkan.")
            return

        # Update jadwal dosen
        update_query = '''UPDATE jadwal_dosen
                          SET hari = %s, jam_mulai = %s, jam_selesai = %s
                          WHERE id = %s'''
        cursor.execute(update_query, (hari_baru, jam_mulai_baru, jam_selesai_baru, id_jadwal))
        conn.commit()

        print("Jadwal dosen berhasil diperbarui.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        cursor.close()

def hapus_jadwal_dosen():
    cursor = conn.cursor()
    print("\n=== Hapus Jadwal Kosong Dosen ===")
    while True:
        kode_dosen = input("Masukkan Kode Dosen (Ketik '0' untuk kembali ke menu utama): ").strip()
        if kode_dosen == '0':
            print("Kembali ke menu utama.")
            return

        cursor.execute("SELECT kode_dosen FROM dosen WHERE kode_dosen = %s", (kode_dosen,))
        if cursor.fetchone() is None:
            print("Dosen dengan kode dosen tersebut tidak ditemukan. Silakan mencoba lagi.")
            continue

        cursor.execute("SELECT id, hari, jam_mulai, jam_selesai FROM jadwal_dosen WHERE kode_dosen = %s", (kode_dosen,))
        jadwal = cursor.fetchall()

        if not jadwal:
            print("Dosen tidak memiliki jadwal kosong yang tercatat.")
            continue

        print("\nJadwal kosong yang tersedia:")
        for i in range(len(jadwal)):
            id_jadwal, hari, jam_mulai, jam_selesai = jadwal[i]
            print(f"{i + 1}. Hari: {hari}, Jam: {jam_mulai} - {jam_selesai} (ID: {id_jadwal})")

        pilihan = input("Masukkan nomor atau ID jadwal yang ingin dihapus (Ketik '0' untuk kembali): ").strip()
        if pilihan == '0':
            print("Proses dibatalkan.")
            break

        try:
            id_jadwal = int(pilihan) if pilihan.isdigit() else None
            if id_jadwal not in [jadwal[j][0] for j in range(len(jadwal))]:
                print("Pilihan tidak valid. Silakan coba lagi.")
                continue

            cursor.execute("DELETE FROM jadwal_dosen WHERE id = %s", (id_jadwal,))
            conn.commit()
            print("Jadwal berhasil dihapus.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

# Fungsi untuk membuat kelas berdasarkan jadwal kosong dosen
def buat_kelas():
    cursor = conn.cursor()
    print("\n=== Buat Kelas ===")

    # Memilih ruang kelas
    print("\nPilih Ruang Kelas:")
    cursor.execute("SELECT * FROM kelas")
    ruang_kelas = cursor.fetchall()

    if not ruang_kelas:
        print("Tidak ada ruang kelas yang tersedia!")
        return

    for ruang in ruang_kelas:
        print(f"Kode Kelas: {ruang[0]}, Informasi: {ruang[1]}")

    kode_kelas = input("\nPilih Kode Kelas untuk kelas: ").strip()

    # Menampilkan jadwal penggunaan ruang yang dipilih
    query = """
        SELECT kode_kelas, hari, jam_mulai, jam_selesai, pengguna FROM detail_kelas
        WHERE kode_kelas = %s
    """
    cursor.execute(query, (kode_kelas,))
    jadwal_ruang = cursor.fetchall()

    if jadwal_ruang:
        print("\nJadwal Penggunaan Ruang Kelas yang Dipilih:")
        for jadwal in jadwal_ruang:
            print("-" * 40)
            print(f"Kode Kelas: {jadwal[0]}, Hari: {jadwal[1]}, Jam: {jadwal[2]} - {jadwal[3]}, Pengguna: {jadwal[4]}")
            print("-" * 40)

    # Memilih dosen
    kode_dosen = input("Masukkan Kode Dosen: ").strip()

    try:
        # Ambil jadwal kosong dosen dan nama dosen dari database
        query = """
        SELECT jadwal_dosen.hari, jadwal_dosen.jam_mulai, jadwal_dosen.jam_selesai, dosen.nama
        FROM jadwal_dosen
        INNER JOIN dosen ON jadwal_dosen.kode_dosen = dosen.kode_dosen
        WHERE jadwal_dosen.kode_dosen = %s
        """
        cursor.execute(query, (kode_dosen,))
        jadwal_list = cursor.fetchall()

        if not jadwal_list:
            print("Tidak ada jadwal kosong untuk dosen ini!")
            return

        print("\nJadwal Kosong Dosen:")
        for jadwal in jadwal_list:
            print(f"Dosen: {jadwal[3]}, Hari: {jadwal[0]}, Jam: {jadwal[1]} - {jadwal[2]}")

        # Memilih mata kuliah
        view_mata_kuliah()
        kode_matkul = input("\nMasukkan Kode Mata Kuliah: ").strip()
        kategori_sks = input("Masukkan kategori SKS (4, 3, 2): ").strip()

        # Validasi kategori SKS
        if kategori_sks not in ['4', '3', '2']:
            print("Kategori SKS tidak valid! Pilih 4, 3, atau 2.")
            return

        durasi = int(kategori_sks) * 50  # Durasi dalam menit

        # Memasukkan waktu penggunaan manual
        while True:
            print("\nMasukkan Waktu Penggunaan Kelas:")
            hari = input("Masukkan Hari (contoh: Senin): ").strip()
            jam_mulai = input("Masukkan Jam Mulai (HH:MM, contoh: 08:00): ").strip()
            jam_selesai = input("Masukkan Jam Selesai (HH:MM, contoh: 10:00): ").strip()

            try:
                jam_mulai_dt = datetime.strptime(jam_mulai, "%H:%M")
                jam_selesai_dt = datetime.strptime(jam_selesai, "%H:%M")
            except ValueError:
                print("Format jam salah! Gunakan format HH:MM.")
                continue

                # Validasi logis: jam mulai harus lebih kecil dari jam selesai
            if jam_mulai_dt >= jam_selesai_dt:
                print("Jam mulai harus lebih kecil dari jam selesai. Silakan masukkan ulang.")
                continue

            # Validasi jadwal dosen dengan menggunakan BETWEEN
            query_dosen = """
                SELECT kode_dosen, hari, jam_mulai, jam_selesai
                FROM jadwal_dosen
                WHERE kode_dosen = %s AND hari = %s AND NOT ((%s BETWEEN jam_mulai AND jam_selesai) OR (%s BETWEEN jam_mulai AND jam_selesai))
            """
            cursor.execute(query_dosen, (kode_dosen, hari.capitalize(), jam_mulai_dt, jam_selesai_dt))
            jadwal_bentrok_dosen = cursor.fetchall()

            if jadwal_bentrok_dosen:
                print("\nWaktu yang Anda pilih di luar jadwal dosen!")
                print(f"\n===== Berikut jadwal dosen pada hari {hari.capitalize()} =====")
                for jadwal in jadwal_bentrok_dosen:
                    print(f"Dosen: {jadwal[0]}, Hari: {jadwal[1]}, Jam: {jadwal[2]} - {jadwal[3]}")
                continue
        
            # Validasi bentrok waktu kelas
            query = """
                SELECT kode_kelas, hari, jam_mulai, jam_selesai, pengguna FROM detail_kelas 
                WHERE kode_kelas = %s AND hari = %s AND ((%s BETWEEN jam_mulai AND jam_selesai) OR (%s BETWEEN jam_mulai AND jam_selesai))
            """
            cursor.execute(query, (kode_kelas, hari, jam_mulai, jam_selesai))
            kelas_bentrok = cursor.fetchall()

            if kelas_bentrok:
                print("\nJadwal yang Anda pilih bertabrakan dengan kelas lain!")
                for kelas in kelas_bentrok:
                    print(f"Kode Kelas: {kelas[0]}, Hari: {kelas[1]}, Jam: {kelas[2]} - {kelas[3]}, Pengguna: {kelas[4]}")
                continue
            else:
                break

        # Memasukkan pengguna kelas
        pengguna = input("\nPengguna kelas (contoh: RPL 1-C, kosongkan jika tidak ada pengguna): ").strip()
        status = 'Tersedia' if not pengguna else 'Digunakan'

        # Simpan data kelas ke database
        query = """
            INSERT INTO detail_kelas (kode_kelas, kode_matkul, hari, kode_dosen, jam_mulai, jam_selesai, pengguna, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (kode_kelas.upper(), kode_matkul.upper(), hari.capitalize(), kode_dosen, jam_mulai, jam_selesai, pengguna.upper(), status))
        conn.commit()
        print("Kelas berhasil dibuat.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def edit_kelas():
    cursor = conn.cursor()
    print("\n=== Edit Data Kelas ===")

    try:
        # Menampilkan daftar kelas
        query = "SELECT id_detail_kelas, kode_kelas, kode_matkul, kode_dosen, jam_mulai, jam_selesai, pengguna, status FROM detail_kelas"
        cursor.execute(query)
        kelas_list = cursor.fetchall()

        if not kelas_list:
            print("Tidak ada data kelas yang tersedia!")
            return

        print("\nDaftar Kelas:")
        for kelas in kelas_list:
            print("-" * 40)
            print(f"ID: {kelas[0]}\nKode Kelas: {kelas[1]}\nKode Mata Kuliah: {kelas[2]}\nKode Dosen: {kelas[3]}\nJam: {kelas[4]} - {kelas[5]}\nPengguna: {kelas[6]}\nStatus: {kelas[7]}")
            print("-" * 40)

        # Memilih kelas yang akan diedit
        kelas_id = input("\nMasukkan ID Kelas yang akan diedit (Ketik '0' untuk kembali): ").strip()
        if kelas_id == '0':
            return  # Kembali ke menu utama

        # Mengambil data kelas berdasarkan ID
        query = "SELECT id_detail_kelas, kode_kelas, kode_matkul, kode_dosen, hari, jam_mulai, jam_selesai, pengguna, status FROM detail_kelas WHERE id_detail_kelas = %s"
        cursor.execute(query, (kelas_id,))
        kelas = cursor.fetchone()

        if not kelas:
            print("Kelas dengan ID tersebut tidak ditemukan!")
            return

        print("\nData Kelas yang Dipilih:")
        print(f"ID: {kelas[0]}\nKode Kelas: {kelas[1]}\nKode Mata Kuliah: {kelas[2]}\nKode Dosen: {kelas[3]}\nHari: {kelas[4]}\nJam: {kelas[5]} - {kelas[6]}\nPengguna: {kelas[7]}\nStatus: {kelas[8]}")

        # Mengedit data kelas
        print("\nMasukkan data baru (kosongkan jika tidak ingin mengubah, ketik '0' untuk kembali):")
        kode_kelas_baru = input("Kode Kelas baru: ").strip()
        if kode_kelas_baru == '0':
            return
        kode_kelas_baru = kode_kelas_baru or kelas[1]

        kode_matkul_baru = input("Kode Mata Kuliah baru: ").strip()
        if kode_matkul_baru == '0':
            return
        kode_matkul_baru = kode_matkul_baru or kelas[2]

        kode_dosen_baru = input("Kode Dosen baru: ").strip()
        if kode_dosen_baru == '0':
            return
        kode_dosen_baru = kode_dosen_baru or kelas[3]

        hari_baru = input("Hari baru: ").strip()
        if hari_baru == '0':
            return
        hari_baru = hari_baru or kelas[4]

        jam_mulai_baru = input("Jam Mulai baru (HH:MM): ").strip()
        if jam_mulai_baru == '0':
            return
        jam_mulai_baru = jam_mulai_baru or kelas[5]

        jam_selesai_baru = input("Jam Selesai baru (HH:MM): ").strip()
        if jam_selesai_baru == '0':
            return
        jam_selesai_baru = jam_selesai_baru or kelas[6]

        pengguna_baru = input("Pengguna baru: ").strip()
        if pengguna_baru == '0':
            return
        pengguna_baru = pengguna_baru or kelas[7]

        status_baru = input("Status baru (kosongkan untuk tetap 'Digunakan'): ").strip()
        if status_baru == '0':
            return
        status_baru = status_baru or kelas[8]

        # Update data kelas di database
        query = """
            UPDATE detail_kelas
            SET kode_kelas = %s, kode_matkul = %s, kode_dosen = %s, hari = %s, jam_mulai = %s, jam_selesai = %s, pengguna = %s, status = %s
            WHERE id_detail_kelas = %s
        """
        cursor.execute(query, (kode_kelas_baru.upper(), kode_matkul_baru.upper(), kode_dosen_baru, hari_baru.capitalize(), jam_mulai_baru, jam_selesai_baru, pengguna_baru.upper(), status_baru, kelas_id))
        conn.commit()
        print("Data kelas berhasil diperbarui.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def tampilkan_kelas():
    try:
        cursor = conn.cursor()
        query = '''
        SELECT detail_kelas.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.kode_dosen, dosen.nama, detail_kelas.hari, detail_kelas.jam_mulai, 
        detail_kelas.jam_selesai, detail_kelas.informasi_kelas, detail_kelas.status, detail_kelas.pengguna FROM detail_kelas INNER JOIN dosen ON detail_kelas.kode_dosen = dosen.kode_dosen
        ORDER BY kode_kelas ASC
        '''
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            table = PrettyTable()
            table.field_names = ["ID Detail Kelas", "Kode Kelas", "Kode Mata Kuliah", "Kode Dosen", "Dosen yang Mengajar", "Waktu Mulai", "Waktu Selesai", "Informasi Kelas", "Pengguna", "Status"]
        
            for row in results:
                table.add_row([ 
                    row[0],  # ID Detail Kelas
                    row[1],  # Kode Kelas
                    row[2],  # Kode Mata Kuliah
                    row[3],  # Kode Dosen
                    row[4],  # Dosen yang Mengajar
                    row[5],  # Waktu Mulai
                    row[6],  # Waktu Selesai
                    row[7],  # Informasi Kelas
                    row[8],  # Status
                    row[9],  # Pengguna
                ])
        
            print("\n=== List Kelas ===")
            print(table)
            

        else:
            print("Tidak ada data di tabel detail_kelas.")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat mengambil data: {err}")

    finally:
        cursor.close()

def view_datakelas():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM kelas")
        kelas = cursor.fetchall()
        if kelas:
            print("\n=== Data Ruang Kelas ===")
            for k in kelas:
                print(f"Kode: {k[0]}, Informasi: {k[1]}")
        else:
            print("Tidak ada data kelas.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def proses_pengajuan_kelas():
    cursor = conn.cursor()
    try:
        # Ambil semua pengajuan yang tersedia
        cursor.execute(
            """
            SELECT transaksi.id_transaksi, transaksi.id_detail_kelas, detail_kelas.kode_kelas, transaksi.nim,
                   detail_kelas.kode_dosen, detail_kelas.hari, detail_kelas.jam_mulai, detail_kelas.jam_selesai,
                   transaksi.pengguna, transaksi.tanggal_transaksi, transaksi.status_transaksi
            FROM transaksi
            INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas
            WHERE status_transaksi = 'Pengajuan Pending'
            """)
        daftar_pengajuan = cursor.fetchall()  # Ambil semua hasil untuk mengosongkan buffer

        if not daftar_pengajuan:
            print("Tidak ada pengajuan yang tersedia.")
            return
    
        # Tampilkan daftar pengajuan
        if daftar_pengajuan:  # Jika ada data pengajuan
            print("\n=== Daftar Pengajuan ===")
            table = PrettyTable()
            table.field_names = ["ID Transaksi", "ID Detail Kelas", "NIM Pemesan", "Pengguna Kelas", "Tanggal Pengajuan", "Status Saat Ini"]
        
            for pengajuan in daftar_pengajuan:
                table.add_row([
                    pengajuan[0],  # ID Transaksi
                    pengajuan[1],  # ID Detail Kelas
                    pengajuan[3],  # NIM Pemesan
                    pengajuan[8],   # Pengguna Kelas
                    pengajuan[9],   # Tanggal Pengajuan
                    pengajuan[10],   # Status
                ])
        
            print(table)
        else:
            print("Tidak ada pengajuan yang ditemukan.")
    
        # Input ID pengajuan yang akan diproses
        while True:
            id_pesanan = input("Masukkan ID Pengajuan yang akan diproses (Tekan 'Enter' untuk kembali): ").strip()

            if id_pesanan == '':
                print("Kembali ke menu utama...")
                return  

            if not id_pesanan.isdigit(): # agar hanya menerima input angka
                print("ID Transaksi harus berupa angka. Silakan coba lagi.")
                continue

            # Periksa apakah ID Pengajuan valid
            cursor.execute(
                """
                SELECT transaksi.id_transaksi, transaksi.id_detail_kelas, detail_kelas.kode_kelas, transaksi.nim,
                       detail_kelas.kode_dosen, detail_kelas.hari, detail_kelas.jam_mulai, detail_kelas.jam_selesai,
                       transaksi.pengguna, transaksi.tanggal_transaksi, transaksi.status_transaksi
                FROM transaksi
                INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas
                WHERE transaksi.id_transaksi = %s
                """,
                (id_pesanan,)
            )
            pesanan = cursor.fetchone()  # Pastikan hanya mengambil satu hasil

            if pesanan:
                break  # Keluar dari loop jika ID valid
            else:
                print("ID Pengajuan tidak ditemukan. Silakan coba lagi.")
        
        table = PrettyTable()
        table.field_names = ["Detail", "Value"]
        table.add_row(["ID Transaksi", pesanan[0]])
        table.add_row(["ID Detail Kelas", pesanan[1]])
        table.add_row(["Kode Kelas", pesanan[2]])
        table.add_row(["NIM Pemesan", pesanan[3]])
        table.add_row(["Kode Dosen", pesanan[4]])
        table.add_row(["Hari", pesanan[5]])
        table.add_row(["Jam Mulai", pesanan[6]])
        table.add_row(["Jam Selesai", pesanan[7]])
        table.add_row(["Pengguna", pesanan[8]])
        table.add_row(["Tanggal Pengajuan", pesanan[9]])
        table.add_row(["Status Saat Ini", pesanan[10]])

        print("\nDetail Pengajuan:")
        print(table)

        while True:
            # Input keputusan dari admin
            keputusan = input("Masukkan keputusan ('Y' ACC / 'N' Ditolak / '0' Batal): ").strip().upper()

            if keputusan == '0':
                print("Proses dibatalkan...")
                return

            # Validasi keputusan
            if keputusan not in ['Y', 'N', '0']:
                print("Keputusan tidak valid. Gunakan 'Y', 'N', atau '0'.")
                continue

            # Input alasan, gunakan default '-' jika kosong
            komentar = input("Masukkan alasan untuk keputusan (tekan Enter jika tidak ada): ").strip()
            if not komentar:
                komentar = "-"  # Isi default

            print(f"Keputusan: {'ACC' if keputusan == 'Y' else 'Ditolak'} dengan alasan: {komentar}")
            break

        # Tentukan status berdasarkan keputusan
        status = 'ACC Pengajuan' if keputusan.upper() == 'Y' else 'Pengajuan Ditolak'

        # Update status transaksi berdasarkan keputusan
        cursor.execute(
            "UPDATE transaksi SET status_transaksi = %s, komentar = %s WHERE id_transaksi = %s",
            (status, komentar, id_pesanan),
        )
        conn.commit()

        print(f"Pengajuan dengan ID {id_pesanan} telah diproses dan statusnya diubah menjadi '{status}'.")

        if status == 'ACC Pengajuan':
            # Ambil pengguna dari transaksi terkait
            cursor.execute(
                "SELECT pengguna FROM transaksi WHERE id_transaksi = %s",
                (id_pesanan,),
            )
            pengguna = cursor.fetchone()

            if pengguna:
                pengguna = pengguna[0]

                # Update status dan pengguna pada tb.detail_kelas
                cursor.execute(
                    """
                    UPDATE detail_kelas
                    SET status = 'Digunakan', pengguna = %s
                    WHERE id_detail_kelas = %s
                    """,
                    (pengguna, pesanan[1],)
                )
                conn.commit()

                print("Status dan pengguna berhasil diperbarui pada detail_kelas.")
            else:
                print("Pengguna tidak ditemukan pada transaksi terkait.")
        else:
            print("Keputusan ditolak, tidak ada perubahan pada detail_kelas.")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")

    finally:
        cursor.close()

class StatusTransaksi(Enum):
    ACC_PENGAJUAN = "ACC Pengajuan"
    ACC_PEMBATALAN = "ACC Pembatalan"
    PENGAJUAN_DITOLAK = "Pengajuan Ditolak"
    PEMBATALAN_DITOLAK = "Pembatalan Ditolak"
    PENGAJUAN_PENDING = "Pengajuan Pending"
    PEMBATALAN_PENDING = "Pembatalan Pending"
    PENGAJUAN_DIBATALKAN = "Pengajuan Dibatalakan"

def proses_pembatalan_kelas_admin():
    cursor = conn.cursor()
    try:
        # Ambil semua pengajuan pembatalan yang berstatus "Pembatalan Pending"
        cursor.execute(
            """
            SELECT transaksi.id_transaksi, transaksi.id_detail_kelas,
                   detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.kode_dosen, detail_kelas.hari, detail_kelas.jam_mulai, 
                   detail_kelas.jam_selesai, transaksi.pengguna, transaksi.tanggal_transaksi, transaksi.status_transaksi
            FROM transaksi
            INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas
            WHERE transaksi.status_transaksi = %s
            """, (StatusTransaksi.PEMBATALAN_PENDING.value,))
        daftar_pembatalan = cursor.fetchall()

        if not daftar_pembatalan:
            print("Tidak ada pengajuan pembatalan yang tersedia")
            return
        
        # Tampilkan daftar pengajuan pembatalan kelas
        print("Daftar pengajuan pembatalan kelas: ")
        
        # Cek apakah ada data 
        if daftar_pembatalan:
            print("\n=== Daftar Pembatalan ===")
            table = PrettyTable()
            table.field_names = ["ID Transaksi", "ID Kelas", "Diajukan oleh", "Kode Kelas","Kode Mata Kuliah","Kode Dosen","Hari", "Jam Mulai", "Jam Selesai","Tanggal Pengajuan", "Status Saat Ini"]
            
            for pembatalan in daftar_pembatalan:
                table.add_row([
                    pembatalan[0],  # ID Transaksi
                    pembatalan[1],  # ID Detail kelas
                    pembatalan[8],  # Diajukan oleh
                    pembatalan[2],  # Kode Kelas
                    pembatalan[3],  # Kode Matkul
                    pembatalan[4],  # Kode Dosen
                    pembatalan[5],  # Hari
                    pembatalan[6],  # Jam mulai
                    pembatalan[7],  # Jam selesai
                    pembatalan[9], # Tanggal pengajuan
                    pembatalan[10] # Status saat ini
                ])
    
             # Menampilkan tabel
            print(table)
        else:
            print("Tidak ada pembatalan yang ditemukan.")

        while True:
            # Input ID pengajuan pembatalan yang akan diproses
            id_transaksi = input("Masukkan ID transaksi yang akan diproses (Tekan 'Enter' untuk kembali): ").strip()
            
            if id_transaksi == "":
                print("Kembali ke menu utama.")
                return

            if not id_transaksi.isdigit(): # agar hanya menerima input angka
                print("ID Transaksi harus berupa angka. Silakan coba lagi.")
                continue

            # Periksa apakah ID pembatalan valid
            cursor.execute(
                """
                SELECT transaksi.id_transaksi, transaksi.id_detail_kelas,
                    detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.kode_dosen, detail_kelas.hari, detail_kelas.jam_mulai, 
                    detail_kelas.jam_selesai, transaksi.pengguna, transaksi.tanggal_transaksi, transaksi.status_transaksi
                FROM transaksi
                INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas
                WHERE transaksi.id_transaksi = %s
                """, (id_transaksi,))
            pembatalan = cursor.fetchone()
            
            if pembatalan is None or pembatalan[10] != StatusTransaksi.PEMBATALAN_PENDING.value:
                print("ID Pembatalan tidak ditemukan, silahkan cek kembali.")
            else:
                break

        # Tampilkan detail pengajuan pembatalan kelas
        table = PrettyTable()
        table.field_names = ["Detail", "Value"]

        # Menambahkan data pembatalan ke tabel
        table.add_row(["ID Transaksi", pembatalan[0]])
        table.add_row(["ID Detail Kelas", pembatalan[1]])
        table.add_row(["Diajukan oleh", pembatalan[8]])
        table.add_row(["Kode Kelas", pembatalan[2]])
        table.add_row(["Kode Mata Kuliah", pembatalan[3]])
        table.add_row(["Kode Dosen", pembatalan[4]])
        table.add_row(["Hari", pembatalan[5]])
        table.add_row(["Jam Mulai", pembatalan[6]])
        table.add_row(["Jam Selesai", pembatalan[7]])
        table.add_row(["Tanggal Pengajuan", pembatalan[9]])
        table.add_row(["Status Saat Ini", pembatalan[10]])

       # Menampilkan tabel
        print("\nDetail Pembatalan:")
        print(table)

        while True:
            # Input keputusan dari admin
            keputusan = input("Masukkan keputusan ('Y' ACC / 'N' Ditolak / '0' Batal): ").strip().upper()

            if keputusan == '0':
                print("Proses dibatalkan...")
                return

            # Validasi keputusan
            if keputusan not in ['Y', 'N', '0']:
                print("Keputusan tidak valid. Gunakan 'Y', 'N', atau '0'.")
                continue

            # Input alasan, gunakan default '-' jika kosong
            komentar = input("Masukkan alasan untuk keputusan (tekan Enter jika tidak ada): ").strip()
            if not komentar:
                komentar = "-"  # Isi default

            print(f"Keputusan: {'ACC' if keputusan == 'Y' else 'Ditolak'} dengan alasan: {komentar}")
            break

        # proses berdasarkan keputusan admin
        status = StatusTransaksi.ACC_PEMBATALAN.value if keputusan.upper() == "Y" else StatusTransaksi.PEMBATALAN_DITOLAK.value

        # Update status pembatalan berdasarkan keputusan admin
        cursor.execute("UPDATE transaksi SET status_transaksi = %s, komentar = %s WHERE id_transaksi = %s", (status, komentar, id_transaksi))
        conn.commit()

        print(f"Pembatalan dengan ID {id_transaksi} telah diproses dan statusnya di ubah menjadi '{status}'.")

        if status == StatusTransaksi.ACC_PEMBATALAN.value:
            cursor.execute("""
                UPDATE detail_kelas 
                SET pengguna = '', status = 'Tersedia' 
                WHERE id_detail_kelas = (
                    SELECT id_detail_kelas FROM transaksi WHERE id_transaksi = %s
                )
            """, (id_transaksi,))
            conn.commit()

        print("Data pada tabel detail_kelas telah diperbarui: kolom pengguna dikosongkan dan status diubah menjadi 'Tersedia'.")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")

    finally:
        cursor.close()

def proses_pembatalan_kelas_mandiri():
    cursor = conn.cursor()
    try:
        # Ambil semua pengajuan pembatalan yang berstatus "Pembatalan Pending"
        cursor.execute(
            """
            SELECT id_pengajuan, pengguna, kode_kelas, kode_matkul, kode_dosen, nama_dosen, hari,
                    jam_mulai, jam_selesai, tgl_pengajuan, status_pengajuan
            FROM pengajuan WHERE status_pengajuan = %s
            """, (StatusTransaksi.PEMBATALAN_PENDING.value,))
        daftar_pembatalan = cursor.fetchall()

        if not daftar_pembatalan:
            print("Tidak ada pengajuan pembatalan yang tersedia")
            return
        
        # Tampilkan daftar pengajuan pembatalan kelas
        print("Daftar pengajuan pembatalan kelas: ")
        
        # Cek apakah ada data 
        if daftar_pembatalan:
            print("\n=== Daftar Pembatalan ===")
            table = PrettyTable()
            table.field_names = ["ID Transaksi", "Diajukan oleh", "Kode Kelas","Kode Mata Kuliah","Kode Dosen", "Dosen", "Hari", "Jam Mulai", "Jam Selesai","Tanggal Pengajuan", "Status Saat Ini"]
            
            for pembatalan in daftar_pembatalan:
                table.add_row([
                    pembatalan[0],  # ID Transaksi
                    pembatalan[1],  # Diajukan oleh
                    pembatalan[2],  # Kode Kelas
                    pembatalan[3],  # Kode Matkul
                    pembatalan[4],  # Kode Dosen
                    pembatalan[5],  # Nama Dosen
                    pembatalan[6],  # Hari
                    pembatalan[7],  # Jam mulai
                    pembatalan[8],  # Jam selesai
                    pembatalan[9], # Tanggal pengajuan
                    pembatalan[10] # Status saat ini
                ])
    
             # Menampilkan tabel
            print(table)
        else:
            print("Tidak ada pembatalan yang ditemukan.")

        while True:
            # Input ID pengajuan pembatalan yang akan diproses
            id_pengajuan = input("Masukkan ID transaksi yang akan diproses (Tekan 'Enter' untuk kembali): ").strip()
            
            if id_pengajuan == '':
                print("Kembali ke menu utama...")
                return

            if not id_pengajuan.isdigit(): # agar hanya menerima input angka
                print("ID Transaksi harus berupa angka. Silakan coba lagi.")
                continue

            # Periksa apakah ID pembatalan valid
            cursor.execute(
                """
                SELECT id_pengajuan, pengguna, kode_kelas, kode_matkul, kode_dosen, nama_dosen, hari,
                        jam_mulai, jam_selesai, tgl_pengajuan, status_pengajuan
                FROM pengajuan WHERE id_pengajuan = %s
                """, (id_pengajuan,))
            pembatalan = cursor.fetchone()
            
            if pembatalan is None or pembatalan[10] != StatusTransaksi.PEMBATALAN_PENDING.value:
                print("ID Pembatalan tidak ditemukan, silahkan cek kembali.")
            else:
                break

        # Tampilkan detail pengajuan pembatalan kelas
        table = PrettyTable()
        table.field_names = ["Detail", "Value"]

        # Menambahkan data pembatalan ke tabel
        table.add_row(["ID Pengajuan", pembatalan[0]])
        table.add_row(["Diajukan oleh", pembatalan[1]])
        table.add_row(["Kode Kelas", pembatalan[2]])
        table.add_row(["Kode Mata Kuliah", pembatalan[3]])
        table.add_row(["Kode Dosen", pembatalan[4]])
        table.add_row(["Nama Dosen", pembatalan[5]])
        table.add_row(["Hari", pembatalan[6]])
        table.add_row(["Jam Mulai", pembatalan[7]])
        table.add_row(["Jam Selesai", pembatalan[8]])
        table.add_row(["Tanggal Pengajuan", pembatalan[9]])
        table.add_row(["Status Saat Ini", pembatalan[10]])

       # Menampilkan tabel
        print("\nDetail Pembatalan:")
        print(table)

        while True:
            # Input keputusan dari admin
            keputusan = input("Masukkan keputusan ('Y' ACC / 'N' Ditolak / '0' Batal): ").strip().upper()

            if keputusan == '0':
                print("Proses dibatalkan...")
                return

            # Validasi keputusan
            if keputusan not in ['Y', 'N', '0']:
                print("Keputusan tidak valid. Gunakan 'Y', 'N', atau '0'.")
                continue

            # Input alasan, gunakan default '-' jika kosong
            komentar = input("Masukkan alasan untuk keputusan (tekan Enter jika tidak ada): ").strip()
            if not komentar:
                komentar = "-"  # Isi default

            print(f"Keputusan: {'ACC' if keputusan == 'Y' else 'Ditolak'} dengan alasan: {komentar}")
            break

        # proses berdasarkan keputusan admin
        status = StatusTransaksi.ACC_PEMBATALAN.value if keputusan.upper() == "Y" else StatusTransaksi.PEMBATALAN_DITOLAK.value

        # Update status pembatalan berdasarkan keputusan admin
        cursor.execute("UPDATE pengajuan SET status_pengajuan = %s, komentar = %s WHERE id_pengajuan = %s", (status, komentar, id_pengajuan))
        conn.commit()

        if status == StatusTransaksi.ACC_PEMBATALAN.value:
            cursor.execute("""
                UPDATE detail_kelas 
                SET pengguna = '', status = 'Tersedia' 
                WHERE id_detail_kelas = (
                    SELECT id_detail_kelas FROM pengajuan WHERE id_pengajuan = %s
                )
            """, (id_pengajuan,))
            conn.commit()

        print("Data pada tabel detail_kelas telah diperbarui!")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")

    finally:
        cursor.close()

def proses_pengajuan_mandiri():
    cursor = conn.cursor()
    try:
        # Pastikan autocommit diaktifkan
        conn.autocommit = True

        cursor.execute("""
            SELECT id_pengajuan, pengguna, kode_kelas, kode_matkul, kode_dosen, nama_dosen, hari,
                    jam_mulai, jam_selesai, tgl_pengajuan, status_pengajuan
            FROM pengajuan WHERE status_pengajuan = 'Pengajuan Pending'
        """)
        pengajuan = cursor.fetchall()

        if not pengajuan:
            print("Tidak ada pengajuan yang perlu diproses.")
            return
        
        # Daftar pengajuan yang perlu diproses
        print("\n===== Daftar Pengajuan yang Perlu Diproses =====")
        for data in pengajuan:
            print("="*40)
            print(f"ID Pengajuan       : {data[0]}")
            print(f"Diajukan oleh      : {data[1]}")
            print(f"Kode Kelas         : {data[2]}")
            print(f"Kode Mata Kuliah   : {data[3]}")
            print(f"Kode Dosen         : {data[4]}")
            print(f"Dosen              : {data[5]}")
            print(f"Waktu Penggunaan   : {data[6]}, {data[7]} - {data[8]}")
            print(f"Tanggal Pengajuan  : {data[9]}")
            print(f"Status Pengajuan   : {data[10]}")
            print("="*40)

        while True:
            id_pengajuan = input("\nMasukkan ID pengajuan yang ingin diproses (Tekan 'Enter' untuk kembali): ")
            
            if id_pengajuan == '':
                print("Kembali ke menu utama...")
                return

            if not id_pengajuan.isdigit(): # agar hanya menerima input angka
                print("ID Transaksi harus berupa angka. Silakan coba lagi.")
                continue

            cursor.execute("""
                SELECT id_pengajuan, pengguna, kode_kelas, kode_matkul, kode_dosen, nama_dosen, hari,
                        jam_mulai, jam_selesai, tgl_pengajuan, status_pengajuan
                FROM pengajuan WHERE id_pengajuan = %s
            """, (id_pengajuan,))
            detail = cursor.fetchone()

            if not detail:
                print("ID tidak ditemukan, silahkan cek kembali.")
            else:
                break
        
        # Daftar pengajuan yang perlu diproses
        print(f"\n===== Detail Pengajuan ID {id_pengajuan} =====")
        print("="*40)
        print(f"ID Pengajuan       : {detail[0]}")
        print(f"Diajukan oleh      : {detail[1]}")
        print(f"Kode Kelas         : {detail[2]}")
        print(f"Kode Mata Kuliah   : {detail[3]}")
        print(f"Kode Dosen         : {detail[4]}")
        print(f"Dosen              : {detail[5]}")
        print(f"Waktu Penggunaan   : {detail[6]}, {detail[7]} - {detail[8]}")
        print(f"Tanggal Pengajuan  : {detail[9]}")
        print(f"Status Pengajuan   : {detail[10]}")
        print("="*40)

        while True:
            # Input keputusan dari admin
            keputusan = input("Masukkan keputusan ('Y' ACC / 'N' Ditolak / '0' Batal): ").strip().upper()

            if keputusan == '0':
                print("Proses dibatalkan...")
                return

            # Validasi keputusan
            if keputusan not in ['Y', 'N', '0']:
                print("Keputusan tidak valid. Gunakan 'Y', 'N', atau '0'.")
                continue

            # Input alasan, gunakan default '-' jika kosong
            komentar = input("Masukkan alasan untuk keputusan (tekan Enter jika tidak ada): ").strip()
            if not komentar:
                komentar = "-"  # Isi default

            print(f"Keputusan: {'ACC' if keputusan == 'Y' else 'Ditolak'} dengan alasan: {komentar}")
            break
        
        status_pengajuan = 'ACC Pengajuan' if keputusan.upper() == 'Y' else 'Pengajuan Ditolak'

        # Update status pengajuan berdasarkan keputusan
        cursor.execute(
            "UPDATE pengajuan SET status_pengajuan = %s, komentar = %s WHERE id_pengajuan = %s",
            (status_pengajuan, komentar, id_pengajuan),
        )
        conn.commit()
        print(f"Pengajuan ID {id_pengajuan} telah diproses.")

        if status_pengajuan == 'ACC Pengajuan':
            cursor.execute("""
                SELECT kode_kelas, kode_matkul, hari, jam_mulai, jam_selesai, 
                       kode_dosen, informasi_kelas, pengguna   
                FROM pengajuan WHERE id_pengajuan = %s
            """, (id_pengajuan,))
            data = cursor.fetchone()

            kode_kelas = data[0]
            kode_matkul = data[1]
            hari = data[2]
            jam_mulai = data[3]
            jam_selesai = data[4]
            kode_dosen = data[5]
            informasiKelas = data[6]
            pengguna = data[7]

            cursor.execute("""
                INSERT INTO detail_kelas (kode_kelas, kode_matkul, hari, jam_mulai, jam_selesai, 
                    kode_dosen, informasi_kelas, pengguna, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Digunakan')
            """, (kode_kelas,kode_matkul,hari,jam_mulai,jam_selesai,kode_dosen,informasiKelas,pengguna,))
            conn.commit()
            print("Data berhasil disimpan.")

            # Dapatkan id_detail_kelas yang baru ditambahkan dari insert di atas
            id_detail_kelas = cursor.lastrowid

            cursor.execute("""
                UPDATE pengajuan SET id_detail_kelas = %s WHERE id_pengajuan = %s
            """, (id_detail_kelas, id_pengajuan))
            conn.commit()
            print("Pengajuan berhasil diperbarui dengan ID Detail Kelas.")

        # Memuat ulang pengajuan setelah update
        cursor.execute("""
            SELECT id_pengajuan, pengguna, kode_kelas, kode_matkul, kode_dosen, nama_dosen, hari,
                    jam_mulai, jam_selesai, tgl_pengajuan, status_pengajuan
            FROM pengajuan WHERE status_pengajuan = 'Pengajuan Pending'
        """)
        pengajuan = cursor.fetchall()

        # Daftar pengajuan yang telah diperbarui
        print("\n===== Daftar Pengajuan yang Perlu Diproses =====")
        for data in pengajuan:
            print("="*40)
            print(f"ID Pengajuan       : {data[0]}")
            print(f"Diajukan oleh      : {data[1]}")
            print(f"Kode Kelas         : {data[2]}")
            print(f"Kode Mata Kuliah   : {data[3]}")
            print(f"Kode Dosen         : {data[4]}")
            print(f"Dosen              : {data[5]}")
            print(f"Waktu Penggunaan   : {data[6]}, {data[7]} - {data[8]}")
            print(f"Tanggal Pengajuan  : {data[9]}")
            print(f"Status Pengajuan   : {data[10]}")
            print("="*40)

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")

    finally:
        cursor.close()
