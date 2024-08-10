# Earth Analytics Final Project 2024
# Landslide Prediction and Monitoring System

## Overview
This repository contains the code for a dual model system designed to predict and locate landslides. By integrating predictive modeling techniques with real-time monitoring systems, this approach offers proactive and reactive capabilities to improve landslide risk management and enhance community safety and resilience.

### Components
1. **Predictive Model (Astar)**: Modified from the Antecedent Water Index model, this component uses extreme values of modeled soil water to anticipate landslide-inducing rainfall, enhancing prediction accuracy.
2. **Land Surface Disturbance Model (OPERA)**: This model utilizes various data sources to detect and pinpoint landslide occurrences in near real time, enabling timely warnings and effective response measures. Provides valuable insights into vegetation disturbance trends at a high spatial resolution using data from Landsat and Sentinel-2 satellites.

### Future Development
The current code demonstrates how each model functions individually. The goal is to develop and automate these models further to provide detailed information on landslide events, including specific dates and precise locations. This advancement will enable more accurate and timely predictions, helping mitigate landslides' risks and impacts on communities.

## How to Use

### Prerequisites
- Python environment set up on your local machine
- Jupyter Notebook installed

### Instructions
1. **Navigate to the directory where you want to clone the repository using the cd command. For example:**
    ```sh
    cd path/to/your/directory
    ```
    
2. **Use the git clone command followed by the URL of the repository:**: 
   ```sh
   git clone https://github.com/misterskye/Predict-and-Locate-California-Landslides.git
   ```
3. **Install the Project2024 Environment**
    The Project2024 environment is included in this repository as an environment.yml file. You can create the environment using conda with the following command:
    ```sh
    conda env create -f environment.yml
    ```
    This command will create a new environment named Project2024 with all the necessary dependencies.

4. **Start by running the 'Astar_Working' Notebook**: 
AWI is a measure used to quantify the moisture content in the soil prior to a significant precipitation event.  

    **Calculating Soil Moisture Anomaly (A*)**

        1. **Start with a Hydrological Model**:
            - We use a special model that simulates soil moisture by considering factors like rain and evaporation.
            - **How It Works**: Think of it like a smart weather forecast that tells us how wet the soil is in different areas over time.

        2. **Establish a Climatological Baseline**:
            - We calculate the average soil moisture for each day over a long period, usually 15 years.
            - **Why This Matters**: This gives us an idea of what's normal for soil moisture throughout the year.

        3. **Calculate the Anomaly**:
            - We find the difference between today's soil moisture and the usual amount for this day.
            - **Example**: If today’s soil moisture is 7 inches, but the average for this day is 5 inches, the anomaly is 2 inches more.

        4. **Normalize the Anomaly**:
            - We adjust this difference by considering how much soil moisture usually varies. This gives us a standard measure called A*.
            - **Why Normalize?**: This helps us compare different places and times fairly. It tells us if today’s moisture is unusually high or
                   low.

        5. **Determine a Threshold for Landslide Risk**:
            - Using historical landslide data, we set a threshold for A* that indicates a high risk of landslides.
            - **How It Helps**: If A* is above this threshold, it means there’s a significant risk of landslides.

        ### Summary
            - **Step-by-Step**:
              1. Use a model to simulate soil moisture.
              2. Calculate the average soil moisture for each day over 15 years.
              3. Compare today’s soil moisture to this average to find the anomaly.
              4. Adjust the anomaly to make it a standard measure (A*).
              5. Set a threshold for A* to identify high landslide risk areas.

5. **LP DAAC’s OPERA Disturbance Alert leverages satellite data to provide timely and accurate land surface disturbance information--OPERA_Working**

The LP DAAC's OPERA Disturbance Alert is a powerful tool for monitoring land surface changes. It combines data from Harmonized Landsat and Sentinel-2, providing observations every 2-4 days at a 30-meter resolution. The system identifies changes in vegetation cover and other land surface conditions by comparing current data to historical baselines. Detected disturbances are highlighted through detailed layers such as disturbance status, confidence levels, and duration. 


### Example Path Setup
In the Jupyter Notebook, you may need to update the directory paths to point to the location where your data files are stored. This ensures that the notebooks can correctly access and process the necessary input files.


## License
This project is licensed under the MIT License.

## References
Perkins, J. P., Oakley, N. S., Collins, B. D., Corbett, S. C., & Burgess, W. P. (2024). Characterizing the Scale of Regional Landslide Triggering from Storm Hydrometeorology. EGUsphere. https://doi.org/10.5194/egusphere-2024-873

Hansen, M.. OPERA Land Surface Disturbance Alert from Harmonized Landsat Sentinel-2 product (Version 1). 2024, distributed by NASA EOSDIS Land Processes Distributed Active Archive Center, https://doi.org/10.5067/SNWG/OPERA_L3_DIST-ALERT-HLS_V1.001. Accessed 2024-07-30.

National Oceanic and Atmospheric Administration. "Historical Archive." California Nevada River Forecast Center, https://www.cnrfc.noaa.gov/arc_search.php. Accessed 29 July 2024.


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13292849.svg)](https://doi.org/10.5281/zenodo.13292849)
---
