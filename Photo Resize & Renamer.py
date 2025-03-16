import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from PIL import Image
import threading


def resize_and_rename(input_paths, output_folder, base_name, progress_bar):
    try:
        total_files = len(input_paths)
        progress_bar['maximum'] = total_files
        
        
        os.makedirs(output_folder, exist_ok=True)
        
        
        def update_progress(count):
            progress_bar['value'] = count
            root.update_idletasks()
        
        
        def next_name(index):
            name = ""
            
            name = chr(97 + index % 26) * (index // 26 + 1) + name
            index = (index // 26) - 1
            return name

        count = 0
        for index, input_path in enumerate(input_paths):
            
            img = Image.open(input_path)
            
            
            img = img.resize((2048, 1536))
            
            
            file_ext = os.path.splitext(input_path)[1]
            
            
            if index == 0:
                output_name = base_name + file_ext
            else:
                output_name = base_name + next_name(index - 1) + file_ext
            output_path = os.path.join(output_folder, output_name)
            
           
            img.save(output_path)
            
            
            count += 1
            update_progress(count)
        
        messagebox.showinfo("Success", "Images resized and renamed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error resizing and renaming images: {str(e)}")


def select_files():
    file_paths = filedialog.askopenfilenames(title="Select Image Files", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_paths:
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if output_folder:
            
            base_name = simpledialog.askstring("Base Name", "Enter base name for renaming:")
            if base_name:
                
                progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate')
                progress_bar.pack(fill=tk.X, padx=10, pady=10)
                
                
                threading.Thread(target=resize_and_rename, args=(file_paths, output_folder, base_name, progress_bar)).start()


root = tk.Tk()
root.title("Image Resizer and Renamer")


file_button = tk.Button(root, text="Select Files", command=select_files)
file_button.pack(pady=10)


root.mainloop()
