import tkinter as tk
from tkinter import filedialog, messagebox, ttk, LEFT
from tkinter.font import Font
from datetime import datetime
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

    download_button.config(state="normal")
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
    # Disable all the buttons upon calling events
    upload_button.config(state="disabled")
    process_button.config(state="disabled")
    download_button.config(state="disabled")

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

# Function to download Terraform script
def download_terraform_script():
    terraform_script = result_text.get("1.0", "end-1c")

    # Get current time in milliseconds
    current_time_milliseconds = datetime.now().strftime("%Y%m%d%H%M%S%f")
    save_terraform_to_file(terraform_script, f"infrawiz_tf_{current_time_milliseconds}")

# Function to save Terraform script to file
def save_terraform_to_file(terraform_script, filename):
    try:
        file_path = os.path.join("TerraformScripts", f"{filename}.tf")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(terraform_script)
        messagebox.showinfo("Success", "Terraform script downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving Terraform script: {str(e)}")

# Function to create and configure Tkinter window and widgets
def configure_gui():
    # Create main Tkinter window
    root = tk.Tk()
    root.title("InfraWiz POC - ChatGPT Prompt Processor")
    root.resizable(width=False, height=False)
    root['bg'] = '#FFE4E1'

    # Set window size
    window_width = 960
    window_height = 520
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")  # Width x Height + X Offset + Y Offset

    # Input Components (Label & Prompt Input Text Area) ===============================================================>
    prompt_label = tk.Label(root, text="JSON File (Preview)", font=("Arial", 12, 'bold'))
    prompt_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    prompt_label['bg'] = '#FFE4E1'

    global prompt_text
    prompt_text = tk.Text(root, width=65, height=25, font=("Consolas", 10))
    prompt_text.grid(row=1, column=0, padx=10, pady=5)
    prompt_text.focus_set()

    # Output Components (Label & ChatGPT Response Text Area)
    result_label = tk.Label(root, text="Terraform Script (Preview)", font=("Arial", 12, 'bold'))
    result_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
    result_label['bg'] = '#FFE4E1'

    global result_text
    result_text = tk.Text(root, width=65, height=25, font=("Consolas", 10), state="disabled")
    result_text.grid(row=1, column=1, padx=10, pady=5)
    # =================================================================================================================>

    # Buttons =========================================================================================================>
    # Load icons
    upload_button_icon = tk.PhotoImage(file="Icons/upload_button.png").subsample(16, 16)
    process_button_icon = tk.PhotoImage(file="Icons/process_button.png").subsample(16, 16)
    download_button_icon = tk.PhotoImage(file="Icons/download_button.png").subsample(16, 16)

    # Button - To upload JSON file
    global upload_button
    upload_button = tk.Button(root, text="(1) Upload JSON", image=upload_button_icon, compound=LEFT, command=process_json_upload, font=("Arial", 11, 'bold'), bg="#FFDAB9", fg="black", width=180)
    upload_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Button - To start processing the prompt
    global process_button
    process_button = tk.Button(root, text="(2) Generate IaC", image=process_button_icon, compound=LEFT, command=process_prompt, font=("Arial", 11, 'bold'), bg="#FFDAB9", fg="black", width=180)
    process_button.grid(row=2, column=1, padx=5, pady=10, sticky="w")

    # Button - To download Terraform script
    global download_button
    download_button = tk.Button(root, text="(3) Download IaC", image=download_button_icon, compound=LEFT, command=download_terraform_script, font=("Arial", 11, 'bold'), bg="#FFDAB9", fg="black", width=180)
    download_button.grid(row=2, column=1, padx=5, pady=10, sticky="e")
    # =================================================================================================================>

    # Run the Tkinter event loop
    root.mainloop()

# Call function to configure GUI
configure_gui()
