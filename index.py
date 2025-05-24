import csv
import hashlib
import re
import pandas as pd

def id_berikutnya(filename):
    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                return int(rows[-1][0]) + 1
    except FileNotFoundError:
        pass
    return 1

def main_menu():
    print("\n=== Selamat Datang di Kaloria ===")
    print("[1] Registrasi")
    print("[2] Login")
    print("[3] Keluar")
    pilihan = input("Pilih: ")

    if pilihan == '1':
        register()
    elif pilihan == '2':
        login()
    elif pilihan == '3':
        print("Sampai jumpa!")
        exit()
    else:
        print("Pilihan tidak valid.")
        main_menu()

def register():
    print("=== Registrasi ===")
    
    try:
        users_df = pd.read_csv("users.csv", header=None)
        users_df.columns = ["user_id", "nama", "email", "password", "nomor_hp", "level"]
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=["user_id", "nama", "email", "password", "nomor_hp", "level"])

    
    user_id = 1 if users_df.empty else users_df["user_id"].max() + 1

    nama = input("Masukkan Nama: ")
    email = input("Masukkan Email: ")
    password = input("Masukkan Password: ")
    nomor_hp = input("Masukkan Nomor HP: ")
    level = "pengguna"

    password = hashlib.sha256(password.encode()).hexdigest()

    new_user = pd.DataFrame({
        "user_id": [user_id],
        "nama": [nama],
        "email": [email],
        "password": [password],
        "nomor_hp": [nomor_hp],
        "level": [level]
    })

    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_csv("users.csv", index=False, header=False)

    print("Registrasi berhasil! Silakan login.")
    main_menu()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def login():
    print("=== Login ===")
    email = input("Masukkan Email: ").strip()
    password = input("Masukkan Password: ").strip()

    if not is_valid_email(email):
        print("Format email tidak valid. Silakan coba lagi.")
        login()
        return

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        with open("users.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == email and row[3] == password_hash:
                    print(f"Login berhasil! Selamat datang, {row[1]}")
                    show_menu(row[5], row[0])
                    return
    except FileNotFoundError:
        print("Belum ada data pengguna. Silakan registrasi.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    print("Email atau password salah. Coba lagi.")
    main_menu()

def show_menu(level, user_id):
    print("\n=== Menu Utama ===")
    print("[0] Profil")

    if level == "pengguna":
        print("[1] Layanan A")
        print("[2] Layanan B")
    elif level == "admin":
        print("[1] Laporan Sistem")
        print("[2] Kelola Pengguna")
    else:
        print("Level tidak dikenali.")
        return

    pilihan = input("Pilih menu: ")

    if pilihan == '0':
        show_profile(level, user_id)
    elif pilihan in ['1', '2']:
        print("Fitur ini masih dalam pengembangan.")
        show_menu(level, user_id)
    else:
        print("Pilihan tidak valid.")
        show_menu(level, user_id)

def show_profile(level, user_id):
    try:
        with open('users.csv', 'r') as file:
            users = list(csv.reader(file))

        user_index = next((i for i, u in enumerate(users) if u[0] == user_id), None)
        if user_index is None:
            print("Pengguna tidak ditemukan.")
            return

        user = users[user_index]

        print("\n=== Profil ===")
        print(f"ID Pengguna: {user[0]}")
        print(f"Nama: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"Nomor HP: {user[4]}")
        print(f"Role: {user[5]}")
        print("=" * 30)

        print("[1] Ubah Nama")
        print("[2] Ubah Email")
        print("[3] Ubah Nomor HP")
        print("[0] Kembali")
        print("[9] Logout")
        pilihan = input("Pilih: ")

        if pilihan == '1':
            new_name = input("Nama baru: ")
            users[user_index][1] = new_name
        elif pilihan == '2':
            new_email = input("Email baru: ")
            users[user_index][2] = new_email
        elif pilihan == '3':
            new_hp = input("Nomor HP baru: ")
            users[user_index][4] = new_hp
        elif pilihan == '0':
            show_menu(level, user_id)
            return
        elif pilihan == '9':
            print("Logout berhasil.")
            main_menu()
            return
        else:
            print("Pilihan tidak valid.")
            show_menu(level, user_id)
            return

        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)

        print("Data berhasil diperbarui.")
        show_menu(level, user_id)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Jalankan program
if __name__ == "__main__":
    main_menu()