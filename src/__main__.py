import subprocess

# Define the path to the ai.py file
ai_file_path = 'src/gemini/ai.py'

# Use subprocess to run the python file
result = subprocess.run(['python', ai_file_path], capture_output=True, text=True)

# Check if the subprocess call was successful
if result.returncode == 0:
    print("Success!")
    print("Output:", result.stdout)
else:
    print("An error occurred:", result.stderr)
