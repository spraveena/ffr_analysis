
import scipy.io.wavfile as wav
from scipy.signal import resample
import re

import numpy as np
import pandas as pd
import scipy.signal as signal
from scipy.io import wavfile
from scipy.io import loadmat
import os


# --- Analysis Functions ---

from scipy.fft import fft, fftfreq
from scipy.signal import hilbert, butter, filtfilt

# --- Dynamic FFR File Loader ---
import glob

# Constants
FFR_FS = 16384  # EEG sampling rate
ISI=.02 # in seconds, adjust according to stimulus
CHANNEL_NUM=7
RESULTS_FILE_DIR = "Results/src_results.csv"

BASELINE_DURATION=ISI/2  
BASELINE_END_SAMPLE = int(BASELINE_DURATION * FFR_FS)  # Baseline duration in samples
END_SAMPLE = int(0.014 * FFR_FS) #time frame within which you're computing lag for maximum correlation between stimulus and response in seconds

os.makedirs("Results", exist_ok=True)


audio_fs, audio_data = wavfile.read(audio_file)

if len(audio_data.shape) > 1:  # Convert to mono if stereo
    audio_data = audio_data[:, 0]


# Resample audio to FFR sampling rate
resampled_audio = signal.resample(audio_data, int(len(audio_data) * FFR_FS / audio_fs))


# Constants for lag selection
END_SAMPLE = 400  # Adjust if needed



# Define data subfolders
subfolders = [
    #insert directory to data folder here (not each individual file, this is meant to collect all files from the folder listed), for instance:
    "data/",
    
]

# Automatically collect all files ending with _MAT from the subfolders (_MAT because this is the result of exporting files from Letswave after initial preprocessing)
ffr_files = []
for folder in subfolders:
    ffr_files.extend(glob.glob(os.path.join(folder, "*_MAT.mat")))

print(f"Found {len(ffr_files)} FFR files.")

results = []



# Apply Butterworth bandpass filter (4th-order, 70-4000 Hz, adjust parameters accordingly for your needs)
b, a = signal.butter(4, [70, 4000], btype='bandpass', fs=FFR_FS)
filtered_audio = signal.lfilter(b, a, resampled_audio)
trial_len = len(filtered_audio)




# Process each EEG response file
for ffr_file in ffr_files:
    # Load EEG data from MATLAB file
    print(ffr_file)
    ffr_response_struct = loadmat(ffr_file)
    print(len(ffr_response_struct['data']))

    
    # Assume 'data' key contains the response matrix
    # BASELINE_END_SAMPLE:BASELINE_END_SAMPLE + len(filtered_audio) retrieves the portion go the signal after the baseline period till the end of the length of the trial
    ffr_response = ffr_response_struct['data'][CHANNEL_NUM-1, BASELINE_END_SAMPLE:BASELINE_END_SAMPLE + trial_len]

    match = re.search(r'P(\d{2})', ffr_file) #depending on how ParticipantID is included in your filename. this is if you store it in the format of P01
    participant_id = match.group(0) if match else "Unknown"
    print(participant_id)



    # Normalize signals
    filtered_audio = (filtered_audio - np.mean(filtered_audio)) / np.std(filtered_audio)
    ffr_response = (ffr_response - np.mean(ffr_response)) / np.std(ffr_response)

    '''
    correlation gives you negative and positive values, which will span the length of 2x the stimulus
    when computing correlation and lag values, we are only concerned with the positive half, so the signal of interest
    starts from after one length of the stimulus(or after the negative half)

    When computing max correlation and lag, we're computing the point at which the stimulus and response are the most synchronized
    and we anticipate this to happen within the first 14-16ms of the stimulus, therefore the END_SAMPLE variable assigned earlier
    '''

    start = len(filtered_audio) - 1 + 100
    end = len(filtered_audio) - 1 + END_SAMPLE

    # Compute cross-correlation
    corr = np.correlate(ffr_response.flatten(), filtered_audio.flatten(), mode="full")
    corr = corr / (len(filtered_audio) * np.std(filtered_audio) * np.std(ffr_response))

    # Find max correlation and corresponding lag
    lags = np.arange(-len(filtered_audio) + 1, len(filtered_audio))
    positive_lags = lags[start:end]
    positive_corr = corr[start:end]

    max_corr_idx = np.argmax(positive_corr[0:END_SAMPLE])
    max_corr = round(positive_corr[max_corr_idx],2)
    max_lag = round((positive_lags[max_corr_idx] / FFR_FS)*1000,2)  # Convert samples to ms


       

    # Store results
    results.append({
        "Participant":participant_id,
        "MaxCorr": max_corr,
        "MaxLag": max_lag,
        
    })

# Convert results to DataFrame
results_df = pd.DataFrame(results)
print(results_df)


# # Save
results_df.to_csv(RESULTS_FILE_DIR, index=False)
print("Concatenated full results saved")




      




