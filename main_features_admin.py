import mysql.connector
from admin_db_info import get_current_mysql_password

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
            kode_matkul = input("Masukkan Kode Mata Kuliah (tekan Enter untuk berhenti): ").strip()
            if not kode_matkul:  # Jika input kosong, berhenti
                break
            
            nama_matkul = input("Masukkan Nama Mata Kuliah: ").strip()
            if not nama_matkul:  # Validasi nama mata kuliah kosong
                print("Nama mata kuliah tidak boleh kosong. Silakan ulangi.")
                continue
            
            # Insert data ke database
            cursor.execute("INSERT INTO mata_kuliah (kode_matkul, nama_matkul) VALUES (%s, %s)", (kode_matkul, nama_matkul))
            conn.commit()
            print(f"Mata kuliah {nama_matkul} berhasil ditambahkan!\n")
        
        print("Proses penambahan mata kuliah selesai.")

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

def add_dosen():
    cursor = conn.cursor()
    print("\n=== Tambah Data Dosen ===")
    print("Tekan Enter pada 'NIP' jika ingin berhenti.\n")
    
    try:
        while True:
            # Input NIP Dosen
            nip = input("Masukkan NIP Dosen: ").strip()
            if not nip:  # Hentikan jika input kosong
                print("Proses penambahan data dosen selesai.\n")
                break

            # Input data lainnya
            nama = input("Masukkan Nama Dosen: ").strip()
            alamat = input("Masukkan Alamat Dosen: ").strip()
            email = input("Masukkan Email Dosen: ").strip()
            no_telp = input("Masukkan No. Telepon Dosen: ").strip()

            # Query untuk menambahkan data ke tabel dosen
            query = """
            INSERT INTO dosen (nip, nama, alamat, email, no_tlp)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nip, nama, alamat, email, no_telp))
            conn.commit()
            print(f"Data dosen dengan NIP '{nip}' berhasil ditambahkan!\n")

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
            print("\n=== Data Dosen ===")
            for dosen in dosens:
                print(f"""
                NIP        : {dosen[0]}
                Nama       : {dosen[1]}
                Alamat     : {dosen[2]}
                Email      : {dosen[3]}
                No. Telp   : {dosen[4]}
                """)
        else:
            print("Tidak ada data dosen.")
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat mengambil data dosen: {err}")
    finally:
        cursor.close()

# Fungsi untuk input jadwal kosong dosen
def input_jadwal_dosen():
    cursor = conn.cursor()
    print("\n=== Input Jadwal Kosong Dosen ===")
    nip = input("Masukkan NIP Dosen: ").strip()

    try:
        while True:
            hari = input("Masukkan hari (contoh: Senin, atau kosongkan untuk selesai): ").strip()
            if not hari:
                break

            jam_mulai = input("Masukkan jam mulai (format 24 jam, contoh: 08:00): ").strip()
            jam_selesai = input("Masukkan jam selesai (format 24 jam, contoh: 12:00): ").strip()

            query = "INSERT INTO jadwal_dosen (nip, hari, jam_mulai, jam_selesai) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nip, hari, jam_mulai, jam_selesai))
        conn.commit()
        print("Jadwal kosong dosen berhasil ditambahkan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def view_jadwal_dosen():
    cursor = conn.cursor()
    try:
        while True:
            print("\n=== Lihat Jadwal Kosong Dosen ===")
            print("1. Lihat semua jadwal dosen")
            print("2. Lihat jadwal berdasarkan NIP")
            print("3. Kembali ke menu utama")
            choice = input("Pilih menu: ").strip()

            if choice == "1":  # Lihat semua jadwal dosen
                query = """
                SELECT jadwal_dosen.nip, dosen.nama, jadwal_dosen.hari, jadwal_dosen.jam_mulai, jadwal_dosen.jam_selesai
                FROM jadwal_dosen
                INNER JOIN dosen ON jadwal_dosen.nip = dosen.nip
                """
                cursor.execute(query)
                jadwal = cursor.fetchall()

                if jadwal:
                    print("\n=== Jadwal Kosong Seluruh Dosen ===")
                    for j in jadwal:
                        print(f"""
                        =====================
                        NIP Dosen   : {j[0]}
                        Nama Dosen  : {j[1]}
                        Hari        : {j[2]}
                        Jam Mulai   : {j[3]}
                        Jam Selesai : {j[4]}
                        =====================
                        """)
                else:
                    print("Tidak ada jadwal kosong dosen.")

            elif choice == "2":  # Lihat jadwal berdasarkan NIP
                nip = input("Masukkan NIP dosen: ").strip()
                query_dosen = "SELECT nama FROM dosen WHERE nip = %s"
                cursor.execute(query_dosen, (nip,))
                result_dosen = cursor.fetchone()

                if result_dosen:  # Jika dosen ditemukan
                    nama_dosen = result_dosen[0]
                    query_jadwal = """
                    SELECT jadwal_dosen.hari, jadwal_dosen.jam_mulai, jadwal_dosen.jam_selesai
                    FROM jadwal_dosen
                    WHERE nip = %s
                    """
                    cursor.execute(query_jadwal, (nip,))
                    jadwal_dosen = cursor.fetchall()

                    if jadwal_dosen:
                        print(f"\n=== Jadwal Kosong untuk Dosen NIP {nip} ({nama_dosen}) ===")
                        for j in jadwal_dosen:
                            print(f"""
                            Hari        : {j[0]}
                            Jam Mulai   : {j[1]}
                            Jam Selesai : {j[2]}
                            """)
                    else:
                        print(f"Tidak ada jadwal kosong untuk dosen dengan NIP {nip} ({nama_dosen}).")
                else:
                    print(f"Dosen dengan NIP {nip} tidak ditemukan.")

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
    nip = input("Masukkan NIP Dosen yang ingin diedit jadwalnya: ").strip()

    try:
        # Menampilkan jadwal yang ada untuk dosen tersebut
        cursor.execute("SELECT id, hari, jam_mulai, jam_selesai FROM jadwal_dosen WHERE nip = %s", (nip,))
        jadwal = cursor.fetchall()

        if not jadwal:
            print(f"Tidak ada jadwal kosong untuk dosen dengan NIP {nip}.")
            return

        # Menampilkan jadwal yang ada
        print("\nJadwal Kosong yang Ada:")
        for j in jadwal:
            print(f"ID: {j[0]} - Hari: {j[1]} - Jam Mulai: {j[2]} - Jam Selesai: {j[3]}")

        # Memilih jadwal untuk diedit
        id_jadwal = input("\nMasukkan ID jadwal yang ingin diedit: ").strip()

        # Memeriksa apakah ID yang dimasukkan valid
        cursor.execute("SELECT * FROM jadwal_dosen WHERE id = %s", (id_jadwal,))
        jadwal_edit = cursor.fetchone()

        if not jadwal_edit:
            print(f"Jadwal dengan ID {id_jadwal} tidak ditemukan.")
            return

        # Mengedit data jadwal
        print("Masukkan data baru untuk jadwal ini.")
        hari_baru = input(f"Masukkan hari baru (sebelumnya {jadwal_edit[1]}): ").strip()
        jam_mulai_baru = input(f"Masukkan jam mulai baru (sebelumnya {jadwal_edit[2]}): ").strip()
        jam_selesai_baru = input(f"Masukkan jam selesai baru (sebelumnya {jadwal_edit[3]}): ").strip()

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
    nip = input("Masukkan NIP Dosen: ").strip()

    try:
        # Ambil jadwal kosong dosen dari database
        query = """
        SELECT jadwal_dosen.nip, dosen.nama, jadwal_dosen.hari, jadwal_dosen.jam_mulai, jadwal_dosen.jam_selesai
        FROM jadwal_dosen
        INNER JOIN dosen ON jadwal_dosen.nip = dosen.nip
        WHERE jadwal_dosen.nip = %s
        """
        cursor.execute(query, (nip,))
        jadwal_list = cursor.fetchall()


        if not jadwal_list:
            print("Tidak ada jadwal kosong untuk dosen ini!")
            return

        print(f"\nJadwal Kosong Dosen {jadwal_list[0][1]}:")
        for jadwal in jadwal_list:
            print("-"*40)
            print(f"NIP: {jadwal[0]}, Dosen: {jadwal[1]}, Hari: {jadwal[2]}, Jam: {jadwal[3]} - {jadwal[4]}")
            print("-"*40)

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
        print("\nMasukkan Waktu Penggunaan Kelas:")
        hari = input("Masukkan Hari (contoh: Senin): ").strip()
        jam_mulai = input("Masukkan Jam Mulai (HH:MM, contoh: 08:00): ").strip()
        jam_selesai = input("Masukkan Jam Selesai (HH:MM, contoh: 10:00): ").strip()

        # Validasi bentrok waktu
        query = """
            SELECT kode_kelas, hari, jam_mulai, jam_selesai, pengguna FROM detail_kelas 
            WHERE kode_kelas = %s AND hari = %s AND ((%s BETWEEN jam_mulai AND jam_selesai) OR (%s BETWEEN jam_mulai AND jam_selesai))
        """
        cursor.execute(query, (kode_kelas, hari, jam_mulai, jam_selesai))
        kelas_bentrok = cursor.fetchall()

        if kelas_bentrok:
            print("\nJadwal yang Anda pilih bertabrakan dengan kelas-kelas berikut:")
            print("-" * 40)
            for kelas in kelas_bentrok:
                print(f"Kode Kelas: {kelas[0]}, Hari: {kelas[1]}, Jam: {kelas[2]} - {kelas[3]}, Pengguna: {kelas[4]}")
            print("-" * 40)
            print("Silakan pilih jadwal yang berbeda.")
            return

        # Validasi bentrok ruang kelas
        query = """
            SELECT kode_kelas, hari, jam_mulai, jam_selesai, pengguna FROM detail_kelas 
            WHERE kode_kelas = %s AND hari = %s AND ((%s BETWEEN jam_mulai AND jam_selesai) OR (%s BETWEEN jam_mulai AND jam_selesai))
        """
        cursor.execute(query, (kode_kelas, hari, jam_mulai, jam_selesai))
        ruang_bentrok = cursor.fetchall()

        if ruang_bentrok:
            print("\nRuang kelas yang Anda pilih sudah terpakai pada waktu tersebut!")
            print("\nBerikut adalah kelas-kelas yang menggunakan ruang tersebut:")
            print("-" * 40)
            for ruang in ruang_bentrok:
                print(f"Kode Kelas: {ruang[0]}, Hari: {ruang[1]}, Jam: {ruang[2]} - {ruang[3]}, Pengguna: {ruang[4]}")
            print("-" * 40)
            print("Silakan pilih ruang kelas yang berbeda.")
            return

        # Memasukkan nama pengguna kelas
        pengguna = input("\nPengguna kelas (Contoh: RPL 1-C, kosongkan jika tidak ada pengguna): ").strip()

        # Tentukan status kelas
        status = 'Tersedia' if not pengguna else 'Digunakan'

        # Simpan data kelas ke database
        query = "SELECT informasi_kelas FROM kelas WHERE kode_kelas = %s"
        cursor.execute(query, (kode_kelas,))
        informasi_kelas_data = cursor.fetchone()

        if not informasi_kelas_data:
            print("Informasi kelas tidak ditemukan di tabel kelas.")
            return

        informasi_kelas = informasi_kelas_data[0]  # Pastikan ini mengakses kolom yang benar (kolom 1)

        # Simpan data kelas ke database
        query = """
            INSERT INTO detail_kelas (kode_kelas, kode_matkul, hari, nip_dosen, jam_mulai, jam_selesai, informasi_kelas, pengguna, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (kode_kelas, kode_matkul, hari, nip, jam_mulai, jam_selesai, informasi_kelas, pengguna, status))
        conn.commit()
        print("Kelas berhasil dibuat.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def edit_kelas():
    cursor = conn.cursor()
    print("\n=== Edit Data Kelas ===")

    try:
        # Menampilkan daftar kelas
        query = "SELECT id_detail_kelas, kode_kelas, kode_matkul, nip_dosen, jam_mulai, jam_selesai, pengguna, status FROM detail_kelas"
        cursor.execute(query)
        kelas_list = cursor.fetchall()

        if not kelas_list:
            print("Tidak ada data kelas yang tersedia!")
            return

        print("\nDaftar Kelas:")
        for kelas in kelas_list:
            print("-" * 40)
            print(f"ID: {kelas[0]}\nKode Kelas: {kelas[1]}\nKode Mata Kuliah: {kelas[2]}\nNIP Dosen: {kelas[3]}\nJam: {kelas[4]} - {kelas[5]}\nPengguna: {kelas[6]}\nStatus: {kelas[7]}")
            print("-" * 40)

        # Memilih kelas yang akan diedit
        kelas_id = input("\nMasukkan ID Kelas yang akan diedit: ").strip()

        # Mengambil data kelas berdasarkan ID
        query = "SELECT id_detail_kelas, kode_kelas, kode_matkul, nip_dosen, jam_mulai, jam_selesai, pengguna, status FROM detail_kelas WHERE id_detail_kelas = %s"
        cursor.execute(query, (kelas_id,))
        kelas = cursor.fetchone()

        if not kelas:
            print("Kelas dengan ID tersebut tidak ditemukan!")
            return

        print("\nData Kelas yang Dipilih:")
        print(f"ID: {kelas[0]}\nKode Kelas: {kelas[1]}\nKode Mata Kuliah: {kelas[2]}\nNIP Dosen: {kelas[3]}\nJam: {kelas[4]} - {kelas[5]}\nPengguna: {kelas[6]}\nStatus: {kelas[7]}")

        # Mengedit data kelas
        print("\nMasukkan data baru (kosongkan jika tidak ingin mengubah):")
        kode_kelas_baru = input("Kode Kelas baru: ").strip() or kelas[1]
        kode_matkul_baru = input("Kode Mata Kuliah baru: ").strip() or kelas[2]
        nip_dosen_baru = input("NIP Dosen baru: ").strip() or kelas[3]
        jam_mulai_baru = input("Jam Mulai baru (HH:MM): ").strip() or kelas[4]
        jam_selesai_baru = input("Jam Selesai baru (HH:MM): ").strip() or kelas[5]
        pengguna_baru = input("Pengguna baru: ").strip() or kelas[6]
        status_baru = input("Status baru (kosongkan untuk tetap 'Digunakan'): ").strip() or kelas[7]

        # Update data kelas di database
        query = """
            UPDATE detail_kelas
            SET kode_kelas = %s, kode_matkul = %s, nip_dosen = %s, jam_mulai = %s, jam_selesai = %s, pengguna = %s, status = %s
            WHERE id_detail_kelas = %s
        """
        cursor.execute(query, (kode_kelas_baru, kode_matkul_baru, nip_dosen_baru, jam_mulai_baru, jam_selesai_baru, pengguna_baru, status_baru, kelas_id))
        conn.commit()
        print("Data kelas berhasil diperbarui.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


def tampilkan_kelas():
    try:
        cursor = conn.cursor()
        query = '''
        SELECT detail_kelas.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.nip_dosen, dosen.nama, detail_kelas.jam_mulai, 
        detail_kelas.jam_selesai, detail_kelas.informasi_kelas, detail_kelas.status, detail_kelas.pengguna FROM detail_kelas INNER JOIN dosen ON detail_kelas.nip_dosen = dosen.nip
        ORDER BY kode_kelas ASC
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        print("\n---List Kelas---")
        if results:
            for row in results:
                
                print("-" * 40)
                print(f"ID Detail Kelas      : {row[0]}")
                print(f"Kode Kelas           : {row[1]}")
                print(f"Kode Mata Kuliah     : {row[2]}")
                print(f"NIP Dosen            : {row[3]}")
                print(f"Dosen yang mengajar  : {row[4]}")
                print(f"Waktu Penggunaan     : {row[5]} - {row[6]}")
                print(f"Informasi Kelas      : {row[7]}")
                print(f"Pengguna             : {row[9]}")
                print(f"Status               : {row[8]}")
                print("-" * 40)
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
        cursor.execute("SELECT * FROM transaksi")
        daftar_pengajuan = cursor.fetchall()

        if not daftar_pengajuan:
            print("Tidak ada pengajuan yang tersedia.")
            return

        # Tampilkan daftar pengajuan
        print("Daftar Pengajuan:")
        for pengajuan in daftar_pengajuan:
            print("\n")
            print("="*40)
            print(f"ID Transaksi      : {pengajuan[0]}")
            print(f"ID Kelas          : {pengajuan[1]}")
            print(f"NIM               : {pengajuan[2]}")
            print(f"Email             : {pengajuan[3]}")
            print(f"Tanggal Pengajuan : {pengajuan[4]}")
            print(f"Status Saat Ini   : {pengajuan[5]}")
            print("="*40)

        # Input ID pengajuan yang akan diproses
        id_pesanan = input("Masukkan ID Pengajuan yang akan diproses: ").strip()

        # Periksa apakah ID Pengajuan valid
        cursor.execute("SELECT * FROM transaksi WHERE id_transaksi = %s", (id_pesanan,))
        pesanan = cursor.fetchone()

        if pesanan is None:
            print("ID Pengajuan tidak ditemukan.")
            return

        # Tampilkan detail pengajuan
        print("\nDetail Pengajuan:")
        print(f"ID Transaksi      : {pesanan[0]}")
        print(f"ID Kelas          : {pesanan[1]}")
        print(f"NIM               : {pesanan[2]}")
        print(f"Email             : {pesanan[3]}")
        print(f"Tanggal Pengajuan : {pesanan[4]}")
        print(f"Status Saat Ini   : {pesanan[5]}")

        # Input keputusan dari admin
        keputusan = input("Masukkan keputusan ('Y' ACC / 'N' Ditolak): ").strip()

        # Validasi keputusan
        if keputusan.upper() not in ["Y", "N"]:
            print("Keputusan tidak valid. Gunakan 'Y' atau 'N'.")
            return

        # Tentukan status berdasarkan keputusan
        status = 'ACC' if keputusan.upper() == 'Y' else 'Ditolak'

        # Update status transaksi berdasarkan keputusan
        cursor.execute("UPDATE transaksi SET status_transaksi = %s WHERE id_transaksi = %s", (status, id_pesanan))
        conn.commit()

        print(f"Pengajuan dengan ID {id_pesanan} telah diproses dan statusnya diubah menjadi '{status}'.")
    
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    
    finally:
        cursor.close()

def proses_pembatalan_kelas():
    cursor = conn.cursor()
    try:
        # ambil semua pengajuan pembatalan kelas yang tersedia
        cursor.execute("SELECT * FROM Pembatalan_Transaksi")
        daftar_pengajuan_pembatalan = cursor.fetchall()

        if not daftar_pengajuan_pembatalan:
            print("Tidak ada pengajuan pembatalan yang tersedia")
            return
        
        # Tampilkan daftar pengajuan pembatalan kelas
        print("Daftar pengajuan pembatalan kelas: ")
        for pengajuan in daftar_pengajuan_pembatalan:
            print("\n")
            print("="*40)
            print(f"ID Pembatalan                : {pengajuan[0]}")
            print(f"ID Kelas                     : {pengajuan[1]}")
            print(f"NIM                          : {pengajuan[2]}")
            print(f"Email                        : {pengajuan[3]}")
            print(f"Tanggal Pengajuan pembatalan : {pengajuan[4]}")
            print(f"Status Saat Ini              : {pengajuan[5]}")
            print("="*40)

            # Input ID pengajuan pembatalan yang akan diproses
            id_pembatalan = input("Masukkan ID pengajuan Pembatalan yang akan diproses: ").strip()

            # Periksa apakah ID pembatalan valid
            cursor.execute("SELECT * FROM pembatalan_transaksi WHERE id_pembatalan = %s", (id_pembatalan,))
        pembatalan = cursor.fetchone()
         
        if pembatalan is None:
            print("ID Pembatalan tidak ditemukan.")
            return

        # Tampilkan detail pengajuan pembatalan kelas
        print("\nDetail Pengajuan Pembatalan:")
        print(f"ID Pembatalan                : {pembatalan[0]}")
        print(f"ID Kelas                     : {pembatalan[1]}")
        print(f"NIM                          : {pembatalan[2]}")
        print(f"Email                        : {pembatalan[3]}")
        print(f"Tanggal Pengajuan pembatalan : {pembatalan[4]}")
        print(f"Status Saat Ini              : {pembatalan[5]}") 

        # Input keputusan dari admin
        keputusan = input("Masukkan keputusan ('Y' ACC / 'N' Ditolak): ").strip()

        #Validasi keputusan
        if keputusan.upper() not in ['Y', 'N']:
            print("Keputusan tidak valid. Gunakan 'Y' atau 'N'.")
            return
        
        # proses berdasarkan keputusan admin
        status = 'ACC' if keputusan.upper() == 'Y' else 'Ditolak'

        # Update status pembatalan berdasarkan keputusan admin
        cursor.execute("UPDATE pembatalan_transaksi SET status_pembatalan = %s WHERE id_pembatalan = %s", (status, id_pembatalan))
        conn.commit()

        print(f"Pengajuan pembatalan dengan ID {id_pembatalan} telah diproses dan statusnya di ubah menjadi'{status}'.")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")

    finally:
        cursor.close()