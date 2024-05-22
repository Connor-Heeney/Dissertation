import os
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def process_single_gedi_file(file_path):
    beams = ['BEAM0000', 'BEAM0001', 'BEAM0010', 'BEAM0011', 
             'BEAM0101', 'BEAM0110', 'BEAM1000', 'BEAM1011']

    all_lat, all_lon, all_pai, all_time = [], [], [], []

    with h5.File(file_path, 'r') as f:
        for beam in beams:
            if beam in f:
                lat = f[f'{beam}/geolocation/latitude_bin0'][:]
                lon = f[f'{beam}/geolocation/longitude_bin0'][:]
                pai = f[f'{beam}/pai_z'][:]
                time = f[f'{beam}/geolocation/delta_time'][:]

                if lat.ndim == 1 and pai.ndim == 2 and lat.size == pai.shape[0]:
                    lat = np.repeat(lat, pai.shape[1])
                    lon = np.repeat(lon, pai.shape[1])
                    time = np.repeat(time, pai.shape[1])
                    pai = pai.flatten()

                    mask = (~np.isnan(lat)) & (~np.isnan(lon)) & (~np.isnan(pai)) & (pai > 0)
                    lat, lon, pai, time = lat[mask], lon[mask], pai[mask], time[mask]

                    all_lat.extend(lat)
                    all_lon.extend(lon)
                    all_pai.extend(pai)
                    all_time.extend(time)

    return np.array(all_lat), np.array(all_lon), np.array(all_pai), np.array(all_time)

def convert_time(delta_times, epoch_start=datetime(2018, 1, 1)):
    return np.array([epoch_start + timedelta(seconds=delta) for delta in delta_times])

def aggregate_by_month(all_lat, all_pai, all_time):
    monthly_data = {}
    for lat, pai, time in zip(all_lat, all_pai, all_time):
        month = time.month
        if month not in monthly_data:
            monthly_data[month] = {'lat': [], 'pai': []}
        monthly_data[month]['lat'].append(lat)
        monthly_data[month]['pai'].append(pai)
    return monthly_data

def plot_pai_vs_latitude(monthly_data):
    for month, data in monthly_data.items():
        lat = np.array(data['lat'])
        pai = np.array(data['pai'])

        bins = np.linspace(np.min(lat), np.max(lat), 100)
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        mean_pai = np.zeros(len(bin_centers))

        for i in range(len(bin_centers)):
            mask = (lat >= bins[i]) & (lat < bins[i + 1])
            mean_pai[i] = np.nanmean(pai[mask])

        plt.plot(bin_centers, mean_pai, linewidth=0.5, label=f'Month {month}')

# Directory for GEDI files
folder_path = os.path.join(os.getcwd(), 'src/data/gedi')
gedi_files = [f for f in os.listdir(folder_path) if f.endswith('.h5')]

all_latitudes = []
all_longitudes = []
all_pai_values = []
all_times = []

for file_name in gedi_files:
    file_path = os.path.join(folder_path, file_name)
    all_lat, all_lon, all_pai, all_time = process_single_gedi_file(file_path)
    all_latitudes.extend(all_lat)
    all_longitudes.extend(all_lon)
    all_pai_values.extend(all_pai)
    all_times.extend(convert_time(all_time))

monthly_data = aggregate_by_month(np.array(all_latitudes), np.array(all_pai_values), np.array(all_times))
# Plot flightlines
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sc = plt.scatter(all_longitudes, all_latitudes, c=all_pai_values, cmap='viridis', s=1, vmin=0, vmax=1.75)
cbar = plt.colorbar(sc)
cbar.set_label('PAI')
plt.title('GEDI PAI Flight Paths')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Plot PAI against latitude over time
plt.subplot(1, 2, 2)
plot_pai_vs_latitude(monthly_data)

plt.ylim(0, 1.75)
plt.title('PAI vs Latitude Over Time')
plt.xlabel('Latitude')
plt.ylabel('Mean PAI')
plt.legend()
plt.tight_layout()
plt.show()