# ToMCAT Synchronize Physio Data

This project synchronizes EEG, EKG, GSR, fNIRS physio data and task data together under a unified time series.

## Install dependencies

This project requires Python 3.11.

### Install dependencies with Conda

Ensure that Conda is already installed, then run the following command to install dependencies into a new conda environment

```
conda conda create -n tomcat-synchronize python=3.11
conda activate tomcat-synchronize
pip install -r requirements.txt
```

### Install dependcies with Pip

You can install the packages using Pip3 in a base environment or an environment created for this project, then run the follow command to install dependencies

```
pip3 install -r requirements.txt
```

### Install dependencies manually

If you want to set up environment and install dependencies manually, then you need the following packages

```
pandas
numpy
scipy
scikit-learn
matplotlib
mne
tqdm
```

## Set up project

Ensure that you downloaded the ToMCAT chunked data [here](https://ivilab.cs.arizona.edu/ivilab/data/tomcat/neurips_2023/intermediate_output.tar.gz), ToMCAT task data [here](https://ivilab.cs.arizona.edu/ivilab/data/tomcat/neurips_2023/correlation_exp_tasks.tar.gz), and ToMCAT experiment information [here](https://ivilab.cs.arizona.edu/ivilab/data/tomcat/neurips_2023/correlation_exp_info.tar.gz)

Set the following variables in the `config.py` file:

- `task_data_path` is the full complete path to the ToMCAT task data you downloaded (make sure to decompress the data, e.g., unzip).
- `physio_data_path` is the full complete path to the ToMCAT chunked data you downloaded (make sure to decompress the data, e.g., unzip).
- `experiment_info_path` is the full complete path to the ToMCAT experiment information data you downloaded (make sure to decompress the data, e.g., unzip).
- `output_dir` is the full complete path to the output directory where the synchronized data will be placed.

## Run project

After setting up the `config.py` file, you can launch the program (make sure that you are in the python environment with required dependencies installed):

### Synchronize fNIRS with each task

```
python3 process_nirs.py
```

### Synchronize EEG-EKG-GSR with each task

```
python3 process_nirs.py
```

### Synchronize fNIRS-EEG-EKG-GSR together with each task

```
python3 process_nirs_eeg.py
```

### Synchronize, low-pass filter, and downsample EEG-EKG-GSR to 120 Hz

```
python3 process_nirs_eeg_120 Hz.py
```

## Output

The program will output synchronized data to the path specified in `output_dir` in `config.py`.

