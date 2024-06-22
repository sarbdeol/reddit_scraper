# app.py

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from threading import Thread
from ai_crawol import generate_script  # Assuming generate_script is imported correctly

# Function to handle script generation and GUI updates
def generate_script_and_save():
    article_url = url_entry.get()
    if not article_url:
        messagebox.showwarning("Warning", "Please enter a Reddit thread URL.")
        return
    
    # Disable the generate button to prevent multiple clicks
    generate_button.config(state=tk.DISABLED)
    
    # Display "Processing..." label immediately
    processing_label.config(text="Processing...")
    processing_label.grid(row=2, columnspan=2, padx=5, pady=10)
    
    # Start a new thread for script generation
    script_thread = Thread(target=generate_script_worker, args=(article_url,))
    script_thread.start()

# Worker function for script generation
def generate_script_worker(article_url):
    try:
        # Generate script
        script = generate_script(article_url)
        with open('generated_script.txt', 'w', encoding='utf-8') as f:
            f.write(script)
        
        # Update GUI on completion
        root.after(0, lambda: update_gui_on_complete())
        
        messagebox.showinfo("Success", "Script generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        # Re-enable the generate button and hide "Processing..." label
        generate_button.config(state=tk.NORMAL)
        processing_label.config(text="Complete")
        processing_label.after(2000, lambda: processing_label.grid_remove())

# Update GUI elements after script generation completes
def update_gui_on_complete():
    save_label.grid(row=3, columnspan=2, padx=5, pady=10)
    save_button.grid(row=4, column=0, padx=5, pady=10)

# Function to save generated script to a file
def save_file_dialog():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            # Copy generated_script.txt content to selected file_path
            with open('generated_script.txt', 'r', encoding='utf-8') as src_file:
                content = src_file.read()
            
            with open(file_path, 'w', encoding='utf-8') as dest_file:
                dest_file.write(content)
            
            messagebox.showinfo("Success", f"Script saved successfully at:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save script: {str(e)}")

# Function to quit the application
def quit_application():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Reddit Script Generator")
root.geometry("540x200")  # Set initial window size

# Center the window on the screen
root.eval('tk::PlaceWindow . center')

# Set a custom style for ttk widgets
style = ttk.Style()
style.theme_use('default')  # Choose from available themes: 'clam', 'alt', 'default', 'classic'

# Define custom colors for style
root.configure(background='#F0F0F0')  # Set background color for root window

style.configure('Custom.TButton', foreground='white', background='#4CAF50', font=('Helvetica', 12))  # Green for buttons
style.configure('Custom.TLabel', foreground='#333333', background='#F0F0F0', font=('Helvetica', 12))  # Darker text color for labels
style.configure('Custom.TEntry', font=('Helvetica', 12))  # Entry field style

# Create a frame for better organization
frame = tk.Frame(root, padx=20, pady=20, background='#F0F0F0')  # Light gray background for frame
frame.pack(expand=True, fill=tk.BOTH)

# Create a menu bar
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Quit", command=quit_application)
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

# Create a label and entry for Reddit URL
url_label = ttk.Label(frame, text="Enter Reddit Thread URL:", style='Custom.TLabel')
url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
url_entry = ttk.Entry(frame, width=50, style='Custom.TEntry')
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Create a button to generate script
generate_button = ttk.Button(frame, text="Generate Script", style='Custom.TButton', command=generate_script_and_save)
generate_button.grid(row=1, columnspan=2, padx=5, pady=10)

# Create a "Processing..." label (hidden initially)
processing_label = ttk.Label(frame, text="Processing...", style='Custom.TLabel')
processing_label.grid(row=2, columnspan=2, padx=5, pady=10)
processing_label.grid_remove()  # Hide the label initially

# Create a "Complete" label (hidden initially)
save_label = ttk.Label(frame, text="Complete", style='Custom.TLabel')
save_label.grid(row=3, columnspan=2, padx=5, pady=10)
save_label.grid_remove()  # Hide the label initially

# Create a button to save generated script (hidden initially)
save_button = ttk.Button(frame, text="Save Script", style='Custom.TButton', command=save_file_dialog)
save_button.grid(row=4, column=0, padx=5, pady=10)
save_button.grid_remove()  # Hide the button initially

# Run the Tkinter main loop
root.mainloop()
