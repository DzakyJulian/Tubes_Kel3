import mysql.connector
from admin_db_info import get_current_mysql_password

def create_table():
    # Koneksi ke database MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=get_current_mysql_password(),
        database="ebookingclass"
    )
    cursor = conn.cursor()
    
    # Fungsi untuk membuat tabel
    def create_tables():
        # Tabel users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            nim INT(20) PRIMARY KEY NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(60) NOT NULL,
            user_role ENUM('admin','mahasiswa') NOT NULL
        )''')
    
        # Tabel dosen
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS dosen (
            nip INT(20) NOT NULL PRIMARY KEY,
            nama VARCHAR(255) NOT NULL,
            alamat TEXT NOT NULL,
            email VARCHAR(255) NOT NULL,
            no_tlp VARCHAR(20) NOT NULL
        )''')
    
        # Tabel jadwal_dosen
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS jadwal_dosen (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nip INT(20) NOT NULL,
            hari ENUM('Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu') NOT NULL,
            jam_mulai TIME NOT NULL,
            jam_selesai TIME NOT NULL,
            FOREIGN KEY (nip) REFERENCES dosen(nip)
        )''')
    
        # Tabel mata_kuliah
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mata_kuliah (
            kode_matkul VARCHAR(10) PRIMARY KEY,
            nama_matkul VARCHAR(255) NOT NULL
        )''')
    
        # Tabel kelas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS kelas (
            kode_kelas VARCHAR(30) PRIMARY KEY,
            informasi_kelas TEXT NOT NULL
        )''')
    
        # Tabel detail_kelas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS detail_kelas (
            id_detail_kelas INT AUTO_INCREMENT PRIMARY KEY,
            kode_kelas VARCHAR(30),
            kode_matkul VARCHAR(10),
            hari ENUM('Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat') NOT NULL,
            jam_mulai TIME NOT NULL,
            jam_selesai TIME NOT NULL,
            nip_dosen INT(20) NOT NULL,
            informasi_kelas TEXT NOT NULL,
            pengguna VARCHAR(30) NULL,
            status ENUM('Tersedia', 'Digunakan') NOT NULL,
            FOREIGN KEY (kode_matkul) REFERENCES mata_kuliah(kode_matkul),
            FOREIGN KEY (nip_dosen) REFERENCES dosen(nip),
            FOREIGN KEY (kode_kelas) REFERENCES kelas(kode_kelas)
        )''')
    
        # Tabel transaksi
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaksi (
            id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
            id_detail_kelas INT(11),
            nim INT(20) NOT NULL,
            email VARCHAR(255) NOT NULL,
            tanggal_transaksi DATETIME NOT NULL,
            status_transaksi ENUM('ACC Pengajuan','ACC Pembatalan', 'Pengajuan Ditolak', 'Pembatalan Ditolak', 'Pengajuan Pending', 'Pembatalan Pending', 'Pengajuan Dibatalkan') NOT NULL,
            pengguna VARCHAR(30) NOT NULL,
            komentar VARCHAR(255),
            FOREIGN KEY (nim) REFERENCES users(nim),
            FOREIGN KEY (id_detail_kelas) REFERENCES detail_kelas(id_detail_kelas)
        )''')
    
        print("Tabel-tabel berhasil dibuat.")
    
    # Eksekusi pembuatan tabel
    create_tables()
    
    # Tutup koneksi
    conn.close()