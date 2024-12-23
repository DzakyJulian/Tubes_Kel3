import mysql.connector
from admin_db_info import get_current_mysql_password

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=get_current_mysql_password(),
    database="ebookingclass"
)

def ajukan_kelas(NIM):
    cursor = conn.cursor()
    id_detail_kelas = input("Masukkan ID Detail Kelas yang ingin diajukan (bukan kode kelas): ").strip()
    try:
        valid_input = False
        while valid_input == False:
            confirmation = input(f"Apakah anda yakin ingin memesan kelas ini? (Y/N): ")
            
            if (confirmation.lower() == 'y'):
                cursor.execute('''
                INSERT INTO transaksi (nim, id_detail_kelas, tanggal_transaksi, status_transaksi)
                VALUES (%s, %s, NOW(), 'Pending')
                ''', (NIM, id_detail_kelas))
                conn.commit()
                print("Pemesanan kelas berhasil. Pengajuan kelas akan ditujukan kepada akademik.")
                break
            elif (confirmation.lower() == 'n'):
                print("Anda tidak jadi memesan kelas ini.")
                break
            else:
                print("Input tidak valid.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# def lihat_pesanan_saya(NIM):
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute('''
#         SELECT * FROM 
#         ''')