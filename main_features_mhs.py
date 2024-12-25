import mysql.connector
from admin_db_info import get_current_mysql_password
from prettytable import PrettyTable

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
    database="ebookingclass"
)


def ajukan_kelas(nim, email):
    cursor = conn.cursor()
    
    # Tampilkan kelas yang tersedia (status 'Tersedia')
    print("\n--- Kelas Tersedia ---")
    try:
        # Query untuk menampilkan kelas yang berstatus 'Tersedia' saja
        query = '''
        SELECT detail_kelas.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.nip_dosen, 
               dosen.nama, detail_kelas.jam_mulai, detail_kelas.jam_selesai, detail_kelas.informasi_kelas, 
               detail_kelas.status, detail_kelas.pengguna 
        FROM detail_kelas 
        INNER JOIN dosen ON detail_kelas.nip_dosen = dosen.nip
        WHERE detail_kelas.status = 'Tersedia'
        ORDER BY kode_kelas ASC
        '''
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("Tidak ada kelas yang tersedia saat ini.")
            return

        # Menampilkan daftar kelas yang tersedia
        if results:
           print("\n=== Detail Kelas ===")
           table = PrettyTable()
           table.field_names = ["ID Detail Kelas", "Kode Kelas", "Kode Mata Kuliah", "NIP Dosen", "Dosen yang Mengajar", "Waktu Mulai", "Waktu Selesai", "Informasi Kelas", "Pengguna", "Status"]
           for row in results:
            table.add_row([
                row[0], row[1], row[2], row[3], 
                row[4], row[5], row[6], row[7], 
                row[8], row[9]])
            print(table)
        else:
            print("Tidak ada Data Kelas ")    

        # Input ID Detail Kelas yang ingin diajukan
        id_detail_kelas = input("\nMasukkan ID Detail Kelas yang ingin diajukan (bukan kode kelas): ").strip()

        # Ambil data kelas yang dipilih untuk mengecek jam mulai dan selesai
        cursor.execute('''
        SELECT jam_mulai, jam_selesai FROM detail_kelas WHERE id_detail_kelas = %s
        ''', (id_detail_kelas,))
        kelas_terpilih = cursor.fetchone()

        if kelas_terpilih is None:
            print("ID Detail Kelas tidak ditemukan.")
            return

        jam_mulai_baru = kelas_terpilih[0]
        jam_selesai_baru = kelas_terpilih[1]

        # Cek ketersediaan waktu kelas yang dipilih
        if not cek_ketersediaan_kelas(jam_mulai_baru, jam_selesai_baru):
            return  # Jika waktu sudah digunakan, tidak lanjutkan pengajuan

        # Proses konfirmasi pengajuan kelas
        valid_input = False
        while not valid_input:
            confirmation = input(f"Apakah anda yakin ingin memesan kelas ini? (Y/N): ")
            
            if confirmation.lower() == 'y':
                try:
                    # Insert data transaksi untuk pemesanan kelas
                    cursor.execute('''
                    INSERT INTO transaksi (nim, id_detail_kelas, email, tanggal_transaksi, status_transaksi)
                    VALUES (%s, %s, %s, NOW(), 'Pending')
                    ''', (nim, id_detail_kelas, email))
                    conn.commit()
                    print("Pemesanan kelas berhasil. Pengajuan kelas akan ditujukan kepada akademik.")
                    valid_input = True
                except mysql.connector.Error as err:
                    print(f"Error: Terjadi kesalahan, tidak dapat memesan kelas. {err}")
            elif confirmation.lower() == 'n':
                print("Anda tidak jadi memesan kelas ini.")
                valid_input = True
            else:
                print("Input tidak valid.")
    
    except mysql.connector.Error as err:
        print(f"Error: Terjadi kesalahan saat mengambil data kelas. {err}")
    
    finally:
        cursor.close()

def cek_ketersediaan_kelas(jam_mulai_baru, jam_selesai_baru):
    cursor = conn.cursor()
    try:
        # Query untuk mencari kelas yang memiliki waktu tumpang tindih
        query = '''
        SELECT * FROM detail_kelas 
        WHERE status = 'Tersedia' 
        AND ((jam_mulai BETWEEN %s AND %s) OR (jam_selesai BETWEEN %s AND %s) 
             OR (%s BETWEEN jam_mulai AND jam_selesai) OR (%s BETWEEN jam_mulai AND jam_selesai))
        '''
        cursor.execute(query, (jam_mulai_baru, jam_selesai_baru, jam_mulai_baru, jam_selesai_baru, jam_mulai_baru, jam_selesai_baru))
        results = cursor.fetchall()

        # Jika ada kelas yang memiliki waktu tumpang tindih
        if results:
            print("Tidak dapat mengajukan kelas, karena waktu tersebut sudah digunakan.")
            return False
        return True
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat memeriksa ketersediaan waktu kelas: {err}")
        return False
    finally:
        cursor.close()


def lihat_pesanan_saya(NIM):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM transaksi INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas WHERE nim = \"{NIM}\" ")
        result = cursor.fetchall()
        
        if len(result) == 0:  # Jika tidak ada data
            print("Anda belum memiliki pesanan kelas.")
        else:
            print("\n============== Pesanan Saya =================")
            table = PrettyTable()
            table.field_names = ["ID Pesanan", "ID Detail Kelas", "Kode Kelas", "Jam Mulai", "Jam Selesai", "Tanggal Transaksi", "Status Transaksi"]
            
            for i in result:
                table.add_row([
                    i[0],  # ID Pesanan
                    i[1],  # ID Detail Kelas
                    i[8],  # Kode Kelas
                    i[11], # Jam Mulai
                    i[12], # Jam Selesai
                    i[4],  # Tanggal Transaksi
                    i[5]   # Status Transaksi
                ])
            print(table)
                
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def batalkan_kelas(nim, id_pesanan):
    cursor = conn.cursor()
    try:
        # Periksa apakah pesanan berstatus 'Pending'
        cursor.execute('''
        SELECT * FROM transaksi WHERE id_transaksi = %s AND nim = %s AND status_transaksi = 'Pending'
        ''', (id_pesanan, nim))
        pesanan = cursor.fetchone()

        if pesanan:
            # Jika pesanan berstatus 'Pending', langsung batalkan
            cursor.execute('''
            UPDATE transaksi SET status_transaksi = 'Dibatalkan' WHERE id_transaksi = %s
            ''', (id_pesanan,))
            conn.commit()
            print(f"Pesanan dengan ID {id_pesanan} berhasil dibatalkan.")
            return

        # Periksa apakah pesanan sudah di-ACC oleh admin
        cursor.execute('''
        SELECT * FROM transaksi WHERE id_transaksi = %s AND nim = %s AND status_transaksi = 'ACC Pengajuan'
        ''', (id_pesanan, nim))
        pesanan_acc = cursor.fetchone()

        if pesanan_acc:
            # Jika sudah di-ACC, ubah status menjadi 'Pembatalan Pending'
            cursor.execute('''
            UPDATE transaksi SET status_transaksi = 'Pembatalan Pending' WHERE id_transaksi = %s
            ''', (id_pesanan,))
            conn.commit()
            print(f"Pengajuan pembatalan untuk ID {id_pesanan} berhasil diajukan. Menunggu konfirmasi admin.")
        else:
            print(f"Pesanan dengan ID {id_pesanan} tidak ditemukan atau tidak dapat dibatalkan. Status saat ini: {pesanan_acc['status_transaksi'] if pesanan_acc else 'tidak ada'}.")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def logout():
    print("\nAnda telah logout. Sampai jumpa lagi!!!") 