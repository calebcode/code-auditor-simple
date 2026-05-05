import ollama
import sys
import os
import uuid

def audit_code(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, "r") as f:
        code_content = f.read()

    filename = str(uuid.uuid1()) + ".md"

    # Define path for the output file
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, 'output')
    output_path = os.path.join(output_dir, filename)

    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"--- Auditing {file_path} via Local LLM ---")

        # Define the system instructions to keep the model focused
        system_prompt = (
            "You are a Senior Systems Engineer. Analyze the provided code "
            "and list 3 specific edge cases or failure modes that could occur "
            "in a production environment. Be concise and technical."
        )

        # Use streaming to see the 'thought process' in real-time
        stream = ollama.chat(
            model='qwen2.5-coder:7b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Analyze this code:\n\n{code_content}"},
            ],
            stream=True,
        )

        with open(output_path, 'a') as md_file:
            md_file.write(f"Auditing file: {file_path}\n\n")

            for chunk in stream:
                md_file.write(chunk['message']['content'])

            md_file.write("\n--- Audit Complete ---")
        
        print(f"\n--- Audit Complete. See log file at {output_path} ---")

    except Exception as e:
        print(f"An error occured: {e}")

    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auditor.py <path_to_file>")
    else:
        audit_code(sys.argv[1])