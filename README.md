# Final Project 2024
# Landslide Prediction and Monitoring System

## Overview
This repository contains the code for a dual model system designed to predict and locate landslides. By integrating predictive modeling techniques with real-time monitoring systems, this approach offers proactive and reactive capabilities to improve landslide risk management and enhance community safety and resilience.

### Components
1. **Predictive Model (A\*)**: Modified from the Antecedent Water Index model, this component uses extreme values of modeled soil water to anticipate landslide-inducing rainfall, enhancing prediction accuracy.
2. **Real-Time Monitoring Model (OPERA)**: This model utilizes various data sources to detect and pinpoint landslide occurrences in near real time, enabling timely warnings and effective response measures.
3. **OPERA Land Surface Disturbance Alert**: Provides valuable insights into vegetation disturbance trends at a high spatial resolution using data from Landsat and Sentinel-2 satellites.

### Future Development
The current code demonstrates how each model functions individually. The goal is to develop and automate these models further to provide detailed information on landslide events, including specific dates and precise locations. This advancement will enable more accurate and timely predictions, helping mitigate landslides' risks and impacts on communities.

## How to Use

### Prerequisites
- Python environment set up on your local machine
- Jupyter Notebook installed

### Instructions
1. **Clone the Repository**: 
   ```sh
   git clone https://github.com/your-username/landslide-prediction.git
   ```

2. **Download the `astar_example_files` Folder**: 
   Ensure you have the `astar_example_files` folder downloaded to your local machine.

3. **Set Up the Directory**: 
   Place the `astar_example_files` folder in the directory where you cloned this repository.

4. **Run the Notebook**: 
   Open the Jupyter Notebook file and direct the code to your directory containing the `astar_example_files` folder. You can do this by modifying the path variables in the notebook to point to your local directory.

### Example Path Setup
In the Jupyter Notebook, update the directory paths as follows:
```python
# Example of setting the path to your local directory
data_directory = "/path/to/your/astar_example_files"
```

## License
This project is licensed under the MIT License.

---
