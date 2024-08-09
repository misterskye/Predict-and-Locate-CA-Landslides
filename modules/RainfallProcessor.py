import os
import glob
import numpy as np
import pandas as pd
import xarray as xr
import rasterio
from metpy.units import units
import rioxarray
import time

class RainfallProcessor:
    def __init__(self, latlon_csv_path, crs_proj4, output_dir):
        self.latlon_csv_path = latlon_csv_path
        self.crs = rasterio.crs.CRS.from_proj4(crs_proj4)
        self.output_dir = output_dir

    def process_file_CNRFC(self, filepath, year):
        ds = xr.open_dataset(filepath, decode_times=False, decode_coords="all")
        ds = ds.squeeze()

        df = pd.read_csv(self.latlon_csv_path, sep=',')
        forlatvec = df.loc[df['Grid x'] == 0]
        latvec = forlatvec['Grid y'].values
        forlonvec = df.loc[df['Grid y'] == 0]
        lonvec = forlonvec['Grid x'].values

        ds = ds.rename_dims(dimx="longitude", dimy="latitude")
        ds = ds.assign_coords(longitude=("longitude", lonvec), latitude=("latitude", latvec))

        rain = ds['qpe_grid']
        rain = rain.metpy.convert_units('m')
        rain.rio.write_crs(self.crs, inplace=True)

        # Set nodata value explicitly
        rain.rio.set_nodata(3.4028234663852886e+38, inplace=True)

        rain_lonlat = rain.rio.reproject("EPSG:4326")

        hour = filepath[-7:-5]
        day = filepath[-10:-8]
        month = filepath[-12:-10]
        year = filepath[-16:-12]

        date = f"{year}-{month}-{day}T{hour}:00"
        
        # Convert to nanosecond precision
        rtime = np.datetime64(date, 'ns')

        rain_lonlat = rain_lonlat.assign_coords({"time": rtime})

        return rain_lonlat

    def process_dir_CNRFC_AWI_WY(self, filepath, min_lon, max_lon, min_lat, max_lat, year, WY):
        filenames = sorted(glob.glob(filepath))

        rain = self.process_file_CNRFC(filenames[1], year)
        rain = rain.where(rain < 1.0e38)
        rain = rain.rio.write_crs(4326)
        rain = rain.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat)

        rainPrism = xr.DataArray()
        AWI_prism = xr.DataArray()
        AWI_old = xr.zeros_like(rain)
        AWI_old[:] = -0.18
        dt_hrs = 6.0

        for file in filenames:
            print(f"Processing {file}", end='\r', flush=True)
            rain = self.process_file_CNRFC(file, year)
            rain = rain.where(rain < 1.0e5)
            rain = rain.rio.write_crs(4326)
            try:
                rain = rain.rio.clip_box(minx=min_lon, miny=min_lat, maxx=max_lon, maxy=max_lat)
            except Exception as e:
                print(f"Error clipping file {file}: {e}")
                continue
            
            if rain.shape[0] <= 1 or rain.shape[1] <= 1:
                print(f"Skipping file {file} due to insufficient data after clipping.")
                continue
            
            rainPrism = xr.concat([rainPrism, rain], 'z')

            AWI_new = self.AWI_run_step(AWI_old, rain, dt_hrs)
            AWI_new['time'] = rain['time']
            AWI_prism = xr.concat([AWI_prism, AWI_new], 'z')

            AWI_old = AWI_new
            time.sleep(0.01)

        rainPrism = rainPrism.rename({'x': 'longitude', 'y': 'latitude'})
        AWI_prism = AWI_prism.rename({'x': 'longitude', 'y': 'latitude'})

        outfile1 = os.path.join(self.output_dir, f"rain_prism_{WY}.nc")
        outfile2 = os.path.join(self.output_dir, f"AWI_prism_{WY}.nc")

        # Check if the files exist and remove them if they do
        if os.path.exists(outfile1):
            os.remove(outfile1)
        if os.path.exists(outfile2):
            os.remove(outfile2)

        rainPrism.to_netcdf(outfile1)
        AWI_prism.to_netcdf(outfile2)

        print("\nFiles exported")
        
        # Count the number of time steps in the AWI_prism DataArray
        num_time_steps = AWI_prism.sizes['z']
    
        print(f"The file {outfile2} contains {num_time_steps} time steps.")

        return rainPrism, AWI_prism

    def AWI_run_step(self, AWI_t_minus_dt, rain_m, dt_hrs):
        kd = 0.01  # Drainage proportionality constant from Godt et al., 2006; [1/hrs]
        Ii_m_hr = rain_m / dt_hrs

        AWI_t = xr.where(AWI_t_minus_dt > 0., AWI_t_minus_dt*np.exp(-kd*dt_hrs) 
                        + ((Ii_m_hr/kd)*(1.-np.exp(-kd*dt_hrs))), 
                        AWI_t_minus_dt + rain_m)
        

        return AWI_t

