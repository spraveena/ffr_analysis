from scipy.fft import fft, fftfreq
from scipy.signal import hilbert, butter, filtfilt
import numpy as np
from scipy.stats import zscore

# --- Dynamic FFR File Loader ---
import glob
import os
import re
from scipy.io import loadmat
import pandas as pd


fft_freqs = [195, 210, 975, 1170,415, 625, 1040, 1250, 1460, 1670, 390.0, 475.0, 585.0, 780.0] # please adjust according to need
FFR_FS = 16384  # EEG sampling rate
BASELINE_DURATION=.02 #in seconds
BASELINE_END_SAMPLE = int(BASELINE_DURATION * FFR_FS)  # Baseline duration in samples
CHANNEL_NUM=7
RESULTS_FILE_DIR = "Results/fft_results.csv"

os.makedirs("Results", exist_ok=True)

def compute_fft_amplitude(signal, fs, target_freqs=fft_freqs, window=None):
    if window is not None:
        signal = signal * window
    N = len(signal)
    yf = np.abs(fft(signal)) / N
    # yf = (yf  - np.min(yf )) / (np.max(yf ) - np.min(yf ))
    xf = fftfreq(N, 1/fs)
    freq_amplitudes = {}
    for f in target_freqs:
        idx = np.argmin(np.abs(xf - f))
        freq_amplitudes[f] = yf[idx]
    return freq_amplitudes








subfolders = [
    "data/",
   
]


# Automatically collect all files ending with _MAT from the subfolders
ffr_files = []
results = []


for folder in subfolders:
    ffr_files.extend(glob.glob(os.path.join(folder, "*_MAT.mat")))

for ffr_file in ffr_files:
    # Load EEG data from MATLAB file
    ffr_response_struct = loadmat(ffr_file)
    
    # Assume 'data' key contains the response matrix
    ffr_response = ffr_response_struct['data'][CHANNEL_NUM-1, BASELINE_END_SAMPLE:]

    match = re.search(r'P(\d{2})', ffr_file)
    participant_id = match.group(0) if match else "Unknown"
    results_row = {}



    # Compute FFT
    fft_result = compute_fft_amplitude(ffr_response, FFR_FS, target_freqs=fft_freqs)

    # Build result row
    results_row = {"Participant": participant_id}
    
    for f in fft_freqs:
        results_row[f"FFT_{f}Hz"] = fft_result[f]
            
        
    
    results.append(results_row)
    

    # --- Save to CSV ---


results_df = pd.DataFrame(results)


results_df = results_df.groupby("Participant").first().reset_index()


results_df.to_csv(RESULTS_FILE_DIR, index=False)


print("Saved FFT amplitude results wide and long")