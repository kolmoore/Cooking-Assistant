import tkinter as tk
from tkinter import messagebox
import bot_chat

# Function to submit message
def submit_message():
    message_text = message_entry.get()
    message = {'role':'user',
               'content':message_text,}
    if message != "":
        try:
            chat_log.append(message) 
        except:
            aide = "Cooking Aide"
            chat_log = bot_chat.init(aide)
            chat_log.append(message)    
        response, chat_log = bot_chat.receive(chat_log)
        
        assistant.config(text = response,wraplength=300)
        message_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("You must enter something")

# Create the main window
root = tk.Tk()
root.title("ChefBot - AI Cooking Assistant")
root.geometry("400x400")

# Textbox to display the AI Response
assistant = tk.Label(root, text = "Say Hello")
assistant.pack(pady=20)

# Entry box to submit new messages
message_entry = tk.Entry(root, width=100)
message_entry.pack(pady=10)
message_entry.insert(0, "Hello")


# Submit Message Button
enter_button = tk.Button(root, text="Enter", command=submit_message)
enter_button.pack(pady=10)
root.bind('<Return>', lambda event: submit_message)


# Run the main loop
root.mainloop()