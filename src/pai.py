import os
import h5py
import numpy as np
import matplotlib.pyplot as plt

def process_single_gedi_file(file_path):
    beams = ['BEAM0000', 'BEAM0001', 'BEAM0010', 'BEAM0011', 
             'BEAM0101', 'BEAM0110', 'BEAM1000', 'BEAM1011']

    all_lat, all_lon, all_pai = [], [], []

    with h5py.File(file_path, 'r') as f:
        for beam in beams:
            if beam in f:
                lat = f[f'{beam}/geolocation/latitude_bin0'][:]
                lon = f[f'{beam}/geolocation/longitude_bin0'][:]
                pai = f[f'{beam}/pai_z'][:]

                # Ensure latitude, longitude, and PAI dimensions match
                if lat.ndim == 1 and pai.ndim == 2:
                    lat = np.repeat(lat, pai.shape[1])
                    lon = np.repeat(lon, pai.shape[1])
                    pai = pai.flatten()

                # Filter out invalid (NaN) entries
                mask = (~np.isnan(lat)) & (~np.isnan(lon)) & (~np.isnan(pai)) & (pai > 0)
                lat, lon, pai = lat[mask], lon[mask], pai[mask]

                all_lat.extend(lat)
                all_lon.extend(lon)
                all_pai.extend(pai)

    return np.array(all_lat), np.array(all_lon), np.array(all_pai)

def plot_pai_vs_latitude(all_lat, all_pai):
    # Bin latitudes and average PAI values for each bin
    bins = np.linspace(np.min(all_lat), np.max(all_lat), 100)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    mean_pai = np.zeros(len(bin_centers))

    for i in range(len(bin_centers)):
        mask = (all_lat >= bins[i]) & (all_lat < bins[i + 1])
        mean_pai[i] = np.nanmean(all_pai[mask])

    return bin_centers, mean_pai

# Directory containing GEDI files
file_name = 'processed_GEDI02_B_2019117234644_O02114_01_T01616_02_003_01_V002.h5'
folder_path = os.path.join(os.getcwd(), 'src/data/gedi')
file_path = os.path.join(folder_path, file_name)

all_lat, all_lon, all_pai = process_single_gedi_file(file_path)

# Range for the colorbar and y-axis
pai_min, pai_max = 0, 1.8

# Plotting the scatter plot
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sc = plt.scatter(all_lon, all_lat, c=all_pai, cmap='viridis', s=1, vmin=pai_min, vmax=pai_max)
cbar = plt.colorbar(sc)
cbar.set_label('PAI')
plt.title('GEDI PAI')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Plotting the line graph
plt.subplot(1, 2, 2)
bin_centers, mean_pai = plot_pai_vs_latitude(all_lat, all_pai)

plt.plot(bin_centers, mean_pai, color='blue', linewidth=0.5)
plt.ylim(pai_min, pai_max)  # Use the same range as the scatter plot
plt.title('PAI vs Latitude')
plt.xlabel('Latitude')
plt.ylabel('Mean PAI')

plt.tight_layout()
plt.show()