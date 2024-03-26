import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import threading
import os
import json

# OpenAI API key
os.environ['REQUESTS_CA_BUNDLE'] = 'C:/Users/AU256UR/Downloads/Zscaler Root CA.crt'

# Function to get completion from OpenAI ChatGPT
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

# Function to generate Terraform script from JSON content
def generate_terraform(json_content):
    try:
        # Prompt for generating Terraform script
        prompt = "Generate a terraform script for the following JSON content:\n" + json_content
        # Get completion from OpenAI ChatGPT
        terraform_script = get_completion(prompt)
        return terraform_script
    except Exception as e:
        return f"Error generating Terraform script: {str(e)}"

# Function to process prompt from user input
def process_prompt():
    # Get user input from text widget
    prompt = prompt_text.get("1.0", "end-1c")
    if prompt.strip() == "":
        messagebox.showerror("Error", "Please enter a prompt.")
    else:
        # Display loading message
        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", "Generating the Terraform Script, Please wait...")

        # Process prompt in a separate thread to prevent GUI freeze
        threading.Thread(target=get_completion, args=(prompt,)).start()

# Function to process JSON file upload
def process_json_upload():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            json_content = file.read()
        # Display JSON content in input text area
        prompt_text.delete("1.0", "end")
        prompt_text.insert("1.0", json_content)
        # Generate Terraform script
        generate_terraform_from_json(json_content)

# Function to generate Terraform script from JSON content
def generate_terraform_from_json(json_content):
    # Display loading message
    result_text.config(state="normal")
    result_text.delete("1.0", "end")
    # result_text.insert("1.0", "Generating the Terraform Script, Please wait...")

    # Process prompt in a separate thread to prevent GUI freeze
    threading.Thread(target=generate_terraform_from_json_thread, args=(json_content,)).start()

# Function to generate Terraform script in a separate thread
def generate_terraform_from_json_thread(json_content):
    try:
        # Generate Terraform script from JSON content
        terraform_script = generate_terraform(json_content)
        # Update result text with Terraform script
        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", terraform_script)
    except Exception as e:
        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", f"Error: {str(e)}")
    finally:
        result_text.config(state="disabled")

# Function to create and configure Tkinter window and widgets
def configure_gui():
    # Create main Tkinter window
    root = tk.Tk()
    root.title("InfraWiz POC - ChatGPT Prompt Processor")
    root.resizable(width=False, height=False)

    # Set window size
    window_width = 960
    window_height = 520
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(
        f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")  # Width x Height + X Offset + Y Offset

    # Input Components (Label & Prompt Input Text Area)
    prompt_label = tk.Label(root, text="JSON File (Preview)", font=("Arial", 12))
    prompt_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    global prompt_text
    prompt_text = tk.Text(root, width=65, height=25, font=("Arial", 10))
    prompt_text.grid(row=1, column=0, padx=10, pady=5)
    prompt_text.focus_set()

    # Output Components (Label & ChatGPT Response Text Area)
    result_label = tk.Label(root, text="Terraform Script (Preview)", font=("Arial", 12))
    result_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    global result_text
    result_text = tk.Text(root, width=65, height=25, font=("Arial", 10), state="disabled")  # Increased height here
    result_text.grid(row=1, column=1, padx=10, pady=5)

    # Button - To upload JSON file
    upload_button = tk.Button(root, text="(1) Upload JSON", command=process_json_upload, font=("Arial", 12), bg="yellow", fg="black", width=20)
    upload_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Button - To start processing the prompt
    process_button = tk.Button(root, text="(2) Generate IaC", command=process_prompt, font=("Arial", 12), bg="yellow", fg="black", width=20)
    process_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    # Run the Tkinter event loop
    root.mainloop()

# Call function to configure GUI
configure_gui()
