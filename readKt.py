import sys
import openai
import os
import re
# Set your OpenAI GPT-3 API key
openai.api_key = ''
def generate_response1(kotlin_code,test_folder):
    conversation = [
        {"role": "system", "content": "You are a test case generator."},
        {"role": "user", "content": f"Generate test cases in kotlin code for the following Kotlin code:\n\n{kotlin_code}"},
        {"role": "assistant", "content": "Please generate pure kotlin class without any comments or points and assert test cases for the given Kotlin code."}
    ]
    # Make the API call to ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=500  # Adjust max_tokens as needed
    )
    print(response)
    test_cases = response['choices'][0]['message']['content']
   # Save the test cases to the specified filepath
    kotlin_code_match = re.search(r'```kotlin(.*?)```', test_cases, re.DOTALL)
    if kotlin_code_match:
      kotlin_code_test = kotlin_code_match.group(1).strip()
      print(kotlin_code_test)
      file_path = os.path.join(test_folder, "Test.kt")
      with open(file_path, 'w') as file:
        file.write(kotlin_code_test)
    else:
      print("No Kotlin code found.")
    print(test_cases)
def read_kotlin_file(file_path):
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <test_folder>")
        sys.exit(1)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            kotlin_code = file.read()
            print("Kotlin test Code:")
            print(kotlin_code)
            return kotlin_code
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        return None
# Check if the correct number of command line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python script_name.py <path_to_kotlin_file>")
    sys.exit(1)
# Take the Kotlin source code file path from the command line argument
kotlin_file_path = sys.argv[1]
test_folder = sys.argv[2]
# Call the function to read the Kotlin file content
kotlin_code = read_kotlin_file(kotlin_file_path)
test_code = generate_response1(kotlin_code,test_folder)
# if kotlin_code is not None:
#     print(kotlin_code)
#     # print("Kotlin test Code:")
#     # print(test_code)
