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

    # Memilih dosen
    nip = input("Masukkan NIP Dosen: ").strip()

    try:
        # Ambil jadwal kosong dosen dari database
        query = "SELECT id, hari, jam_mulai, jam_selesai FROM jadwal_dosen WHERE nip = %s"
        cursor.execute(query, (nip,))
        jadwal_list = cursor.fetchall()

        if not jadwal_list:
            print("Tidak ada jadwal kosong untuk dosen ini!")
            return

        print("\nJadwal Kosong Dosen:")
        for jadwal in jadwal_list:
            print("-"*40)
            print(f"ID: {jadwal[0]}, Hari: {jadwal[1]}, Jam: {jadwal[2]} - {jadwal[3]}")
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

        # waktu_penggunaan = f"{hari} {jam_mulai} - {jam_selesai}"

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

        pengguna = input("\nMasukkan nama pengguna kelas(Contoh: RPL 1-C): ").strip()

        # Simpan data kelas ke database
        informasi_kelas = f"Kelas untuk mata kuliah {kode_matkul} dengan dosen NIP {nip} pada hari {hari}, jam {jam_mulai} - {jam_selesai} di ruang {kode_kelas}."
        query = "INSERT INTO detail_kelas (kode_kelas, kode_matkul, nip_dosen, informasi_kelas, pengguna, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (kode_kelas, kode_matkul, nip, informasi_kelas, pengguna, 'Digunakan'))
        conn.commit()
        print("Kelas berhasil dibuat.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Fungsi tambahan untuk mahasiswa
def view_kelas():
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

def tampilkan_kelas():
    try:
        cursor = conn.cursor()
        query = '''
        SELECT detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.nip_dosen, dosen.nama, detail_kelas.informasi_kelas,
        detail_kelas.status, detail_kelas.pengguna FROM detail_kelas INNER JOIN dosen ON detail_kelas.nip_dosen = dosen.nip
        ORDER BY kode_kelas ASC
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        print("\n---List Kelas---")
        if results:
            for row in results:
                
                print("-" * 40)
                print(f"Kode Kelas           : {row[0]}")
                print(f"Kode Mata Kuliah     : {row[1]}")
                print(f"NIP Dosen            : {row[2]}")
                print(f"Dosen yang mengajar  : {row[3]}")
                print(f"Informasi Kelas      : {row[4]}")
                print(f"Status               : {row[5]} oleh {row[6]}")
                print("-" * 40)
        else:
            print("Tidak ada data di tabel detail_kelas.")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat mengambil data: {err}")

    finally:
        cursor.close()


def ajukan_kelas():
    cursor = conn.cursor()
    kode_kelas = input("Masukkan Kode Kelas yang ingin diajukan: ").strip()
    nim = input("Masukkan NIM Anda: ").strip()
    try:
        cursor.execute('''
        INSERT INTO pengajuan (nim, kode_kelas, tanggal_pengajuan, status_pengajuan)
        VALUES (%s, %s, NOW(), 'Berhasil')
        ''', (nim, kode_kelas))
        conn.commit()
        print("Pengajuan kelas berhasil!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()