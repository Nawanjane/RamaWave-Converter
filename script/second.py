import pandas as pd

# Specify accurate laser wavelength
laser_wavelength_nm = 534.0  # Replace with your actual laser wavelength

# Function for conversion, optimized for clarity and efficiency
def wavelength_to_raman_shift(wavelength_nm):
    wavelength_m = wavelength_nm * 1e-9
    return (1 / laser_wavelength_nm - 1 / wavelength_nm) * 1e7

# Read the data efficiently
file_path = '/Users/leopard/Desktop/position_01.asc'  # Adjust the file path
data = pd.read_csv(file_path, sep='\t', header=None, nrows=1600, dtype={0: 'float64', 1: 'int64'})
data.columns = ['Wavelength_nm', 'Count']

# Ensure data quality
data.dropna(subset=['Wavelength_nm'], inplace=True)  # Remove rows with missing wavelengths

# Convert to Raman shift using vectorized operation for speed
data['Raman_Shift_cm^-1'] = wavelength_to_raman_shift(data['Wavelength_nm'])

# Select desired columns directly
data = data[['Raman_Shift_cm^-1', 'Count']]

# Overwrite the file with precise output
data.to_csv(file_path, sep='\t', header=False, index=False, float_format='%.8f')

print(f"Data converted and saved to {file_path}")

