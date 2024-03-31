import os
import subprocess


def copy_rows_to_temp(filename, start_row=1603, temp_folder="temp"):
    """
    Copies rows from a specified starting row in an ASCII file to a temporary file in a specified folder.

    Args:
        filename: The path to the ASCII file.
        start_row: The row number from which to start copying (inclusive). Defaults to 1603.
        temp_folder: The folder where the temporary file will be saved. Defaults to "temp/".
    """

    try:
        os.makedirs(temp_folder, exist_ok=True)  # Create the temp folder if it doesn't exist
        temp_filename = os.path.join(temp_folder, "temp.txt")  # Construct full temp file path

        with open(filename, 'r') as input_file, open(temp_filename, 'w') as output_file:
            for _ in range(start_row - 1):
                next(input_file)  # Skip lines before starting row

            for line in input_file:
                output_file.write(line)

        # Call the second Python script after copying
        subprocess.run(["python", "script/second.py"])

    except FileNotFoundError as e:
        print(f"Error: Could not open file '{filename}'.")
    except PermissionError as e:
        print(f"Error: Script does not have permission to create files in '{temp_folder}'.")
    except Exception as e:  # Catch other unexpected errors
        print(f"An unexpected error occurred: {e}")

# Example usage
filename = "Data/position_01.asc"  # Replace with your actual file path
copy_rows_to_temp(filename)
