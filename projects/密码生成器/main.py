import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip  # 需要安装 pip install pyperclip

def generate_password():
    """生成密码并显示到界面"""
    try:
        length = int(length_var.get())
    except ValueError:
        messagebox.showerror("输入错误", "密码长度必须是整数！")
        return

    # 构造字符集
    char_set = ''
    if var_digits.get():
        char_set += string.digits
    if var_upper.get():
        char_set += string.ascii_uppercase
    if var_lower.get():
        char_set += string.ascii_lowercase
    if var_symbols.get():
        char_set += string.punctuation

    if not char_set:
        messagebox.showwarning("未选择字符类型", "请至少勾选一种字符类型！")
        return

    # 生成密码
    password = ''.join(random.choice(char_set) for _ in range(length))
    password_var.set(password)

def copy_to_clipboard():
    """复制密码到剪贴板"""
    pwd = password_var.get()
    if pwd:
        pyperclip.copy(pwd)
        messagebox.showinfo("已复制", "密码已复制到剪贴板。")
    else:
        messagebox.showwarning("无密码", "请先生成密码。")

# 创建主窗口
root = tk.Tk()
root.title("密码生成器")
root.geometry("800x600")
root.resizable(False, False)
root.configure(bg="#e6f3ff")  # 设置窗口背景色为浅灰色

# 密码长度
tk.Label(root, text="密码长度：").pack(pady=5)
length_var = tk.StringVar(value="12")
tk.Entry(root, textvariable=length_var, width=10, justify='center').pack()

# 字符类型勾选
var_digits = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="包含数字", variable=var_digits).pack(anchor='w', padx=80)
tk.Checkbutton(root, text="包含大写字母", variable=var_upper).pack(anchor='w', padx=80)
tk.Checkbutton(root, text="包含小写字母", variable=var_lower).pack(anchor='w', padx=80)
tk.Checkbutton(root, text="包含特殊符号", variable=var_symbols).pack(anchor='w', padx=80)

# 生成按钮
tk.Button(root, text="生成密码", command=generate_password).pack(pady=5)

# 显示密码
password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, font=("Consolas", 12), justify='center', state='readonly').pack(pady=5)

# 复制按钮
tk.Button(root, text="复制到剪贴板", command=copy_to_clipboard).pack(pady=5)

# 启动主循环
root.mainloop()
