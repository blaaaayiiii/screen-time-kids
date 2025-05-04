import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import threading
import os

# 初始时间设置（秒）
app_limits = {
    "YouTube": 10,
    "Game": 8
}

app_locked = {
    "YouTube": False,
    "Game": False
}

admin_password = "1234"  # 家长解锁密码

# 日志记录
def log_usage(app_name, used_time):
    with open("usage_log.txt", "a") as f:
        f.write(f"{app_name} was used for {used_time} seconds.\n")

# 倒计时窗口
def countdown_window(app_name, time_limit):
    win = tk.Toplevel()
    win.title(f"{app_name} Running")
    win.geometry("300x130")
    label = tk.Label(win, text="", font=("Arial", 16))
    label.pack(pady=20)

    def countdown():
        for remaining in range(time_limit, 0, -1):
            label.config(text=f"{app_name} running...\nTime left: {remaining} sec")
            time.sleep(1)
        label.config(text=f"{app_name} has been locked!")
        app_locked[app_name] = True
        log_usage(app_name, time_limit)
        messagebox.showinfo("Time Up", f"{app_name} is now locked.")
        win.destroy()

    threading.Thread(target=countdown).start()

# 启动 App
def open_app(app_name, button):
    if app_locked[app_name]:
        messagebox.showwarning("Locked", f"{app_name} is already locked!")
    else:
        countdown_window(app_name, app_limits[app_name])
        button.config(state="disabled")

# ============ 切换界面功能 ============
def show_dashboard():
    welcome_frame.pack_forget()
    dashboard_frame.pack()

def show_settings():
    dashboard_frame.pack_forget()
    settings_frame.pack()

def save_settings():
    try:
        yt_time = int(entry_youtube.get())
        game_time = int(entry_game.get())
        app_limits["YouTube"] = yt_time
        app_limits["Game"] = game_time
        messagebox.showinfo("Saved", "Time limits updated successfully.")
        settings_frame.pack_forget()
        dashboard_frame.pack()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# 使用记录统计窗口
def show_usage_summary():
    if not os.path.exists("usage_log.txt"):
        messagebox.showinfo("No Records", "No usage log found yet.")
        return

    usage = {"YouTube": 0, "Game": 0}
    with open("usage_log.txt", "r") as f:
        for line in f:
            for app in usage:
                if line.startswith(app):
                    try:
                        seconds = int(line.strip().split(" ")[-2])
                        usage[app] += seconds
                    except:
                        continue

    win = tk.Toplevel()
    win.title("📊 Usage Summary")
    win.geometry("300x150")

    summary = "\n".join([f"{app}: {usage[app]} seconds" for app in usage])
    label = tk.Label(win, text=summary, font=("Arial", 14), justify="left")
    label.pack(pady=20)

# 解锁功能
def unlock_apps():
    pwd = simpledialog.askstring("Unlock", "Enter parent password:", show="*")
    if pwd == admin_password:
        for app in app_locked:
            app_locked[app] = False
        yt_button.config(state="normal")
        game_button.config(state="normal")
        messagebox.showinfo("Unlocked", "All apps have been unlocked.")
    else:
        messagebox.showerror("Wrong Password", "Incorrect password. Try again.")

# ============ 主窗口 ============

root = tk.Tk()
root.title("Screen Time Saver for Kids")
root.geometry("430x370")

# ===== 欢迎界面 =====
welcome_frame = tk.Frame(root)
welcome_label = tk.Label(welcome_frame, text="👋 Welcome to Screen Time Saver!", font=("Arial", 16))
welcome_label.pack(pady=30)
start_button = tk.Button(welcome_frame, text="Start Using", font=("Arial", 14), width=18, command=show_dashboard)
start_button.pack()
welcome_frame.pack()

# ===== 控制台界面 =====
dashboard_frame = tk.Frame(root)

title_label = tk.Label(dashboard_frame, text="Select an app to run:", font=("Arial", 14))
title_label.pack(pady=10)

frame = tk.Frame(dashboard_frame)
frame.pack()

yt_button = tk.Button(frame, text="Open YouTube", font=("Arial", 12), width=15,
                      command=lambda: open_app("YouTube", yt_button))
game_button = tk.Button(frame, text="Open Game", font=("Arial", 12), width=15,
                        command=lambda: open_app("Game", game_button))

yt_button.grid(row=0, column=0, padx=10, pady=10)
game_button.grid(row=0, column=1, padx=10, pady=10)

# 控制台功能按钮
settings_button = tk.Button(dashboard_frame, text="⚙ Settings", font=("Arial", 12), command=show_settings)
settings_button.pack(pady=5)

summary_button = tk.Button(dashboard_frame, text="📊 Usage History", font=("Arial", 12), command=show_usage_summary)
summary_button.pack(pady=5)

unlock_button = tk.Button(dashboard_frame, text="🔓 Unlock Apps", font=("Arial", 12), command=unlock_apps)
unlock_button.pack(pady=5)

# ===== 设置界面 =====
settings_frame = tk.Frame(root)

label_setting = tk.Label(settings_frame, text="🛠 Set Time Limits (in seconds)", font=("Arial", 14))
label_setting.pack(pady=10)

entry_youtube = tk.Entry(settings_frame, font=("Arial", 12))
entry_youtube.insert(0, str(app_limits["YouTube"]))
entry_game = tk.Entry(settings_frame, font=("Arial", 12))
entry_game.insert(0, str(app_limits["Game"]))

label_yt = tk.Label(settings_frame, text="YouTube:")
label_game = tk.Label(settings_frame, text="Game:")

label_yt.pack()
entry_youtube.pack()
label_game.pack()
entry_game.pack()

save_button = tk.Button(settings_frame, text="Save", font=("Arial", 12), command=save_settings)
save_button.pack(pady=10)

# ===== 启动 GUI =====
root.mainloop()

# ===== Start GUI =====
root.mainloop()

# readline() example
print("\n=== Example: readline() ===")
try:
    with open("usage_log.txt", "r") as f:
        line = f.readline()
        print("The first line is:", line.strip())
except FileNotFoundError:
    print("⚠ File 'usage_log.txt' not found. Please run the app first.")

# readlines() example
print("\n=== Example: readlines() ===")
try:
    with open("usage_log.txt", "r") as f:
        lines = f.readlines()
        for idx, l in enumerate(lines):
            print(f"Line {idx + 1}: {l.strip()}")
except FileNotFoundError:
    print("⚠ File 'usage_log.txt' not found. Please run the app first.")
