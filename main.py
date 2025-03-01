import os
import tkinter as tk
from tkinter import ttk, Label
from PIL import Image, ImageTk

# Set your image folder path
IMAGE_FOLDER = r"C:\Users\koran\PycharmProjects\ChapterNavigator\chapter"


# Function to scan images and categorize them
def get_image_data():
    images = {}

    for filename in os.listdir(IMAGE_FOLDER):
        if filename.startswith("MA8251-") and filename.endswith(".JPG"):
            parts = filename.split("-")
            if len(parts) == 4:
                chapter, topic, step = parts[1], parts[2], parts[3].split(".")[0]

                if chapter not in images:
                    images[chapter] = {}

                if topic not in images[chapter]:
                    images[chapter][topic] = []

                images[chapter][topic].append(step)

    # Sorting logic: first numeric sorting, then alphabetically
    def sort_key(value):
        return (int(value) if value.isdigit() else float('inf'), value.lower())

    for chapter in images:
        images[chapter] = {
            k: sorted(v, key=sort_key) for k, v in sorted(images[chapter].items(), key=lambda item: sort_key(item[0]))
        }

    return images


# Function to update topic dropdown
def update_topics(*args):
    selected_chapter = chapter_var.get()
    topics = sorted(image_data.get(selected_chapter, {}).keys(), key=lambda x: (int(x) if x.isdigit() else float('inf'), x))  # Sort topics
    topic_dropdown["values"] = topics or ["Select"]
    topic_var.set(topics[0] if topics else "Select")
    update_steps()


# Function to update step dropdown
def update_steps(*args):
    selected_chapter = chapter_var.get()
    selected_topic = topic_var.get()
    step_list = sorted(image_data.get(selected_chapter, {}).get(selected_topic, []), key=lambda x: (int(x) if x.isdigit() else float('inf'), x))  # Sort steps

    step_dropdown["values"] = step_list or ["Select"]
    step_var.set(step_list[0] if step_list else "Select")

    update_positions()


# Function to update topic & step position labels
def update_positions():
    selected_chapter = chapter_var.get()
    selected_topic = topic_var.get()
    selected_step = step_var.get()

    topic_list = list(topic_dropdown["values"])
    step_list = image_data.get(selected_chapter, {}).get(selected_topic, [])

    # Update topic position
    if selected_topic in topic_list:
        current_topic_idx = topic_list.index(selected_topic) + 1
        total_topics = len(topic_list)
        topic_position_label.config(text=f"Topic: {current_topic_idx}/{total_topics}")
    else:
        topic_position_label.config(text="Topic: 0/0")

    # Update step position
    if selected_step in step_list:
        current_step_idx = step_list.index(selected_step) + 1
        total_steps = len(step_list)
        step_position_label.config(text=f"Step: {current_step_idx}/{total_steps}")
    else:
        step_position_label.config(text="Step: 0/0")


# Function to display selected image
def display_image():
    selected_chapter = chapter_var.get()
    selected_topic = topic_var.get()
    selected_step = step_var.get()

    if selected_step == "Select":
        return

    image_path = os.path.join(IMAGE_FOLDER, f"MA8251-{selected_chapter}-{selected_topic}-{selected_step}.JPG")

    if not os.path.exists(image_path):
        image_label.config(text="Image Not Found", image="")
        return

    img = Image.open(image_path)
    img = img.resize((window_width, window_height - 150), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)

    image_label.config(image=img)
    image_label.image = img
    image_label.config(text="")

    update_positions()


# Function to move to the next topic
def next_topic(event=None):
    topic_list = list(topic_dropdown["values"])
    if topic_var.get() in topic_list:
        idx = topic_list.index(topic_var.get())
        if idx < len(topic_list) - 1:
            topic_var.set(topic_list[idx + 1])
            update_steps()
            display_image()


# Function to move to the previous topic
def prev_topic(event=None):
    topic_list = list(topic_dropdown["values"])
    if topic_var.get() in topic_list:
        idx = topic_list.index(topic_var.get())
        if idx > 0:
            topic_var.set(topic_list[idx - 1])
            update_steps()
            display_image()


# Function to move to the next step
def next_step(event=None):
    step_list = list(step_dropdown["values"])
    if step_var.get() in step_list:
        idx = step_list.index(step_var.get())
        if idx < len(step_list) - 1:
            step_var.set(step_list[idx + 1])
            display_image()


# Function to move to the previous step
def prev_step(event=None):
    step_list = list(step_dropdown["values"])
    if step_var.get() in step_list:
        idx = step_list.index(step_var.get())
        if idx > 0:
            step_var.set(step_list[idx - 1])
            display_image()


# Load image data
image_data = get_image_data()

# Create Tkinter Window (Reduced Size)
root = tk.Tk()
root.title("MA8251 Image Viewer")

# Set window size
window_width = int(root.winfo_screenwidth() * 0.9)
window_height = int(root.winfo_screenheight() * 0.9)
root.geometry(f"{window_width}x{window_height}+50+50")

# Dropdown Variables
chapter_var = tk.StringVar(value="Select")
topic_var = tk.StringVar(value="Select")
step_var = tk.StringVar(value="Select")

# Add placeholder chapters if there are fewer than 10
chapter_list = list(image_data.keys())
for i in range(len(chapter_list), 10):
    chapter_list.append(f"Chapter {i + 1}")

# UI Layout
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

ttk.Label(frame_top, text="Chapter:").grid(row=0, column=0, padx=10, pady=5)
chapter_dropdown = ttk.Combobox(frame_top, textvariable=chapter_var, values=chapter_list)
chapter_dropdown.grid(row=0, column=1, padx=10, pady=5)
chapter_dropdown.bind("<<ComboboxSelected>>", update_topics)

ttk.Label(frame_top, text="Topic:").grid(row=0, column=2, padx=10, pady=5)
topic_dropdown = ttk.Combobox(frame_top, textvariable=topic_var, values=["Select"])
topic_dropdown.grid(row=0, column=3, padx=10, pady=5)
topic_dropdown.bind("<<ComboboxSelected>>", update_steps)

ttk.Label(frame_top, text="Step:").grid(row=0, column=4, padx=10, pady=5)
step_dropdown = ttk.Combobox(frame_top, textvariable=step_var, values=["Select"])
step_dropdown.grid(row=0, column=5, padx=10, pady=5)

# Topic & Step Position Labels
topic_position_label = ttk.Label(frame_top, text="Topic: 0/0", font=("Arial", 12, "bold"))
topic_position_label.grid(row=0, column=6, padx=10, pady=5)

step_position_label = ttk.Label(frame_top, text="Step: 0/0", font=("Arial", 12, "bold"))
step_position_label.grid(row=0, column=7, padx=10, pady=5)

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

ttk.Button(frame_buttons, text="Previous Topic", command=prev_topic).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(frame_buttons, text="Previous Step", command=prev_step).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(frame_buttons, text="Show Image", command=display_image).grid(row=0, column=2, padx=10, pady=5)
ttk.Button(frame_buttons, text="Next Step", command=next_step).grid(row=0, column=3, padx=10, pady=5)
ttk.Button(frame_buttons, text="Next Topic", command=next_topic).grid(row=0, column=4, padx=10, pady=5)

# Bind arrow keys for navigation
root.bind("<Up>", prev_topic)
root.bind("<Down>", next_topic)
root.bind("<Left>", prev_step)
root.bind("<Right>", next_step)

# Image Label
image_label = Label(root, text="No Image Selected")
image_label.pack(fill="both", expand=True)

# Run Tkinter Loop
root.mainloop()
