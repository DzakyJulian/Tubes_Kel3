import mysql.connector
from datetime import datetime
from admin_db_info import get_current_mysql_password
from main_features_admin import view_mata_kuliah
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
        query = '''
        SELECT detail_kelas.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.kode_matkul, detail_kelas.kode_dosen, 
               dosen.nama, detail_kelas.hari, detail_kelas.jam_mulai, detail_kelas.jam_selesai, detail_kelas.informasi_kelas, 
               detail_kelas.status, detail_kelas.pengguna
        FROM detail_kelas 
        INNER JOIN dosen ON detail_kelas.kode_dosen = dosen.kode_dosen
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
            table.field_names = [
                "ID Detail Kelas",
                "Kode Kelas", 
                "Kode Mata Kuliah", 
                "Kode Dosen", 
                "Dosen yang Mengajar", 
                "Hari", 
                "Waktu Mulai", 
                "Waktu Selesai", 
                "Informasi Kelas", 
                "Pengguna", 
                "Status",
            ]
            for row in results:
                table.add_row([ 
                    row[0], 
                    row[1], 
                    row[2], 
                    row[3], 
                    row[4], 
                    row[5], 
                    row[6], 
                    row[7], 
                    row[8], 
                    row[10], 
                    row[9]])
            print(table)
        else:
            print("Tidak ada Data Kelas ")    

        # Validasi pengguna tidak boleh kosong
        while True:
            pengguna = input("Siapa yang mengajukan kelas? (masukkan kelas contoh RPL 1-C) atau ketik 0 untuk kembali: ").strip()
            if len(pengguna) <= 0:
                print("Pengguna kelas tidak boleh kosong.")
            else:
                break
            
        if pengguna == '0':
            return
        
        id_detail_kelas = input("Masukkan ID Detail Kelas yang ingin diajukan (bukan kode kelas) atau ketik 0 untuk kembali: ").strip()

        if id_detail_kelas == '0':
            return

        # Validasi ID Kelas sudah dipesan oleh mahasiswa atau belum
        cursor.execute('''
        SELECT * FROM transaksi WHERE id_detail_kelas = %s AND nim = %s
        ''', (id_detail_kelas, nim))
        tr_res = cursor.fetchall()
        
        if (len(tr_res) > 0):
            print(f"Anda sudah memesan kelas dengan ID Detail Kelas: {id_detail_kelas}. Harap memesan kelas yang lain.")
            return

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
                confirmation = input(f"Apakah anda yakin ingin memesan kelas ini? (Y/N) atau ketik 0 untuk kembali: ")
                
                if confirmation.lower() == 'y':
                    try:
                        cursor.execute(''' 
                        INSERT INTO transaksi (nim, id_detail_kelas, email, tanggal_transaksi, status_transaksi, pengguna)
                        VALUES (%s, %s, %s, NOW(), 'Pengajuan Pending', %s)
                        ''', (nim, id_detail_kelas, email, pengguna.upper()))
                        conn.commit()

                        print("Pemesanan kelas berhasil. Pengajuan kelas akan ditujukan kepada akademik.")
                        valid_input = True

                    except mysql.connector.Error as err:
                        print(f"Error: Terjadi kesalahan, tidak dapat memesan kelas. {err}")

                elif confirmation.lower() == 'n':
                    print("Anda tidak jadi memesan kelas ini.")
                    valid_input = True

                elif confirmation == '0':
                    return

                else:
                    print("Input tidak valid.")
        else:
            print(f"Digunakan oleh {pengguna_baru}, tidak dapat memesan kelas ini.")

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

        if not results:
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
            SELECT transaksi.id_transaksi, transaksi.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.kode_dosen,  
                    detail_kelas.hari, detail_kelas.jam_mulai, detail_kelas.jam_selesai, transaksi.tanggal_transaksi, 
                    transaksi.pengguna, transaksi.status_transaksi
            FROM transaksi
            INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas
            WHERE transaksi.nim = %s AND transaksi.status_transaksi = 'Pengajuan Pending' OR transaksi.status_transaksi = 'ACC Pengajuan'
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
        id_transaksi = input("Masukkan ID Pesanan yang ingin dibatalkan atau ketik 0 untuk kembali: ").strip()

        if id_transaksi == '0':
            return

        try:
            # Verifikasi ID Transaksi yang dipilih
            cursor.execute('''
                SELECT * FROM transaksi WHERE id_transaksi = %s AND nim = %s
            ''', (id_transaksi, nim))
            transaksi_terpilih = cursor.fetchone()
            status_transaksi_terpilih = transaksi_terpilih[5]
        except:
            print("ID transaksi tidak ditemukan atau terjadi kesalahan.")
            return

        # Proses konfirmasi pembatalan
        confirmation = input(f"Apakah Anda yakin ingin membatalkan pesanan kelas ID {id_transaksi}? (Y/N) atau ketik 0 untuk kembali: ").lower()
        if confirmation.lower() == 'y':

            if status_transaksi_terpilih == "Pengajuan Pending":
                # Jika pesanan berstatus 'Pengajuan Pending', langsung batalkan
                cursor.execute(''' 
                UPDATE transaksi SET status_transaksi = 'Pengajuan Dibatalkan' WHERE id_transaksi = %s AND nim = %s
                ''', (id_transaksi, nim))
                conn.commit()
                print(f"Pesanan dengan ID {id_transaksi} berhasil dibatalkan.")
                return

            if status_transaksi_terpilih == "ACC Pengajuan":
                # Jika sudah di-ACC, ubah status menjadi 'Pembatalan Pending'
                cursor.execute(''' 
                UPDATE transaksi SET status_transaksi = 'Pembatalan Pending' WHERE id_transaksi = %s AND nim = %s
                ''', (id_transaksi, nim))
                conn.commit()
                print(f"Pengajuan pembatalan untuk ID {id_transaksi} berhasil diajukan. Menunggu konfirmasi admin.")
            else:
                print(f"Pesanan dengan ID {id_transaksi} tidak ditemukan atau tidak dapat dibatalkan. Status saat ini: {status_transaksi_terpilih}.")
                return
            
        elif confirmation.lower() == 'n':
            print("Pembatalan dibatalkan.")
        elif confirmation == '0':
            return
        else:
            print("Input tidak valid.")
    except mysql.connector.Error as err:
        print(f"Error: Terjadi kesalahan saat mengambil data transaksi. {err}")
        
def pengajuan(nim, email):
    cursor = conn.cursor()

    print("======= Pengajuan Pemakaian Kelas =======")
    pengguna = input("\nDiajukan oleh(0 untuk kembali): ").strip()
    if pengguna.lower() == "0":
        print("Kembali ke menu utama.")
        return

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

        # durasi = int(kategori_sks) * 50  # Durasi dalam menit

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

        cursor.execute("SELECT informasi_kelas FROM kelas WHERE kode_kelas = %s", (kode_kelas,))
        results = cursor.fetchone()

        if results is None:
            print("Kode kelas tidak ditemukan. Silakan periksa kembali.")
            return

        infoKelas = pengguna + " [ "+ kategori_sks + " SKS ]" + results[0]

        # Validasi kode_dosen dosen
        cursor.execute("SELECT nama FROM dosen WHERE kode_dosen = %s", (kode_dosen,))
        nama = cursor.fetchone()

        if nama is None:
            print("Kode dosen tidak ditemukan. Silakan periksa kembali.")
            return

        nama_dosen = nama[0]

        cursor.execute("""
            INSERT INTO pengajuan (nim, email, pengguna, kode_kelas, kode_dosen, nama_dosen, kode_matkul, hari, jam_mulai, jam_selesai, informasi_kelas, tgl_pengajuan, status_pengajuan)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 'Pengajuan Pending')
        """, (nim, email, pengguna, kode_kelas, kode_dosen, nama_dosen, kode_matkul, hari, jam_mulai, jam_selesai, infoKelas))

        conn.commit()

        print("Data pengajuan dikirim ke Akademik. Silahkan tunggu konfirmasi dari pihak terkait.")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def batal_pengajuan(nim):
    cursor = conn.cursor()
    
    try:
        # Tampilkan pesanan yang sudah ada (status 'Pending' atau 'Confirmed')
        print("\n--- Pesanan Kelas Anda ---")
        cursor.execute(''' 
            SELECT id_pengajuan, pengguna, kode_kelas, kode_dosen, nama_dosen, hari,
                jam_mulai, jam_selesai, tgl_pengajuan, status_pengajuan
            FROM pengajuan
            WHERE pengajuan.nim = %s AND status_pengajuan = 'Pengajuan Pending' OR status_pengajuan = 'ACC Pengajuan'
        ''', (nim,))
        result = cursor.fetchall()

        if not result:
            print("Tidak ada kelas yang dapat dibatalkan atau sudah dikonfirmasi.")
            return

        # Menampilkan daftar pesanan kelas yang dapat dibatalkan
        print("-" * 40)
        for row in result:
            print(f"ID Pesanan           : {row[0]}")
            print(f"Kode Kelas           : {row[2]}")
            print(f"Dosen                : {row[3]} - {row[4]}")
            print(f"Waktu Penggunaan     : {row[5]}, {row[6]} - {row[7]}")
            print(f"Tanggal Transaksi    : {row[8]}")
            print(f"Diajukan oleh        : {row[1]}")
            print(f"Status Transaksi     : {row[9]}")
            print("-" * 40)

        # Input ID Pesanan yang ingin dibatalkan
        id_pengajuan = input("Masukkan ID Pesanan yang ingin dibatalkan (ketik 0 untuk kembali): ").strip()

        if id_pengajuan == '0':
            return

        # Verifikasi ID Transaksi yang dipilih
        cursor.execute('''
            SELECT status_pengajuan FROM pengajuan WHERE id_pengajuan = %s AND nim = %s
        ''', (id_pengajuan, nim))
        pengajuan_terpilih = cursor.fetchone()
        status_pengajuan_terpilih = pengajuan_terpilih[0]

        if pengajuan_terpilih is None:
            print("ID Transaksi tidak ditemukan.")
            return

        # Proses konfirmasi pembatalan
        confirmation = input(f"Apakah Anda yakin ingin membatalkan pengajuan kelas ID {id_pengajuan}? (Y/N) atau ketik 0 untuk kembali: ").upper()
        if confirmation.upper() == 'Y':

            if status_pengajuan_terpilih == "Pengajuan Pending":
                # Jika pesanan berstatus 'Pengajuan Pending', langsung batalkan
                cursor.execute(''' 
                UPDATE pengajuan SET status_pengajuan = 'Pengajuan Dibatalkan' WHERE id_pengajuan = %s AND nim = %s
                ''', (id_pengajuan, nim))
                conn.commit()
                print(f"Pesanan dengan ID {id_pengajuan} berhasil dibatalkan.")
                return

            if status_pengajuan_terpilih == "ACC Pengajuan":
                # Jika sudah di-ACC, ubah status menjadi 'Pembatalan Pending'
                cursor.execute(''' 
                UPDATE pengajuan SET status_pengajuan = 'Pembatalan Pending' WHERE id_pengajuan = %s AND nim = %s
                ''', (id_pengajuan, nim))
                conn.commit()
                print(f"Pengajuan pembatalan untuk ID {id_pengajuan} berhasil diajukan. Menunggu konfirmasi admin.")
            else:
                print(f"Pesanan dengan ID {id_pengajuan} tidak ditemukan atau tidak dapat dibatalkan. Status saat ini: {status_pengajuan_terpilih}.")
                return
            
        elif confirmation.upper() == 'N':
            print("Pembatalan dibatalkan.")
        elif confirmation == '0':
            return
        else:
            print("Input tidak valid.")
    except mysql.connector.Error as err:
        print(f"Error: Terjadi kesalahan saat mengambil data transaksi. {err}")
    
def lihat_pesanan_kelas(NIM):
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
                SELECT transaksi.id_transaksi, transaksi.id_detail_kelas, detail_kelas.kode_kelas, detail_kelas.kode_matkul, 
                       detail_kelas.kode_dosen, detail_kelas.hari, detail_kelas.jam_mulai, detail_kelas.jam_selesai, transaksi.tanggal_transaksi, 
                       transaksi.pengguna, transaksi.status_transaksi, transaksi.komentar
                FROM transaksi 
                       INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas WHERE nim = {NIM}
                """)
        result = cursor.fetchall()
        
        if len(result) == 0:  # Jika tidak ada data
            print("Anda belum memiliki pesanan kelas.")
        else:
            print("\n[ Pesanan Saya ]")
            table = PrettyTable()
            table.field_names = [
                "ID Pesanan",
                "ID Detail Kelas", 
                "Kode Kelas",
                "Kode Mata Kuliah",
                "Kode Dosen",
                "Hari", 
                "Jam Mulai", 
                "Jam Selesai", 
                "Tanggal Transaksi", 
                "Status Transaksi",
            ]
            
            for i in result:
                table.add_row([
                    i[0],  # ID Pesanan
                    i[1],  # ID Detail Kelas
                    i[2],  # Kode Kelas
                    i[3],  # Kode Matkul
                    i[4],  # Kode Dosen
                    i[5],  # Hari
                    i[6],  # Jam Mulai
                    i[7],  # Jam Selesai
                    i[8],  # Tanggal Transaksi
                    i[10],   # Status Transaksi
                ])
            print(table)
                
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def lihat_pesanan_mandiri(NIM):
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT id_pengajuan, pengguna, kode_kelas, kode_matkul, kode_dosen, nama_dosen, hari,
                jam_mulai, jam_selesai, tgl_pengajuan, status_pengajuan
            FROM pengajuan WHERE nim = {NIM}
        """)
        result = cursor.fetchall()
        
        if len(result) == 0:  # Jika tidak ada data
            print("Anda belum memiliki pesanan kelas.")
        else:
            print("\n[ Pesanan Saya ]")
            table = PrettyTable()
            table.field_names = [
                "ID Pesanan",
                "Diajukan oleh",
                "Kode Kelas",
                "Kode Mata Kuliah",
                "Kode Dosen",
                "Dosen",
                "Hari", 
                "Jam Mulai", 
                "Jam Selesai", 
                "Tanggal Pengajuan", 
                "Status Pengajuan",
            ]
            
            for i in result:
                table.add_row([
                    i[0],  # ID Pesanan
                    i[1],  # Diajukan oleh
                    i[2],  # Kode Kelas
                    i[3],  # Kode Matkul
                    i[4],  # Kode Dosen
                    i[5],  # Nama Dosen
                    i[6],  # Hari
                    i[7],  # Jam Mulai
                    i[8],  # Jam Selesai
                    i[9],  # Tanggal Pengajuan
                    i[10], # Status Pengajuan
                ])
            print(table)
                
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()


def lihat_profil(NIM):
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
        SELECT * FROM users WHERE nim = '{NIM}'
        ''')
        res = cursor.fetchone()

        table = PrettyTable()
        table.field_names = ["Property", "Value"]
        table.add_row(["NIM", res[0]])
        table.add_row(["Email", res[1]])
        table.add_row(["Role", res[3]])
        print(table)

    except mysql.connector.Error as err:
        print("Profil tidak ditemukan atau terjadi kesalahan.")
    finally:
        cursor.close()