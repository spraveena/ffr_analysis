
## About

Scripts in this repository were constructed with the aim to facilitate analysis of Frequency Following Responses (FFR)
to auditory stimulus.
As of now, the script currently reads in a MATLAB data struct and assumes signal data is stored under the key 'data' of the MATLAB struct



## Scripts

---

### Expected directory structure

```
project/
├── data/               # .mat EEG files (e.g. P01_MAT.mat)
├── wav/                # stimulus audio files
├── Results/            # output CSVs (auto-created by scripts)
├── fft_harmonics.py
├── resp2stim_corr.py
├── requirements.txt
└── README.md
```

---

### `fft_harmonics.py`
Computes FFT amplitude at specified harmonic frequencies from FFR (Frequency Following Response) 
EEG data exported from Letswave. For each participant file, it extracts amplitude at 
user-defined target frequencies and saves results to a wide-format CSV.

**Input:** `.mat` files in `data/` folder, named with participant ID in format `P01`  
**Output:** `Results/fft_results.csv`  
**Configure:** `fft_freqs`, `CHANNEL_NUM`, `BASELINE_DURATION` at top of script

---

### `resp2stim_corr.py`
Computes stimulus-to-response envelope correlation between a stimulus audio file and FFR EEG 
responses. Returns maximum cross-correlation value and corresponding lag (ms) per participant.

**Input:** `.wav` stimulus file + `.mat` EEG files in `data/`  
**Output:** `Results/src_results.csv`  
**Configure:** `audio_file` path, `CHANNEL_NUM`, `ISI`, `END_SAMPLE` at top of script

---
## Setup

### Windows

1. Go to python.org/downloads and download the latest installer (e.g., Python 3.x.x).
2. Run the installer. Important: Check the box that says "Add Python to PATH" before clicking Install Now.
3. Verify the installation by opening Command Prompt and running:

`python --version`

### macOS

Python 3 can be installed via the official installer or Homebrew:
Option A — Official installer: Download from python.org and run the .pkg file.
Option B — Homebrew:

`brew install python`

Verify with 

`python3 --version`

### Installing packages required to run scripts

Go into directory of scripts, check that there's a file called `requirements.txt`

Run the following command in command prompt:

`pip install -r requirements.txt`




### Run scripts

```bash
python fft_harmonics.py
python resp2stim_corr.py
```

---

## Notes

- Both scripts expect EEG data stored under the key `data` in the `.mat` file, as exported by Letswave
- Participant IDs are parsed from filenames using the pattern `P` followed by two digits (e.g. `P01`, `P12`)
- The `Results/` directory is created automatically if it does not exist

---

If you have found these scripts to be beneficial for your analysis please consider citing this repository (:

