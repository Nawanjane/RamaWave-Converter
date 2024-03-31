import os
import pandas as pd

# Function to convert wavelength to Raman shift
def wavelength_to_raman_shift(wavelength_nm):
    wavelength_m = wavelength_nm * 1e-9
    return (1 / laser_wavelength_nm - 1 / wavelength_nm) * 1e7

# Function to process .asc files
def process_asc_file(file_path, laser_wavelength_nm):
    data = pd.read_csv(file_path, sep='\t', header=None, nrows=1600, dtype={0: 'float64', 1: 'int64'})
    data.columns = ['Wavelength_nm', 'Count']
    data.dropna(subset=['Wavelength_nm'], inplace=True)  # Remove rows with missing wavelengths
    data['Raman_Shift_cm^-1'] = wavelength_to_raman_shift(data['Wavelength_nm'])
    data = data[['Raman_Shift_cm^-1', 'Count']]
    data.to_csv(file_path, sep='\t', header=False, index=False, float_format='%.8f')

# Function to copy lines to temp.txt
def copy_rows_to_temp(filename, start_row, temp_filename):
    with open(filename, 'r') as input_file, open(temp_filename, 'w') as output_file:
        # Ensure there are enough rows to reach start_row
        if start_row <= len(input_file.readlines()):  # Check line count
            for _ in range(start_row - 1):
                next(input_file)
            for line in input_file:
                output_file.write(line)
        else:
            print(f"Warning: File '{filename}' has fewer than {start_row} rows. Skipping copying.")


# Function to append lines from temp.txt to an .asc file
def append_temp_to_asc(file_path, temp_filename):
    with open(file_path, 'a') as file, open(temp_filename, 'r') as temp_file:
        file.write(temp_file.read())

# Main function to traverse directory and process files
def process_directory(directory, laser_wavelength_nm, start_row, temp_folder):
    temp_filename = os.path.join(temp_folder, "temp.txt")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.asc'):
                full_path = os.path.join(root, file)
                print(f"Processing {full_path}")
                process_asc_file(full_path, laser_wavelength_nm)
                copy_rows_to_temp(full_path, start_row, temp_filename)
                append_temp_to_asc(full_path, temp_filename)
                # Clear temp.txt
                open(temp_filename, 'w').close()

# Set parameters
laser_wavelength_nm = 534.0  # Replace with your actual laser wavelength
directory_to_process = 'Data'  # Replace with your directory path
start_row_to_copy = 1603  # Replace with the row number from which to start copying
temp_folder = 'temp'  # Replace with your temp folder path

# Run the process
process_directory(directory_to_process, laser_wavelength_nm, start_row_to_copy, temp_folder)
