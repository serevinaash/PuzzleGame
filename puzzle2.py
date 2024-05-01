import time

# Konstanta
KAPASITAS = 100

class TekaTeki:
    def __init__(self):
        self.isi = [[''] * KAPASITAS for _ in range(KAPASITAS)]
        self.baris = 0
        self.kolom = 0

class DaftarKata:
    def __init__(self):
        self.isi = []
        self.jumlah = 0

def file2data(nama_berkas, teka_teki, daftar_kata):
    jalur_berkas = f"./test/{nama_berkas}"
    
    with open(jalur_berkas, 'r') as berkas:
        baris = berkas.readlines()
    
    # Inisialisasi indeks
    i = 0
    
    # Baca isi teka-teki
    while i < len(baris) and baris[i].strip() != "":
        baris_teka_teki = baris[i].strip().replace(" ", "")
        teka_teki.isi[i][:len(baris_teka_teki)] = baris_teka_teki
        i += 1
    
    teka_teki.baris = i
    teka_teki.kolom = len(baris_teka_teki) if i > 0 else 0

    # Baca isi daftar kata
    while i < len(baris):
        baris_kata = baris[i].strip()
        if baris_kata:
            daftar_kata.isi.append(baris_kata)
            daftar_kata.jumlah += 1
        i += 1

def cetak_grid(teka_teki, grid_ditemukan):
    for baris in range(teka_teki.baris):
        baris_teks = ''
        for kolom in range(teka_teki.kolom):
            if grid_ditemukan[baris][kolom]:
                baris_teks += teka_teki.isi[baris][kolom] + ' '
            else:
                baris_teks += '- '
        print(baris_teks)

def cari_kata(teka_teki, kata):
    panjang = len(kata)
    grid_ditemukan = [[False] * KAPASITAS for _ in range(KAPASITAS)]
    jumlah_perbandingan = 0  # Menginisialisasi jumlah perbandingan

    for i in range(teka_teki.baris):
        for j in range(teka_teki.kolom):
            arah = {
                "Timur": lambda k: (i, j + k),
                "Tenggara": lambda k: (i + k, j + k),
                "Selatan": lambda k: (i + k, j),
                "Barat Daya": lambda k: (i + k, j - k),
                "Barat": lambda k: (i, j - k),
                "Barat Laut": lambda k: (i - k, j - k),
                "Utara": lambda k: (i - k, j),
                "Timur Laut": lambda k: (i - k, j + k)
            }
            
            for arah, posisi in arah.items():
                ditemukan = True
                for k in range(panjang):
                    baris, kolom = posisi(k)
                    
                    # Tambah perbandingan
                    jumlah_perbandingan += 1
                    
                    if not (0 <= baris < teka_teki.baris and 0 <= kolom < teka_teki.kolom):
                        ditemukan = False
                        break
                    
                    if teka_teki.isi[baris][kolom] != kata[k]:
                        ditemukan = False
                        break
                
                if ditemukan:
                    for k in range(panjang):
                        baris, kolom = posisi(k)
                        grid_ditemukan[baris][kolom] = True
                    print(f"Kata '{kata}' ditemukan dalam arah '{arah}' mulai dari ({i}, {j}):")
                    cetak_grid(teka_teki, grid_ditemukan)
                    return jumlah_perbandingan  # Kembalikan jumlah perbandingan
    
    print(f"Kata '{kata}' tidak ditemukan!")
    return jumlah_perbandingan

def main():
    teka_teki = TekaTeki()
    daftar_kata = DaftarKata()

    # Baca berkas
    nama_berkas = input("\nMasukkan nama berkas uji Anda: ")
    print("\n")
    file2data(nama_berkas, teka_teki, daftar_kata)

    # Metode Brute Force
    total_jumlah_perbandingan = 0  # Total perbandingan
    awal = time.time()

    for i in range(daftar_kata.jumlah):
        # Perbarui total_jumlah_perbandingan dengan jumlah perbandingan yang dikembalikan oleh cari_kata
        total_jumlah_perbandingan += cari_kata(teka_teki, daftar_kata.isi[i])
        print("\n")
    
    akhir = time.time()
    durasi = (akhir - awal) * 1e6  # Konversi ke mikrodetik
    print(f"Waktu yang dihabiskan: {durasi:.0f} mikrodetik")
    print(f"Total perbandingan: {total_jumlah_perbandingan} huruf\n\n")

if __name__ == "__main__":
    main()
