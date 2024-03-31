import os
import pandas as pd
from flask import Flask, request, send_from_directory, render_template, redirect, url_for
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = 'Data'
ALLOWED_EXTENSIONS = {'txt', 'asc', '*'}  # Allow all text extensions

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file extensions (adjusted for all text extensions)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to convert wavelength to Raman shift
def wavelength_to_raman_shift(wavelength_nm):
    wavelength_m = wavelength_nm * 1e-9
    return (1 / laser_wavelength_nm - 1 / wavelength_nm) * 1e7

# Function to process .asc files
import chardet

def process_asc_file(file_path, laser_wavelength_nm, nrows):
    # Open the file in binary mode and detect encoding
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    try:
        # Attempt to read the file with detected encoding
        data = pd.read_csv(file_path, sep='\t', header=None, nrows=nrows, dtype={0: 'float64', 1: 'int64'}, encoding=encoding)
    except UnicodeDecodeError:
        # If decoding fails, try with 'latin-1' encoding (common for older text files)
        data = pd.read_csv(file_path, sep='\t', header=None, nrows=nrows, dtype={0: 'float64', 1: 'int64'}, encoding='latin-1', errors='replace')
        print(f"Warning: Potential encoding issue with '{file_path}'. Using 'latin-1' with error replacement.")

    data.columns = ['Wavelength_nm', 'Count']
    data.dropna(subset=['Wavelength_nm'], inplace=True)  # Remove rows with missing wavelengths
    data['Raman_Shift_cm^-1'] = wavelength_to_raman_shift(data['Wavelength_nm'])
    data = data[['Raman_Shift_cm^-1', 'Count']]

    # Save the processed data to a temporary file
    temp_processed_file = file_path + '.tmp'
    data.to_csv(temp_processed_file, sep='\t', header=False, index=False, float_format='%.8f')

    # Append the unprocessed lines to the temporary file
    with open(file_path, 'r', encoding=encoding) as original_file, open(temp_processed_file, 'a') as processed_file:
        # Skip the first nrows lines
        for _ in range(nrows):
            next(original_file)
        # Copy the rest of the lines
        for line in original_file:
            processed_file.write(line)

    # Replace the original file with the temporary file
    os.replace(temp_processed_file, file_path)



# Function to process uploaded folder (archive)
def process_uploaded_folder(file_path, laser_wavelength_nm, nrows):
    import logging

    logger = logging.getLogger(__name__)
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for filename in zip_ref.namelist():
            if not filename.endswith('/'):  # Skip directories within the archive
                try:
                    data_file = zip_ref.open(filename)
                    # Process the extracted file using process_asc_file
                    process_asc_file(data_file, laser_wavelength_nm, nrows)
                    data_file.close()
                    logger.info(f"Successfully processed file: {filename}")
                except Exception as e:
                    logger.error(f"Error processing file: {filename} - {e}")



@app.route('/process', methods=['GET', 'POST'])
def process_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename
            # Check if filename ends with a common archive extension (modify as needed)
            if filename.endswith(('.zip', '.tar')):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                laser_wavelength_nm = float(request.form.get('laser_wavelength_nm', 534.0))
                nrows = int(request.form.get('nrows', 1600))
                process_uploaded_folder(file_path, laser_wavelength_nm, nrows)
                os.remove(file_path)  # Remove uploaded archive after processing
                return redirect(url_for('download_file', filename='processed_folder.txt'))  # Provide a download for processed data
            else:
                # Handle single file upload
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if allowed_file(filename):
                    file.save(file_path)
                    laser_wavelength_nm = float(request.form.get('laser_wavelength_nm', 534.0))
                    nrows = int(request.form.get('nrows', 1600))
                    process_asc_file(file_path, laser_wavelength_nm, nrows)
                    return redirect(url_for('download_file', filename=filename))
                else:
                    return "Invalid file format. Please upload a text file (.txt, .asc, etc.)"
    return render_template('process.html')


@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

