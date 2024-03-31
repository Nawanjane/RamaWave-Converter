import os
import pandas as pd

# Function to convert wavelength to Raman shift
def wavelength_to_raman_shift(laser_wavelength_nm, wavelength_nm):
    wavelength_m = wavelength_nm * 1e-9
    return (1 / (laser_wavelength_nm * 1e-9) - 1 / wavelength_m) * 1e7

# Function to process .asc files
def process_asc_file(file_path, laser_wavelength_nm):
    # Read the first 1600 rows of the .asc file for processing
    data = pd.read_csv(file_path, sep='\t', header=None, nrows=1600, dtype={0: 'float64', 1: 'int64'})
    data.columns = ['Wavelength_nm', 'Count']
    data.dropna(subset=['Wavelength_nm'], inplace=True)
    data['Raman_Shift_cm^-1'] = data['Wavelength_nm'].apply(lambda x: wavelength_to_raman_shift(laser_wavelength_nm, x))
    data = data[['Raman_Shift_cm^-1', 'Count']]
    
    # Save the processed data to a temporary file
    temp_processed_file = file_path + '.tmp'
    data.to_csv(temp_processed_file, sep='\t', header=False, index=False, float_format='%.8f')
    
    # Append the unprocessed lines to the temporary file
    with open(file_path, 'r') as original_file, open(temp_processed_file, 'a') as processed_file:
        # Skip the first 1600 lines
        for _ in range(1600):
            next(original_file)
        # Copy the rest of the lines
        for line in original_file:
            processed_file.write(line)
    
    # Replace the original file with the temporary file
    os.replace(temp_processed_file, file_path)

# Main function to traverse directory and process files
def process_directory(directory, laser_wavelength_nm):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.asc'):
                full_path = os.path.join(root, file)
                print(f"Processing {full_path}")
                process_asc_file(full_path, laser_wavelength_nm)

# Set parameters
laser_wavelength_nm = 534.0  # Replace with your actual laser wavelength
directory_to_process = 'Data'  # Replace with your directory path

# Run the process
process_directory(directory_to_process, laser_wavelength_nm)
