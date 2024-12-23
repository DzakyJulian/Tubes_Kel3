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
    id_detail_kelas = input("Masukkan ID Detail Kelas yang ingin diajukan (bukan kode kelas): ").strip()
    try:
        valid_input = False
        while valid_input == False:
            confirmation = input(f"Apakah anda yakin ingin memesan kelas ini? (Y/N): ")
            
            if (confirmation.lower() == 'y'):
                cursor.execute('''
                INSERT INTO transaksi (nim, id_detail_kelas, email, tanggal_transaksi, status_transaksi)
                VALUES (%s, %s, %s, NOW(), 'Pending')
                ''', (nim, id_detail_kelas, email))
                conn.commit()
                print("Pemesanan kelas berhasil. Pengajuan kelas akan ditujukan kepada akademik.")
                break
            elif (confirmation.lower() == 'n'):
                print("Anda tidak jadi memesan kelas ini.")
                break
            else:
                print("Input tidak valid.")
    except mysql.connector.Error as err:
        print(f"Error: Terjadi kesalahan, tidak dapat memesan kelas.")
    finally:
        cursor.close()

def lihat_pesanan_saya(NIM):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM transaksi INNER JOIN detail_kelas ON transaksi.id_detail_kelas = detail_kelas.id_detail_kelas WHERE nim = \"{NIM}\" ")
        result = cursor.fetchall()
        
        if (len(result) == 0):
            print("Anda belum memiliki pesanan kelas.")
        else:
            print("============== Pesanan Saya =================")
            for i in result:
                print(f"ID Pesanan           : {i[0]}")
                print(f"ID Detail Kelas      : {i[1]}")
                print(f"Kode Kelas           : {i[8]}")
                print(f"Jam Mulai            : {i[11]}")
                print(f"Jam Selesai          : {i[12]}")
                print(f"Tanggal Transaksi    : {i[4]}")
                print(f"Status Transaksi     : {i[5]}")
                print("=============================================")
                
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")