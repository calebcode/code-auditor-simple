import ollama
import sys
import os

def audit_code(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    with open(file_path, "r") as f:
        code_content = f.read()

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

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    print("\n--- Audit Complete ---")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auditor.py <path_to_file>")
    else:
        audit_code(sys.argv[1])