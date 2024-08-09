# Library Imports
import os
import gzip
import shutil

import pandas as pd
import requests

def download_and_unzip_qpe(year, month, WY):
    '''The download_and_unzip_qpe function downloads and unzips QPE 6-hour observed precipitation files 
    for a specified year and month from the CNRFC archive. It generates the appropriate file names 
    and URLs, downloads the files, unzips them directly from the response stream, 
    and saves the unzipped files in a specified directory.
    Parameters:
        year (int): The year for which to download the files (e.g., 2023).
        month (int): The month for which to download the files (e.g., 10 for October).
        WY (str): The water year for which the data is being processed (e.g., '2023').
    Example usage:
        download_and_unzip_qpe(2023, 10, '2023')  # Replace with desired year, month, and WY
    '''
    # Define the date range and time intervals
    start_date = f'{year}-{month:02d}-01'
    end_date = pd.to_datetime(start_date) + pd.offsets.MonthEnd(1)
    time_intervals = ['0000', '0600', '1200', '1800']

    # Extract year and month from the start_date
    year = pd.to_datetime(start_date).year
    month = pd.to_datetime(start_date).strftime('%b')  # Month in abbreviated form, e.g., 'Oct'

    # Base URL with dynamic year and month
    base_url = f"https://www.cnrfc.noaa.gov/archive/{year}/{month}/netcdfqpe/"

    # Generate a list of dates
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')

    # Create lists to store file names and URLs
    file_names = []
    urls = []

    # Loop through each date and time interval to create file names and URLs
    for date in date_range:
        for time in time_intervals:
            file_name = f"qpe.{date.strftime('%Y%m%d')}_{time}.nc.gz"
            url = f"{base_url}{file_name}"
            file_names.append(file_name)
            urls.append(url)

    # Create a DataFrame from the lists of file names and URLs
    df = pd.DataFrame({'File Names': file_names, 'URL': urls})

    # Adjust pandas display options to show the full URL
    pd.set_option('display.max_colwidth', None)

    # Display the DataFrame
    print(df)

    # Define the project root directory using the current working directory
    project_root = os.getcwd()

    # Directory to save the unzipped files, dynamically generated using the year and WY
    unzip_dir = os.path.join(project_root, f'wy{WY}_astar', 'wy_data')

    # Create directory if it doesn't exist
    os.makedirs(unzip_dir, exist_ok=True)

    # Download, unzip, and save the files directly without keeping the zipped files
    for index, row in df.iterrows():
        file_name = row['File Names']
        url = row['URL']
        unzipped_file_name = file_name[:-3]  # Remove .gz extension
        unzipped_file_path = os.path.join(unzip_dir, unzipped_file_name)
        
        # Download the file
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Unzip the file content and save it directly
            with gzip.GzipFile(fileobj=response.raw) as f_in:
                with open(unzipped_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        #     print(f"Downloaded and unzipped: {unzipped_file_name}")
        # else:
        #     print(f"Failed to download: {file_name}")

    print("Download and extraction complete.")


