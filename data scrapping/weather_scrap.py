import requests
import csv
import time

API_KEY = "Your API Key"

daftar_ibukota = [
    "Banda Aceh", "Medan", "Padang", "Pekanbaru", "Tanjung Pinang", "Jambi", 
    "Bengkulu", "Palembang", "Pangkal Pinang", "Bandar Lampung", "Serang", 
    "Jakarta", "Bandung", "Semarang", "Yogyakarta", "Surabaya", "Denpasar", 
    "Mataram", "Kupang", "Pontianak", "Palangkaraya", "Banjarmasin", 
    "Samarinda", "Tanjung Selor", "Manado", "Palu", "Makassar", "Kendari", 
    "Gorontalo", "Mamuju", "Ambon", "Sofifi", "Manokwari", "Nabire", 
    "Jayapura", "Merauke", "Wamena", "Sorong"
]

nama_file_csv = 'cuaca_provinsi_indonesia.csv'

header_csv = [
    'kota', 'provinsi', 'latitude', 'longitude', 'waktu_lokal', 'suhu_c', 
    'kondisi_cuaca', 'kode_kondisi', 'icon_url', 'kecepatan_angin_kph', 
    'arah_angin', 'kelembapan', 'uv_index'
]

print(f"Memulai proses pengambilan data untuk {len(daftar_ibukota)} kota...")

with open(nama_file_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header_csv)

    for kota in daftar_ibukota:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={kota}&aqi=no"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            location_data = data.get('location', {})
            current_data = data.get('current', {})
            condition_data = current_data.get('condition', {})

            baris_data = [
                location_data.get('name', kota),
                location_data.get('region', 'N/A'),
                location_data.get('lat', 'N/A'),
                location_data.get('lon', 'N/A'),
                location_data.get('localtime', 'N/A'),
                current_data.get('temp_c', 'N/A'),
                condition_data.get('text', 'N/A'),
                condition_data.get('code', 'N/A'),
                "https:" + condition_data.get('icon', ''),
                current_data.get('wind_kph', 'N/A'),
                current_data.get('wind_dir', 'N/A'),
                current_data.get('humidity', 'N/A'),
                current_data.get('uv', 'N/A')
            ]
            
            writer.writerow(baris_data)
            
            print(f"✔️ Berhasil mengambil data untuk: {kota}")

        except requests.exceptions.HTTPError as err:
            print(f"❌ Gagal untuk {kota}: {err.response.status_code} - {err.response.json().get('error', {}).get('message', 'Error tidak diketahui')}")
        except Exception as err:
            print(f"❌ Terjadi kesalahan teknis untuk {kota}: {err}")
            
        time.sleep(1)

print(f"\n🎉 Proses selesai! Data telah disimpan di file: {nama_file_csv}")
