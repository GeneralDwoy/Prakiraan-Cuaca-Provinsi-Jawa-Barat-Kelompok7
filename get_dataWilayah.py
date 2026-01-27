import requests
import pandas as pd

def ambil_dataWilayah_jabar():
    url_api = "https://wilayah.id/api"
    kode_provinsi = "32"  # Jawa Barat
    
    data_kelurahan = []   # Tempat menyimpan semua data
    
    print("Mulai mengambil data wilayah Jawa Barat...")

    try:
        # Ambil daftar Kabupaten / Kota
        response_kab = requests.get(f"{url_api}/regencies/{kode_provinsi}.json")
        daftar_kab = response_kab.json()["data"]
        
        print("Jumlah Kabupaten/Kota:", len(daftar_kab))

        # Loop setiap Kabupaten/Kota
        for kab in daftar_kab:
            print("Memproses:", kab["name"])

            # Ambil daftar Kecamatan
            response_kec = requests.get(f"{url_api}/districts/{kab['code']}.json")
            daftar_kec = response_kec.json()["data"]

            # Loop setiap Kecamatan
            for kec in daftar_kec:

                # Ambil daftar Kelurahan / Desa
                response_kel = requests.get(f"{url_api}/villages/{kec['code']}.json")
                daftar_kel = response_kel.json()["data"]

                # Simpan semua kelurahan ke list
                for kel in daftar_kel:
                    data_kelurahan.append({
                        "Kode": kel["code"],
                        "Kelurahan": kel["name"],
                        "Kecamatan": kec["name"],
                        "Kabupaten/Kota": kab["name"]
                    })

        # Simpan ke file CSV
        tabel = pd.DataFrame(data_kelurahan)
        tabel.to_csv("kode_wilayah_jabar.csv", index=False)
        tabel.to_excel("kode_wilayah_jabar.xlsx", index=False)

        print("\nSelesai!")
        print("Total kelurahan/desa:", len(tabel))
        print("File tersimpan: kode_wilayah_jabar.csv dan kode_wilayah_jabar.xlsx")

    except Exception as error:
        print("Terjadi kesalahan:", error)


# Program utama
if __name__ == "__main__":
    ambil_dataWilayah_jabar()