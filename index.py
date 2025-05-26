import csv
import hashlib
import re
import pandas as pd
import random
import os
from datetime import datetime

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
        print("[1] Hitung Menu")
        print("[2] Rekomendasi Menu")
        print("[3] History Konsumsi")
        print("[4] Rekomendasi Resep")
        print("[5] Visualisasi Konsumsi Kalori")
    elif level == "admin":
        print("[1] Kelola Rekomendasi Menu")
        print("[2] Kelola Rekomendasi Resep")
    else:
        print("Level tidak dikenali.")
        return

    pilihan = input("Pilih menu: ")

    if level == "pengguna":
        if pilihan == '0':
            show_profile(level, user_id)
        elif pilihan == '1':
            hitung_menu(level, user_id)
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

def hitung_menu(level, user_id):
    print("\n=== Hitung Menu ===")
    print("Ingin menginput menu secara:")
    print("[1] Manual")
    print("[2] Otomatis")

    pilihan = input("Pilih metode: ")

    if pilihan == "1":
        hitung_manual(level, user_id)
    elif pilihan == "2":
        hitung_otomatis(level, user_id)
    else:
        print("Pilihan tidak valid.")
        
def hitung_manual(level, user_id):
    print("\n=== Mode Manual ===")
    print("Pilih tujuan konsumsi:")
    print("[1] Diet (maks 1000 kalori)")
    print("[2] Normal (maks 1800 kalori)")
    print("[3] Bulking (maks 2500 kalori)")
    print("[0] Input jumlah kalori manual")

    pilihan = input("Pilihan: ")

    if pilihan == "1":
        batas_kalori = 1000
    elif pilihan == "2":
        batas_kalori = 1800
    elif pilihan == "3":
        batas_kalori = 2500
    elif pilihan == "0":
        try:
            batas_kalori = int(input("Masukkan batas kalori manual: "))
        except ValueError:
            print("❌ Input tidak valid.")
            return
    else:
        print("❌ Pilihan tidak valid.")
        return

    def input_manual_menu():
        print("\n=== Input Menu Manual ===")
        print("Masukkan daftar makanan dan jumlah kalorinya.")
        print("Ketik 'n' jika sudah selesai.\n")

        makanan_list = []

        while True:
            makanan = input("Nama Makanan: ")
            if makanan.lower() == 'n':
                break

            try:
                kalori = int(input("Jumlah Kalori: "))
            except ValueError:
                print("❌ Kalori harus berupa angka!")
                continue

            makanan_list.append({"makanan": makanan, "kalori": kalori})

            lanjut = input("Ingin tambah makanan lagi? (y untuk lanjut, n untuk berhenti): ")
            if lanjut.lower() == 'n':
                break

        return makanan_list

    makanan_list = input_manual_menu()

    total_kalori = sum(item["kalori"] for item in makanan_list)

    print("\n📋 Daftar Makanan yang Dimasukkan:")
    for item in makanan_list:
        print(f"- {item['makanan']} ({item['kalori']} kkal)")

    print(f"\n✅ Total Kalori: {total_kalori} dari batas {batas_kalori} kkal")

    if total_kalori <= batas_kalori:
        print("✅ Menu sesuai dengan target kalori.")
    else:
        print("⚠️  Menu melebihi target kalori.")

        # 🧠 Tambahkan solusi knapsack jika melebihi batas
        n = len(makanan_list)
        W = batas_kalori

        # Buat tabel DP
        dp = [[0] * (W + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            kal = makanan_list[i - 1]['kalori']
            for w in range(W + 1):
                if kal <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - kal] + kal)
                else:
                    dp[i][w] = dp[i - 1][w]

        # Traceback untuk mencari item yang dipilih
        w = W
        selected_items = []
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(makanan_list[i - 1])
                w -= makanan_list[i - 1]['kalori']

        selected_items.reverse()

        print("\n💡 Rekomendasi Menu Terbaik (Knapsack ≤ batas kalori):")
        for item in selected_items:
            print(f"- {item['makanan']} ({item['kalori']} kkal)")
        print(f"\n✅ Total Kalori Optimal: {sum(item['kalori'] for item in selected_items)} kkal")
        simpan = input("\n💾 Apakah ingin menyimpan hasil ke history? (y/n): ")
        if simpan.lower() == 'y':
            kebutuhan = "manual"
            simpan_ke_history(user_id, makanan_list, kebutuhan)
            print("✅ Disimpan ke history.csv")
        else:
            print("❌ Tidak disimpan.")
        show_menu(level, user_id)
    
def hitung_otomatis(level, user_id):
    print("\n=== Mode Otomatis ===")
    print("Pilih tujuan konsumsi:")
    print("[1] Diet")
    print("[2] Normal")
    print("[3] Bulking")

    pilihan = input("Pilihan: ")

    try:
        kalori_df = pd.read_csv("kalori.csv")
        menu_df = pd.read_csv("menu.csv")
    except:
        print("❌ Gagal membaca file kalori.csv atau menu.csv")
        return

    if pilihan == "1":
        target = "diet"
    elif pilihan == "2":
        target = "normal"
    elif pilihan == "3":
        target = "bulking"
    else:
        print("Pilihan tidak valid.")
        return

    batas = kalori_df[kalori_df['jenis'] == target]['jumlah maks kalori'].values
    if len(batas) == 0:
        print("❌ Tidak ditemukan data kalori untuk kategori tersebut.")
        return

    batas_kalori = batas[0]
    print(f"\nTarget Kalori Maksimum: {batas_kalori} kkal")

    menu_df_sorted = menu_df.sort_values(by='kalori', ascending=False)

    selected = []
    total = 0

    for _, row in menu_df_sorted.iterrows():
        if total + row['kalori'] <= batas_kalori:
            selected.append({"makanan": row['makanan'], "kalori": row['kalori']})
            total += row['kalori']

    print("\n📋 Menu Rekomendasi Berdasarkan Knapsack Greedy:")
    for item in selected:
        print(f"- {item['makanan']} ({item['kalori']} kkal)")

    print(f"\n✅ Total kalori: {total} / {batas_kalori}")

    # Tawarkan simpan ke history
    simpan = input("\n💾 Apakah ingin menyimpan hasil ke history? (y/n): ")
    if simpan.lower() == 'y':
        simpan_ke_history(user_id, selected, target)
        print("✅ Disimpan ke history.csv")
    else:
        print("❌ Tidak disimpan.")

def simpan_ke_history(user_id, makanan_list, kebutuhan):
    import pandas as pd
    import os
    from datetime import datetime

    if os.path.exists("history.csv"):
        try:
            data_df = pd.read_csv("history.csv")
            # Pastikan kolom 'id' ada
            if 'id' not in data_df.columns:
                # Jika kolom 'id' tidak ada, beri nama kolom secara manual
                data_df = pd.read_csv("history.csv", header=None)
                data_df.columns = ["id", "user_id", "tanggal", "makanan dan kalori", "kebutuhan"]
        except Exception as e:
            print(f"Error membaca CSV: {e}")
            data_df = pd.DataFrame(columns=["id", "user_id", "tanggal", "makanan dan kalori", "kebutuhan"])
        data_id = data_df["id"].max() + 1 if not data_df.empty else 1
    else:
        data_df = pd.DataFrame(columns=["id", "user_id", "tanggal", "makanan dan kalori", "kebutuhan"])
        data_id = 1

    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    makanan_str = ', '.join([f"{item['makanan']} ({item['kalori']})" for item in makanan_list])

    data = {
        "id": [data_id],
        "user_id": [user_id],
        "tanggal": [tanggal],
        "makanan dan kalori": [makanan_str],
        "kebutuhan": [kebutuhan]
    }

    df_baru = pd.DataFrame(data)

    df_baru.to_csv("history.csv", mode='a', header=not os.path.exists("history.csv"), index=False)

        
# Jalankan program
if __name__ == "__main__":
    main_menu()