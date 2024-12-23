""" Inisialisasi untuk program CLI karena password MySQL nya beda-beda """

""" 
Jalankan ini paling pertama terlebih dahulu setelah melakukan git clone, 
git pull, update kodingan terbaru, atau sekedar ingin update value password MySQL

Default password untuk MySQL adalah "" atau tidak ada.
"""

from create_db import create_database
from create_tb import create_table
import os

os.system("cls")
print("===== Initialize CLI setup for E-Booking Class =====")

# ambil semua value dari file "admin_db_info"
with open("admin_db_info.txt", mode="r") as file:
    content = file.readlines()

# ganti password nya menjadi yang terbaru (yang diinput oleh user)
current_mysql_password = str(input("Password MySQL anda (kosongkan jika tidak ada): "))
content[2] = f"password=\"{current_mysql_password}\"\n" # content[2] isinya: password=""

# update content pada file admin_db_info
with open("admin_db_info.txt", mode="w") as file:
    file.writelines(content)
print("Password MySQL berhasil diubah.")

# opsi apakah user ingin membuat database dan tabel secara otomatis
# ini akan menjalankan fungsi create_database dan create_table
opsi_migrate_db_dan_table = input("Apakah anda ingin membuat database bernama 'ebookingclass' beserta tabel nya? (Y/N)\n> ")
if (opsi_migrate_db_dan_table.lower() == "y"):
    create_database()
    print('|')
    create_table()
    print('|')
    print('Database dan tabel berhasil dibuat.')
    print("Initialize CLI setup telah selesai.")
    
elif (opsi_migrate_db_dan_table.lower() == "n"):
    print("Database dan tabel tidak akan dibuat.")
    print("Initialize CLI setup telah selesai.")

else:
    print("Input tidak valid. Exiting the initialize CLI setup.")