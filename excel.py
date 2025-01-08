import os
import subprocess
import time
import openpyxl

# Compile the C++ program
subprocess.run(["g++", "-o", "projeto", "projeto.cpp"])

# Directory containing test files
test_dir = "bigggtest"

# List to store results
results = []

# Run tests and measure time
for test_file in os.listdir(test_dir):
   
    input_path = os.path.join(test_dir, test_file)

    # Read input variables from the input file
    with open(input_path, "r") as f:
        input_data = f.read().strip()
        input_lines = input_data.splitlines()
        if input_lines:
            first_line = input_lines[0]
            input_variables = first_line.split()[:3]  # Get the first 3 integers

    # Measure execution time
    start_time = time.time()
    subprocess.run(["./projeto"], input=input_data, text=True, capture_output=True)
    end_time = time.time()
    execution_time = end_time - start_time

    # Store the input variables and execution time
    results.append((input_variables, execution_time))

# Create an Excel workbook and sheet
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Test Results"

# Write headers
ws.append(["Input Variable 1", "Input Variable 2", "Input Variable 3", "Execution Time (s)"])

# Write results to the sheet
for input_vars, exec_time in results:
    ws.append([input_vars[0], input_vars[1], input_vars[2], exec_time])

# Save the workbook
excel_file = "test_results.xlsx"
wb.save(excel_file)

print(f"Results saved to {excel_file}")