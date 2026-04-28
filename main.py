import tkinter as tk
from tkinter import messagebox
import random
import string
import json

try:
    with open("passwords.json", "r", encoding="utf-8") as f:
        passwords = json.load(f)
except:
    passwords = []

def save():
    with open("passwords.json", "w", encoding="utf-8") as f:
        json.dump(passwords, f, indent=4)

def show_list():
    box.delete(0, tk.END)
    if not passwords:
        box.insert(0, "Пусто")
        return
    for i, p in enumerate(passwords[-10:], 1):
        box.insert(tk.END, f"{i}. {p['pwd']} | {p['len']} симв.")

def create():
    try:
        length = int(spin.get())
        if length < 4:
            messagebox.showerror("Ошибка", "Минимум 4 символа!")
            return
        if length > 30:
            messagebox.showerror("Ошибка", "Максимум 30 символов!")
            return
    except:
        messagebox.showerror("Ошибка", "Введите число!")
        return
    
    chars = ""
    if chk1.get():
        chars += string.ascii_letters
    if chk2.get():
        chars += string.digits
    if chk3.get():
        chars += "!@#$%&*"
    
    if not chars:
        messagebox.showerror("Ошибка", "Выберите символы!")
        return
    
    pwd = "".join(random.choice(chars) for _ in range(length))
    
    result.config(text=pwd)
    
    passwords.append({"pwd": pwd, "len": length})
    save()
    show_list()

def copy():
    p = result.cget("text")
    if p and p != "Жми на кнопку":
        root.clipboard_clear()
        root.clipboard_append(p)
        messagebox.showinfo("Ок", "Скопировано!")

def clear():
    if messagebox.askyesno("Очистка", "Точно?"):
        global passwords
        passwords = []
        save()
        show_list()

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x550")  # Исправлено: x вместо _

tk.Label(root, text="ПАРОЛЬНЫЙ ГЕНЕРАТОР", font=("Arial", 12, "bold")).pack(pady=10)

# Длина
len_frame = tk.Frame(root)
len_frame.pack(pady=5)
tk.Label(len_frame, text="Длина:").pack(side="left")
spin = tk.Spinbox(len_frame, from_=4, to=30, width=8)
spin.delete(0, tk.END)
spin.insert(0, "12")
spin.pack(side="left", padx=5)

# Чекбоксы
chk1 = tk.BooleanVar(value=True)
chk2 = tk.BooleanVar(value=True)
chk3 = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Буквы A-z", variable=chk1).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Цифры 0-9", variable=chk2).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Символы !@#$%&*", variable=chk3).pack(anchor="w", padx=40)

tk.Button(root, text="СГЕНЕРИРОВАТЬ", command=create, bg="green", fg="white").pack(pady=10)

result = tk.Label(root, text="Жми на кнопку", font=("Courier", 10), fg="red")
result.pack()

tk.Button(root, text="КОПИРОВАТЬ", command=copy, bg="orange").pack(pady=5)

tk.Label(root, text="ИСТОРИЯ", font=("Arial", 10)).pack()
box = tk.Listbox(root, height=8, width=45)
box.pack(pady=5)

tk.Button(root, text="ОЧИСТИТЬ", command=clear, bg="red", fg="white").pack(pady=5)

show_list()
root.mainloop()