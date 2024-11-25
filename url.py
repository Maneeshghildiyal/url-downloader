import tkinter as tk
from tkinter import messagebox
import requests
import os

# Function to validate URL
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

# Function to download the file
def download_file():
    url = url_entry.get().strip()  # Get and clean the URL from the entry field
    file_name = file_name_entry.get().strip()  # Get and clean the file name

    # Validate inputs
    if not url or not file_name:
        result_label.config(text="Please enter both a URL and a file name.", fg="red")
        return

    if not is_valid_url(url):
        result_label.config(text="Invalid URL. Please start with http:// or https://", fg="red")
        return

    if not os.path.splitext(file_name)[1]:  # Check for file extension
        result_label.config(text="File name must include an extension (e.g., .txt, .jpg).", fg="red")
        return

    try:
        # Send a GET request to the provided URL
        response = requests.get(url, timeout=10)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the content to the specified file
            with open(file_name, 'wb') as file:
                file.write(response.content)
            result_label.config(text=f"File '{file_name}' downloaded successfully.", fg="green")
        else:
            result_label.config(text=f"Failed to download. Status code: {response.status_code}", fg="red")
    except requests.exceptions.MissingSchema:
        result_label.config(text="Invalid URL format. Please check the URL and try again.", fg="red")
    except requests.exceptions.ConnectionError:
        result_label.config(text="Connection error. Please check your internet connection.", fg="red")
    except requests.exceptions.Timeout:
        result_label.config(text="Request timed out. Please try again later.", fg="red")
    except Exception as e:
        result_label.config(text=f"An unexpected error occurred: {e}", fg="red")

# Create the main window
root = tk.Tk()
root.title("File Downloader")
root.geometry("800x400")  # Set the window size

# Label and Entry for URL
url_label = tk.Label(root, text="Enter URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Label and Entry for file name
file_name_label = tk.Label(root, text="Enter File Name (with extension):")
file_name_label.pack(pady=5)
file_name_entry = tk.Entry(root, width=50)
file_name_entry.pack(pady=5)

# Button to trigger the download_file function
download_button = tk.Button(root, text="Download", command=download_file)
download_button.pack(pady=10)

# Label to display result or error message
result_label = tk.Label(root, text="", wraplength=700, justify="left", fg="blue")
result_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()
