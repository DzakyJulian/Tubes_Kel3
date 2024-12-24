import mysql.connector
from admin_db_info import get_current_mysql_password

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
        query = '''
        SELECT detail_kelas.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.nip_dosen, 
               dosen.nama, detail_kelas.jam_mulai, detail_kelas.jam_selesai, detail_kelas.informasi_kelas, 
               detail_kelas.status, detail_kelas.pengguna, detail_kelas.hari 
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

        for row in results:
            print("-" * 40)
            print(f"ID Detail Kelas      : {row[0]}")
            print(f"Kode Kelas           : {row[1]}")
            print(f"Kode Mata Kuliah     : {row[2]}")
            print(f"NIP Dosen            : {row[3]}")
            print(f"Dosen yang mengajar  : {row[4]}")
            print(f"Waktu Penggunaan     : {row[10]}, {row[5]} - {row[6]}")
            print(f"Informasi Kelas      : {row[7]}")
            print(f"Pengguna             : {row[9]}")
            print(f"Status               : {row[8]}")
            print("-" * 40)

        pengguna = input("\nSiapa yang mengajukan kelas? (masukkan kelas contoh RPL 1-C): ").strip()
        
        id_detail_kelas = input("\nMasukkan ID Detail Kelas yang ingin diajukan (bukan kode kelas): ").strip()

        cursor.execute('''
        SELECT jam_mulai, jam_selesai, pengguna FROM detail_kelas WHERE id_detail_kelas = %s
        ''', (id_detail_kelas,))
        kelas_terpilih = cursor.fetchone()

        if kelas_terpilih is None:
            print("ID Detail Kelas tidak ditemukan.")
            return

        jam_mulai_baru = kelas_terpilih[0]
        jam_selesai_baru = kelas_terpilih[1]
        pengguna_baru = kelas_terpilih[2]

        if pengguna_baru is None or pengguna_baru.strip() == '':
            if not cek_ketersediaan_kelas(jam_mulai_baru, jam_selesai_baru):
                return

            valid_input = False
            while not valid_input:
                confirmation = input(f"Apakah anda yakin ingin memesan kelas ini? (Y/N): ")
                
                if confirmation.lower() == 'y':
                    try:
                        cursor.execute(''' 
                        INSERT INTO transaksi (nim, id_detail_kelas, email, tanggal_transaksi, status_transaksi, pengguna)
                        VALUES (%s, %s, %s, NOW(), 'Pengajuan Pending', %s)
                        ''', (nim, id_detail_kelas, email, pengguna))
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
        else:
            print(f"Digunakan oleh {pengguna_baru[2]}, tidak dapat memesan kelas ini.")

    except mysql.connector.Error as err:
        print(f"Error: Terjadi kesalahan saat mengambil data kelas. {err}")
    
    finally:
        cursor.close()

def cek_ketersediaan_kelas(jam_mulai_baru, jam_selesai_baru):
    cursor = conn.cursor()
    try:
        query = '''
        SELECT * FROM detail_kelas 
        WHERE status = 'Tersedia'
        AND pengguna = ''
        AND NOT (
            (jam_mulai < %s AND jam_selesai > %s)
        )
        '''
        cursor.execute(query, (jam_selesai_baru, jam_mulai_baru))
        results = cursor.fetchall()

        if results:
            print("Tidak dapat mengajukan kelas, karena waktu tersebut sudah digunakan oleh pengguna lain.")
            return False
        return True
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat memeriksa ketersediaan waktu kelas: {err}")
        return False
    finally:
        cursor.close()

def batal_kelas(nim):
    cursor = conn.cursor()
    
    try:
        # Tampilkan pesanan yang sudah ada (status 'Pending' atau 'Confirmed')
        print("\n--- Pesanan Kelas Anda ---")
        cursor.execute('''
            SELECT transaksi.id_transaksi, transaksi.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.nip_dosen,  
                    detail_kelas.hari, detail_kelas.jam_mulai, detail_kelas.jam_selesai, transaksi.tanggal_transaksi, 
                    transaksi.pengguna, transaksi.status_transaksi
            FROM transaksi
            INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas
            WHERE transaksi.nim = %s AND transaksi.status_transaksi = 'Pengajuan Pending'
        ''', (nim,))
        result = cursor.fetchall()

        if not result:
            print("Tidak ada kelas yang dapat dibatalkan atau sudah dikonfirmasi.")
            return

        # Menampilkan daftar pesanan kelas yang dapat dibatalkan
        print("-" * 40)
        for row in result:
            print(f"ID Pesanan           : {row[0]}")
            print(f"ID Detail Kelas      : {row[1]}")
            print(f"Kode Kelas           : {row[2]}")
            print(f"Dosen                : {row[3]}")
            print(f"Waktu Penggunaan     : {row[4]}, {row[5]} - {row[6]}")
            print(f"Tanggal Transaksi    : {row[7]}")
            print(f"Diajukan oleh        : {row[8]}")
            print(f"Status Transaksi     : {row[9]}")
            print("-" * 40)

        # Input ID Pesanan yang ingin dibatalkan
        id_transaksi = input("Masukkan ID Pesanan yang ingin dibatalkan: ").strip()

        # Verifikasi ID Transaksi yang dipilih
        cursor.execute('''
            SELECT * FROM transaksi WHERE id_transaksi = %s AND nim = %s
        ''', (id_transaksi, nim))
        transaksi_terpilih = cursor.fetchone()

        if transaksi_terpilih is None:
            print("ID Transaksi tidak ditemukan.")
            return

        # Proses konfirmasi pembatalan
        confirmation = input(f"Apakah Anda yakin ingin membatalkan pesanan kelas ID {id_transaksi}? (Y/N): ")
        if confirmation.lower() == 'y':
            # Update status transaksi menjadi 'Cancelled'
            cursor.execute('''
                UPDATE transaksi
                SET status_transaksi = 'Pengajuan Dibatalkan'
                WHERE id_transaksi = %s
            ''', (id_transaksi,))
            conn.commit()
            print("Pesanan kelas berhasil dibatalkan.")
        elif confirmation.lower() == 'n':
            print("Pembatalan dibatalkan.")
        else:
            print("Input tidak valid.")

    except mysql.connector.Error as err:
        print(f"Error: Terjadi kesalahan saat membatalkan pesanan kelas. {err}")
    finally:
        cursor.close()

def lihat_pesanan_saya(NIM):
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
                SELECT transaksi.id_transaksi, transaksi.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.nip_dosen,  
                       detail_kelas.hari, detail_kelas.jam_mulai, detail_kelas.jam_selesai, transaksi.tanggal_transaksi, 
                       transaksi.pengguna, transaksi.status_transaksi 
                FROM transaksi 
                       INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas WHERE nim = {NIM}
                """)
        result = cursor.fetchall()
        
        if (len(result) == 0):
            print("Anda belum memiliki pesanan kelas.")
        else:
            print("\n============== Pesanan Saya =================")
            for i in result:
                print(f"ID Pesanan           : {i[0]}")
                print(f"ID Detail Kelas      : {i[1]}")
                print(f"Kode Kelas           : {i[2]}")
                print(f"Dosen                : {i[3]}")
                print(f"Waktu Penggunaan     : {i[4]}, {i[5]} - {i[6]}")
                print(f"Tanggal Transaksi    : {i[7]}")
                print(f"Diajukan untuk kelas : {i[8]}")
                print(f"Status Transaksi     : {i[9]}")
                print("=============================================")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
