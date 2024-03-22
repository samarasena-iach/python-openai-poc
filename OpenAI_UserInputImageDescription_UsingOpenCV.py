import tkinter as tk
from tkinter import messagebox, filedialog
import openai
import threading
import cv2
from PIL import Image, ImageTk
import base64
import os

# OpenAI API key
os.environ['REQUESTS_CA_BUNDLE'] = 'C:/Users/AU256UR/Downloads/Zscaler Root CA.crt'

# Function to recognize objects in the image using OpenCV
def recognize_objects(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect objects in the image using OpenCV's object detection algorithms
    # For demonstration purposes, we'll simply return a placeholder list of objects
    objects = ["cat", "dog", "car", "person"]
    return objects

# Function to generate text based on recognized objects using GPT-3
def generate_text(objects):
    # Combine recognized objects with a prompt for GPT-3
    prompt = f"I see the following objects in the image: {', '.join(objects)}. Can you describe what's happening in the image?"

    # Generate text based on recognized objects using GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )

    return response.choices[0].text.strip()

# Function to process image file
def process_image():
    # Open file dialog to select image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

    if file_path:
        # Display selected image
        image = Image.open(file_path)
        image = image.resize((300, 300))  # Resize image for display
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

        # Display loading message
        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", "Processing image... Please wait.")
        result_text.config(state="disabled")

        # Process image recognition in a separate thread to prevent GUI freeze
        threading.Thread(target=process_image_thread, args=(file_path,)).start()

def process_image_thread(image_path):
    try:
        # Recognize objects in the image using OpenCV
        objects = recognize_objects(image_path)

        # Generate text based on recognized objects using GPT-3
        description = generate_text(objects)

        # Update result text with image description
        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", description)
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
    root.title("Image Recognition with OpenCV and GPT-3")
    root.geometry("800x600")  # Window size

    # Create button to upload image
    upload_button = tk.Button(root, text="Upload Image", command=process_image, font=("Arial", 14), bg="sky blue", fg="white", width=20)
    upload_button.pack(pady=20)

    # Create label to display image
    global image_label
    image_label = tk.Label(root)
    image_label.pack()

    # Create label for result display
    result_label = tk.Label(root, text="Image Description:", font=("Arial", 12))
    result_label.pack(pady=10)

    # Create text widget to display result
    global result_text
    result_text = tk.Text(root, width=50, height=10, font=("Arial", 12), state="disabled")
    result_text.pack()

    # Run the Tkinter event loop
    root.mainloop()

# Call function to configure GUI
configure_gui()
