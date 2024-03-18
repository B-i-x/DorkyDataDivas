# __main__.py
import subprocess
import json

def main():
    # Run the first python file and capture the output
    result = subprocess.run(['python', 'src/gemini/ai.py'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("First script failed", result.stderr)
    
    print(result.stdout)
    # Extract the words and number from the output
    # output = json.loads(result.stdout)
    # print(output)
    # Convert list of words into a space-separated string to pass as arguments
    # words_str = ' '.join(words)
    # print(words, number)
    # Run the second python file with the words and number as arguments
    # subprocess.run(['python', 'ai/process_words.py', "test", str("2")])

if __name__ == "__main__":
    main()
