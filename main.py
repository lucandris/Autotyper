import time
import random
import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading

stop_typing = False

def human_typing(text, min_delay=0.05, max_delay=0.15, introduce_mistakes=False, slow_down_quotes=False, error_prob=0.01):
    global stop_typing

    def introduce_typing_mistakes(char):
        if introduce_mistakes and random.random() < error_prob:
            mistake = random.choice("abcdefghijklmnopqrstuvwxyz")
            pyautogui.typewrite(mistake)
            time.sleep(random.uniform(min_delay, max_delay))
            pyautogui.press('backspace')
        return char

    for char in text:
        if stop_typing:
            break
        if slow_down_quotes and char in "\"'":
            time.sleep(random.uniform(min_delay * 2, max_delay * 2))
        
        char = introduce_typing_mistakes(char)
        pyautogui.typewrite(char)
        
        variable_delay = random.uniform(min_delay * 0.8, max_delay * 1.2)
        time.sleep(variable_delay)

def start_typing():
    global stop_typing
    
    text_to_type = text_input.get("1.0", "end-1c")
    try:
        wpm = float(wpm_entry.get())
        error_prob = float(error_prob_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for WPM and Error Probability.")
        return
    
    if wpm <= 0:
        messagebox.showerror("Invalid input", "WPM should be greater than 0.")
        return

    if not (0 <= error_prob <= 1):
        messagebox.showerror("Invalid input", "Error probability should be between 0 and 1.")
        return

    time_per_word = 60 / wpm
    time_per_char = time_per_word / 5

    min_delay = time_per_char * 0.6
    max_delay = time_per_char * 1.4

    introduce_mistakes = mistake_var.get()
    slow_down_quotes = quotes_var.get()

    time.sleep(5)

    stop_typing = False
    typing_thread = threading.Thread(target=human_typing, args=(text_to_type, min_delay, max_delay, introduce_mistakes, slow_down_quotes, error_prob))
    typing_thread.start()

def stop_typing_func():
    global stop_typing
    stop_typing = True
    messagebox.showinfo("Stopped", "Typing process has been stopped.")

root = tk.Tk()
root.title("Typing Simulator")

text_label = tk.Label(root, text="Text to Type:")
text_label.pack(pady=5)
text_input = tk.Text(root, height=10, width=50)
text_input.pack(pady=5)

wpm_label = tk.Label(root, text="Words per minute (WPM):")
wpm_label.pack(pady=5)
wpm_entry = tk.Entry(root)
wpm_entry.pack(pady=5)
wpm_entry.insert(0, "75")

error_prob_label = tk.Label(root, text="Error Probability (0 to 1):")
error_prob_label.pack(pady=5)
error_prob_entry = tk.Entry(root)
error_prob_entry.pack(pady=5)
error_prob_entry.insert(0, "0.01")

mistake_var = tk.BooleanVar()
mistake_checkbox = tk.Checkbutton(root, text="Introduce spelling mistakes", variable=mistake_var)
mistake_checkbox.pack(pady=5)

quotes_var = tk.BooleanVar()
quotes_checkbox = tk.Checkbutton(root, text="Slow down at quotes", variable=quotes_var)
quotes_checkbox.pack(pady=5)

start_button = tk.Button(root, text="Start Typing", command=start_typing)
start_button.pack(pady=5)
stop_button = tk.Button(root, text="Stop Typing", command=stop_typing_func)
stop_button.pack(pady=5)

root.mainloop()
