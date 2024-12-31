""" Inisialisasi untuk program CLI karena password MySQL nya beda-beda """

""" 
Jalankan ini paling pertama terlebih dahulu setelah melakukan git clone, 
git pull, update kodingan terbaru, atau sekedar ingin update value password MySQL

Default password untuk MySQL adalah "" atau tidak ada.
"""

from create_db import create_database
from create_tb import create_table
from delete_db import delete_database
from seed_db import seed_database

from prettytable import PrettyTable
import os

os.system("cls")
while True:
    print("=== Initialize CLI setup for E-Booking Class ===")
    main_table = PrettyTable()
    main_table.align = "l"
    main_table.field_names = ["No", "Action"]
    main_table.add_row(["1", "Ganti password MySQL"])
    main_table.add_row(["2", "Buat database baru beserta tabelnya"])
    main_table.add_row(["3", "Isi database dengan data dummy"])
    main_table.add_row(["4", "Hapus database"])
    main_table.add_row(["0", "Exit"])
    print(main_table)
    
    action_option = str(input("Pilih opsi [1/2/3/4/0]: ")).strip()
    
    # Ganti Password
    if action_option == "1":
        while True:
            opsi_ganti_password = input("Apakah anda ingin mengganti password MySQL? (Y/N)\n>")
            if (opsi_ganti_password.lower() == "y"):
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
                break
            elif (opsi_ganti_password.lower() == "n"):
                print("Anda tidak jadi merubah password MySQL.")
                break
            else:
                print("Harap masukkan input yang valid.")
                
    # Membuat Database dan Tabel
    elif action_option == "2":
        while True:
            opsi_migrate_db_dan_table = input("Apakah anda ingin membuat database bernama 'ebookingclass' beserta tabel nya? (Y/N)\n> ")
            if (opsi_migrate_db_dan_table.lower() == "y"):
                create_database()
                print('|')
                create_table()
                print('|')
                print('Database dan tabel berhasil dibuat.')
                break
            elif (opsi_migrate_db_dan_table.lower() == "n"):
                print("Anda tidak jadi membuat database dan tabel.")
                break
            else:
                print("Harap masukkan input yang valid.")
    
    # Mengisi Database dengan Data Dummy
    elif action_option == "3":
        while True:
            # opsi apakah user ingin mengisi database dengan data dummy yang sudah disediakan.
            opsi_seeding_database = input("Apakah anda ingin mengisi database dengan data dummy? (Y/N)\n>")
            if (opsi_seeding_database.lower() == "y"):
                seed_database()
                break
            elif (opsi_seeding_database.lower() == "n"):
                print("Anda tidak jadi mengisi database.")
                break
            else:
                print("Harap masukkan input yang valid.")
    
    # Menghapus Database
    elif action_option == "4":
        while True:
            opsi_hapus_db = input("Apakah anda ingin menghapus database bernama 'ebookingclass'? (Y/N)\n>")
            if (opsi_hapus_db.lower() == "y"):
                delete_database()
                break
            elif (opsi_hapus_db.lower() == "n"):
                print("Anda tidak jadi menghapus database.")
                break
            else:
                print("Harap masukkan input yang valid.")
    elif action_option == "0":
        print("Inisialisasi setup CLI selesai.")
        break
    else:
        print("Harap masukkan input yang valid.")