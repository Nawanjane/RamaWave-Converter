def count_rows_after_start(filename, start_row=1603):
  """
  Counts the number of rows in an ASCII file after a specified starting row.

  Args:
      filename: The path to the ASCII file.
      start_row: The row number from which to start counting (inclusive). Defaults to 1603.

  Returns:
      The number of rows after the starting row.
  """
  num_rows = 0
  with open(filename, 'r') as file:
    for _ in range(start_row - 1):  # Skip rows before the starting row
      next(file)

    for line in file:
      num_rows += 1

  return num_rows

# Example usage
filename = "/Users/leopard/Desktop/position_01.asc"
start_row = 1603  # Modify this if needed
num_rows_after_start = count_rows_after_start(filename, start_row)

print(f"Number of rows after row {start_row}: {num_rows_after_start}")

import os

def count_and_copy_rows(filename, start_row=1603, temp_filename="temp.txt"):
    """
    Counts the number of rows in an ASCII file after a specified starting row,
    copies those rows to a temporary text file, and runs a second Python script.
    """

    try:
        # Create the temporary file (or open it if it exists)
        with open(temp_filename, 'w') as output_file:
            for _ in range(start_row - 1):
                next(open(filename, 'r'))  # Skip lines before starting row

            for line in open(filename, 'r'):
                output_file.write(line)

        num_rows_copied = count_rows_after_start(filename, start_row)
        print(f"Number of rows copied to {temp_filename}: {num_rows_copied}")
        temp_file_path = os.path.abspath(temp_filename)
        print(f"Absolute path of temporary file: {temp_file_path}")
        # Run the second Python script
        import subprocess
        subprocess.run(["python", "/Users/leopard/Desktop/second.py"])

    except FileNotFoundError as e:
        print(f"Error: Could not open file '{filename}'.")
    except PermissionError as e:
        print(f"Error: Script does not have permission to create '{temp_filename}'.")
    except Exception as e:  # Catch other unexpected errors
        print(f"An unexpected error occurred: {e}")

# Example usage
filename = "/Users/leopard/Desktop/position_01.asc"  # Replace with your actual file path
count_and_copy_rows(filename)
