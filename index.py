import csv
import hashlib
import re
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re
import os

# FABYAN
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
    os.system('cls')
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
    os.system('cls')
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
    os.system('cls')
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
                    os.system ('cls')
                    return
    except FileNotFoundError:
        print("Belum ada data pengguna. Silakan registrasi.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    print("Email atau password salah. Coba lagi.")
    os.system ('cls')
    main_menu()

def show_menu(level, user_id):
    os.system('cls')
    print("\n=== Menu Utama ===")
    print("[0] Profil")

    if level == "pengguna":
        print("[1] Hitung Menu")
        print("[2] History Konsumsi")
        print("[3] Rekomendasi Resep")
        print("[4] Visualisasi Konsumsi Kalori")
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
        elif pilihan == '2':
            history_konsumsi(level, user_id)
        elif pilihan == '3':
            rekomendasi_resep(level, user_id)
        elif pilihan == '4':
            visualisasi_konsumsi_kalori(level, user_id)
        else:
            print("Pilihan tidak valid.")
            show_menu(level, user_id)
    else:
        if pilihan == '0':
            show_profile(level, user_id)
        elif pilihan == '1':
            kelola_rekomendasi_menu(level, user_id)
        elif pilihan == '2':
            kelola_rekomendasi_resep(level, user_id)
        else:
            print("Pilihan tidak valid.")
            show_menu(level, user_id)
            

def show_profile(level, user_id):
    os.system('cls')
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
    os.system('cls')
    print("\n=== Hitung Menu ===")
    print("Ingin menginput menu secara:")
    print("[1] Manual")
    print("[2] Otomatis")
    print("[3] Kembali")

    pilihan = input("Pilih metode: ")

    if pilihan == "1":
        hitung_manual(level, user_id)
    elif pilihan == "2":
        hitung_otomatis(level, user_id)
    elif pilihan == "3":
        show_menu(level, user_id)
    else:
        print("Pilihan tidak valid.")
     
# NISA
def hitung_manual(level, user_id):
    os.system('cls')
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
        os.system ('cls')
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

        n = len(makanan_list)
        W = batas_kalori

        dp = [[0] * (W + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            kal = makanan_list[i - 1]['kalori']
            for w in range(W + 1):
                if kal <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - kal] + kal)
                else:
                    dp[i][w] = dp[i - 1][w]

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
            show_menu(level, user_id)
        else:
            print("❌ Tidak disimpan.")
            show_menu(level, user_id)
    
def hitung_otomatis(level, user_id):
    os.system('cls')
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
        os.system ('cls')
        target = "diet"
    elif pilihan == "2":
        os.system ('cls')
        target = "normal"
    elif pilihan == "3":
        os.system ('cls')
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

    simpan = input("\n💾 Apakah ingin menyimpan hasil ke history? (y/n): ")
    if simpan.lower() == 'y':
        simpan_ke_history(user_id, selected, target)
        print("✅ Disimpan ke history.csv")
    else:
        print("❌ Tidak disimpan.")
    show_menu(level, user_id)
    
def simpan_ke_history(user_id, makanan_list, kebutuhan):
    os.system('cls')

    if os.path.exists("history.csv"):
        try:
            data_df = pd.read_csv("history.csv")
            if 'id' not in data_df.columns:
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

    with open("history.csv", mode='a', newline='', encoding='utf-8') as f:
        df_baru.to_csv(f, header=f.tell() == 0, index=False)
        
def history_konsumsi(level, user_id):
    os.system('cls')

    print("\n=== Riwayat Konsumsi Kalori ===")
    try:
        if not os.path.exists("history.csv"):
            print("❌ File history.csv tidak ditemukan.")
            return show_menu(level, user_id)

        df = pd.read_csv("history.csv", names=["id", "user_id", "tanggal", "menu (kalori)", "kebutuhan"], header=0)

        user_history = df[df['user_id'] == int(user_id)]

        if user_history.empty:
            print("❌ Belum ada riwayat konsumsi untuk pengguna ini.")
        else:
            for index, row in user_history.iterrows():
                print(f"\n🧾 ID: {row['id']}")
                print(f"📅 Tanggal: {row['tanggal']}")
                print(f"🍽️  Menu: {row['menu (kalori)']}")
                print(f"🎯 Kebutuhan: {row['kebutuhan']}")

            hapus = input("\n🗑️ Apakah kamu ingin menghapus salah satu data? (y/n): ").lower()
            if hapus == 'y':
                try:
                    id_hapus = int(input("Masukkan ID data yang ingin dihapus: "))
                    if id_hapus in user_history['id'].values:
                        df = df[df['id'] != id_hapus] 
                        df.to_csv("history.csv", index=False)
                        print("✅ Data berhasil dihapus.")
                    else:
                        print("❌ ID tidak ditemukan dalam riwayat kamu.")
                except ValueError:
                    print("❌ Masukan ID harus berupa angka.")
    except KeyError as e:
        print(f"❌ Kolom yang dibutuhkan tidak ditemukan: {e}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

    show_menu(level, user_id)

def rekomendasi_resep(level, user_id):
    os.system('cls')
    print("\n=== Rekomendasi Resep ===")
    try:
        df = pd.read_csv("resep.csv")

        print("Pilih kategori kebutuhan:")
        print("1. Diet (maks 1000 kalori)")
        print("2. Bulking (maks 2500 kalori)")
        print("3. Normal (maks 1800 kalori)")
        print("4. Input batas kalori sendiri")
        print("5. Kembali")

        pilihan = input("Masukkan pilihan (1-4): ")

        kebutuhan = ""
        max_kalori = 0

        if pilihan == '1':
            kebutuhan = "diet"
            max_kalori = 1000
        elif pilihan == '2':
            kebutuhan = "bulking"
            max_kalori = 2500
        elif pilihan == '3':
            kebutuhan = "normal"
            max_kalori = 1800
        elif pilihan == '4':
            kebutuhan = None
        elif pilihan == '5':
            show_menu(level, user_id)
            try:
                max_kalori = int(input("Masukkan batas maksimal kalori: "))
            except ValueError:
                print("❌ Input kalori tidak valid.")
                return
        else:
            print("❌ Pilihan tidak valid.")
            return

        filtered = df.copy()

        if kebutuhan:
            filtered = filtered[filtered['kebutuhan'].str.lower() == kebutuhan.lower()]

        filtered['kalori'] = filtered['nama makanan'].str.extract(r"\((\d+)\)").astype(float)
        filtered = filtered[filtered['kalori'] <= max_kalori]

        if filtered.empty:
            print("❌ Tidak ada resep yang cocok.")
        else:
            resep_terpilih = filtered.sample(n=1).iloc[0]
            print("\n🎉 Resep Rekomendasi:")
            print(f"🍽️  Nama Makanan: {resep_terpilih['nama makanan']}")
            print(f"📋 Bahan: {resep_terpilih['resep']}")
            print("👨‍🍳 Cara Masak:")
            print(resep_terpilih['cara_masak'].replace("\\n", "\n"))
            print(f"🎯 Kebutuhan: {resep_terpilih['kebutuhan']}")
            print(f"🔥 Kalori: {int(resep_terpilih['kalori'])} kalori")

    except FileNotFoundError:
        print("❌ File resep.csv tidak ditemukan.")
    except KeyError as e:
        print(f"❌ Kolom tidak ditemukan: {e}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
    show_menu(level, user_id)
    
def visualisasi_konsumsi_kalori(level, user_id):
    os.system('cls')
    try:
        df = pd.read_csv("history.csv")

        df['tanggal'] = pd.to_datetime(df['tanggal'])

        df['user_id'] = df['user_id'].astype(int)
        df['tanggal'] = pd.to_datetime(df['tanggal'])

        now = datetime.now()
        one_week_ago = now - timedelta(days=7)

        df_filtered = df[(df['user_id'] == int(user_id)) & (df['tanggal'] >= one_week_ago)]
    
        if df_filtered.empty:
            print("❌ Tidak ada data konsumsi dalam 7 hari terakhir.")
            show_menu(level, user_id)
            return

        def extract_total_calories(menu_string):
            angka = re.findall(r'\((\d+)\)', menu_string)
            total = sum([int(kal) for kal in angka])
            return total

        df_filtered['total_kalori'] = df_filtered['menu (kalori)'].apply(extract_total_calories)

        df_grouped = df_filtered.groupby(df_filtered['tanggal'].dt.date)['total_kalori'].sum()

        # Plot grafik
        plt.figure(figsize=(10, 5))
        df_grouped.plot(kind='bar', color='skyblue')
        plt.title('Konsumsi Kalori 7 Hari Terakhir')
        plt.xlabel('Tanggal')
        plt.ylabel('Total Kalori')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig("grafik_kalori.png")
        plt.show()

    except FileNotFoundError:
        print("❌ File history.csv tidak ditemukan.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
    
# WINSA
# Admin Role
def kelola_rekomendasi_menu(level, user_id):
    os.system('cls')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("📋 === Kelola Rekomendasi Menu ===")
        
        if not os.path.exists("menu.csv"):
            print("⚠️  File menu.csv tidak ditemukan. Membuat file baru...")
            df = pd.DataFrame(columns=["id", "makanan", "kalori"])
            df.to_csv("menu.csv", index=False)
        else:
            df = pd.read_csv("menu.csv", usecols=["id", "makanan", "kalori"])

        if df.empty:
            print("📭 Belum ada data menu yang tersedia.")
        else:
            print("\n📑 Daftar Menu:")
            print(df.to_string(index=False))

        print("\n✨ Pilihan:")
        print("[1] ➕ Tambah Menu Baru")
        print("[2] ✏️  Edit Menu yang Ada")
        print("[3] 🗑️  Hapus Menu")
        print("[0] 🔙 Kembali ke Menu Utama")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == "1":
            tambah_menu(df)
        elif pilihan == "2":
            edit_menu(df)
        elif pilihan == "3":
            hapus_menu(df)
        elif pilihan == "0":
            print("🔙 Kembali ke Menu Admin...\n")
            show_menu(level, user_id)
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")
            input("Tekan Enter untuk melanjutkan...")

def tambah_menu(df):
    os.system('cls')
    print("\n📥 Tambah Menu Baru")
    makanan = input("Masukkan nama makanan: ")
    kalori = input("Masukkan jumlah kalori: ")

    try:
        kalori = int(kalori)
        id_baru = df["id"].max() + 1 if not df.empty else 1
        df.loc[len(df)] = [id_baru, makanan, kalori]
        df.to_csv("menu.csv", index=False)
        print("✅ Menu berhasil ditambahkan!")
    except ValueError:
        print("❌ Kalori harus berupa angka.")

    input("Tekan Enter untuk kembali...")

def edit_menu(df):
    os.system('cls')
    print("\n✏️ Edit Menu")
    try:
        id_edit_input = input("Masukkan ID menu yang ingin diedit: ")
        if not id_edit_input.strip():
            print("❌ ID tidak boleh kosong.")
            input("Tekan Enter untuk kembali...")
            return

        id_edit = int(id_edit_input)
        if id_edit in df["id"].values:
            makanan_lama = df.loc[df["id"] == id_edit, "makanan"].values[0]
            kalori_lama = df.loc[df["id"] == id_edit, "kalori"].values[0]

            makanan_baru = input(f"Masukkan nama makanan baru (kosongkan untuk tetap '{makanan_lama}'): ")
            kalori_input = input(f"Masukkan kalori baru (kosongkan untuk tetap '{kalori_lama}'): ")

            makanan_final = makanan_baru.strip() if makanan_baru.strip() else makanan_lama
            kalori_final = int(kalori_input) if kalori_input.strip() else kalori_lama

            df.loc[df["id"] == id_edit, ["makanan", "kalori"]] = [makanan_final, kalori_final]
            df.to_csv("menu.csv", index=False)
            print("✅ Menu berhasil diperbarui!")
        else:
            print("❌ ID tidak ditemukan.")
    except ValueError:
        print("❌ Input tidak valid. Harus berupa angka.")
    input("Tekan Enter untuk kembali...")

def hapus_menu(df):
    os.system('cls')
    print("\n🗑️ Hapus Menu")
    try:
        id_hapus = int(input("Masukkan ID menu yang ingin dihapus: "))
        if id_hapus in df["id"].values:
            df = df[df["id"] != id_hapus]
            df.to_csv("menu.csv", index=False)
            print("🗑️ Menu berhasil dihapus.")
        else:
            print("❌ ID tidak ditemukan.")
    except ValueError:
        print("❌ Input tidak valid.")
    input("Tekan Enter untuk kembali...")
    
def kelola_rekomendasi_resep(level, user_id):
    os.system('cls')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("📋 === Kelola Rekomendasi Resep ===")
        
        if not os.path.exists("resep.csv"):
            print("⚠️  File resep.csv tidak ditemukan. Membuat file baru...")
            df = pd.DataFrame(columns=["id", "nama makanan", "resep", "cara_masak", "kebutuhan"])
            df.to_csv("resep.csv", index=False)
        else:
            df = pd.read_csv("resep.csv")

        if df.empty:
            print("📭 Belum ada data resep yang tersedia.")
        else:
            print("\n📑 Daftar Resep:")
            for _, row in df.iterrows():
                print(f"ID: {row['id']}")
                print(f"Nama Makanan: {row['nama makanan']}")
                print(f"Bahan-bahan: {row['resep']}")
                print("Cara Masak:")
                for line in str(row['cara_masak']).split('\\n'):
                    print(f"  {line.strip()}")
                print(f"Kebutuhan: {row['kebutuhan']}")
                print("-" * 40)

        print("\n✨ Pilihan:")
        print("[1] ➕ Tambah Resep Baru")
        print("[2] ✏️  Edit Resep yang Ada")
        print("[3] 🗑️  Hapus Resep")
        print("[0] 🔙 Kembali ke Menu Utama")

        pilihan = input("Masukkan pilihan Anda: ")

        if pilihan == "1":
            tambah_resep(df)
        elif pilihan == "2":
            edit_resep(df)
        elif pilihan == "3":
            hapus_resep(df)
        elif pilihan == "0":
            print("🔙 Kembali ke Menu Admin...\n")
            break
        else:
            print("❌ Pilihan tidak valid. Coba lagi.")
            input("Tekan Enter untuk melanjutkan...")

def tambah_resep(df):
    os.system('cls')
    print("\n📥 Tambah Resep Baru")
    nama = input("Masukkan nama makanan: ")
    resep = input("Masukkan bahan-bahan (pisahkan dengan koma): ")
    
    print("Masukkan cara masak (satu per baris):")
    cara_masak_list = []
    while True:
        step = input(f"  Langkah {len(cara_masak_list)+1}: ")
        if step.strip() != "":
            cara_masak_list.append(step.strip())
        lanjut = input("Apakah lanjut? (y/n): ").lower()
        if lanjut != 'y':
            break
    cara_masak = "\\n".join(cara_masak_list)

    kebutuhan = ""
    while kebutuhan not in ['normal', 'diet', 'bulking']:
        kebutuhan = input("Masukkan kebutuhan (normal/diet/bulking): ").lower()
    
    id_baru = df["id"].max() + 1 if not df.empty else 1
    df.loc[len(df)] = [id_baru, nama, resep, cara_masak, kebutuhan]
    df.to_csv("resep.csv", index=False)
    print("✅ Resep berhasil ditambahkan!")
    input("Tekan Enter untuk kembali...")

def edit_resep(df):
    os.system('cls')
    print("\n✏️ Edit Resep")
    try:
        id_edit_input = input("Masukkan ID resep yang ingin diedit: ")
        if not id_edit_input.strip():
            print("❌ ID tidak boleh kosong.")
            input("Tekan Enter untuk kembali...")
            return

        id_edit = int(id_edit_input)
        if id_edit in df["id"].values:
            nama_lama = df.loc[df["id"] == id_edit, "nama makanan"].values[0]
            resep_lama = df.loc[df["id"] == id_edit, "resep"].values[0]
            cara_masak_lama = df.loc[df["id"] == id_edit, "cara_masak"].values[0]
            kebutuhan_lama = df.loc[df["id"] == id_edit, "kebutuhan"].values[0]

            nama_baru = input(f"Nama makanan baru (kosongkan untuk tetap '{nama_lama}'): ")
            resep_baru = input(f"Bahan-bahan baru (kosongkan untuk tetap '{resep_lama}'): ")

            print("Masukkan cara masak baru (kosongkan untuk tetap cara masak lama):")
            cara_masak_list = []
            while True:
                step = input(f"  Langkah {len(cara_masak_list)+1}: ")
                if step.strip() != "":
                    cara_masak_list.append(step.strip())
                else:
                    if len(cara_masak_list) == 0:
                        break
                lanjut = input("Apakah lanjut? (y/n): ").lower()
                if lanjut != 'y':
                    break
            if len(cara_masak_list) > 0:
                cara_masak_baru = "\\n".join(cara_masak_list)
            else:
                cara_masak_baru = cara_masak_lama

            kebutuhan_baru = input(f"Kebutuhan baru (normal/diet/bulking) (kosongkan untuk tetap '{kebutuhan_lama}'): ").lower()
            if kebutuhan_baru not in ['normal', 'diet', 'bulking']:
                kebutuhan_baru = kebutuhan_lama

            nama_final = nama_baru if nama_baru.strip() else nama_lama
            resep_final = resep_baru if resep_baru.strip() else resep_lama

            df.loc[df["id"] == id_edit, ["nama makanan", "resep", "cara_masak", "kebutuhan"]] = [nama_final, resep_final, cara_masak_baru, kebutuhan_baru]
            df.to_csv("resep.csv", index=False)
            print("✅ Resep berhasil diperbarui!")
        else:
            print("❌ ID tidak ditemukan.")
    except ValueError:
        print("❌ Input tidak valid. Harus berupa angka.")
    input("Tekan Enter untuk kembali...")

def hapus_resep(df):
    os.system('cls')
    print("\n🗑️ Hapus Resep")
    try:
        id_hapus = int(input("Masukkan ID resep yang ingin dihapus: "))
        if id_hapus in df["id"].values:
            df = df[df["id"] != id_hapus]
            df.to_csv("resep.csv", index=False)
            print("🗑️ Resep berhasil dihapus.")
        else:
            print("❌ ID tidak ditemukan.")
    except ValueError:
        print("❌ Input tidak valid.")
    input("Tekan Enter untuk kembali...")
    
if __name__ == "__main__":
    main_menu()
