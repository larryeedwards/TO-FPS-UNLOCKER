import struct
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Offsets for dtMinWait in each build (big-endian floats)
XEX_DT_MIN_WAIT_OFFSET  = 0x35868   # Xbox 360 default.xex
DOL_DT_MIN_WAIT_OFFSET  = 0x3DE120  # Wii main.dol
ELF_DT_MIN_WAIT_OFFSET  = 0x57CE58  # PS3 EBOOT.elf

def fps_to_dtmin(fps):
    """Convert FPS target to dtMinWait value."""
    if fps <= 0:
        return 0.0
    return (1.0 / float(fps)) - 0.001

def detect_format(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".xex":
        return "xex"
    if ext == ".dol":
        return "dol"
    if ext == ".elf":
        return "elf"

    # Fallback: sniff magic
    with open(path, "rb") as f:
        magic = f.read(4)
    if magic == b"XEX2":
        return "xex"
    if magic == b"\x7FELF":
        return "elf"
    # Default to DOL if unknown but user selected a game file
    return "dol"

def patch_file(path, fps):
    game_type = detect_format(path)

    if game_type == "xex":
        offset = XEX_DT_MIN_WAIT_OFFSET
    elif game_type == "dol":
        offset = DOL_DT_MIN_WAIT_OFFSET
    elif game_type == "elf":
        offset = ELF_DT_MIN_WAIT_OFFSET
    else:
        raise RuntimeError("Unknown game format.")

    dt = fps_to_dtmin(fps)
    float_bytes = struct.pack(">f", dt)  # PPC/Cell/Wii/360 all big-endian

    with open(path, "rb") as f:
        data = bytearray(f.read())

    if offset + 4 > len(data):
        raise RuntimeError("File too small for expected offset.")

    data[offset:offset+4] = float_bytes

    base, ext = os.path.splitext(path)
    tag = "uncap" if fps <= 0 else f"{fps}fps"
    out_path = f"{base}_{tag}{ext}"

    with open(out_path, "wb") as f:
        f.write(data)

    return out_path, game_type, dt

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Tornado Outbreak – Multi-Platform FPS Patcher")
root.geometry("470x270")
root.resizable(False, False)

title = tk.Label(root,
    text="Tornado Outbreak – FPS Patcher (360 / Wii / PS3)",
    font=("Segoe UI", 13, "bold"))
title.pack(pady=10)

# File chooser
frame_file = tk.Frame(root)
frame_file.pack(pady=3)

tk.Label(frame_file, text="Game file (.xex / .dol / .elf): ").pack(side=tk.LEFT)
path_var = tk.StringVar()
tk.Entry(frame_file, textvariable=path_var, width=35).pack(side=tk.LEFT)

def browse():
    p = filedialog.askopenfilename(
        title="Select default.xex / main.dol / EBOOT.elf",
        filetypes=[
            ("Game binaries", "*.xex *.dol *.elf"),
            ("All files", "*.*")
        ],
    )
    if p:
        path_var.set(p)

tk.Button(frame_file, text="Browse", command=browse).pack(side=tk.LEFT, padx=4)

# FPS selector
frame_fps = tk.Frame(root)
frame_fps.pack(pady=15)

tk.Label(frame_fps, text="Framerate target: ").pack(side=tk.LEFT)

fps_var = tk.StringVar(value="60")
fps_menu = tk.OptionMenu(
    frame_fps,
    fps_var,
    "30", "45", "60", "90", "120", "144", "240", "Uncapped"
)
fps_menu.pack(side=tk.LEFT)

# dtMinWait preview
dt_label_var = tk.StringVar(value="dtMinWait = ? s")
dt_label = tk.Label(root, textvariable=dt_label_var)
dt_label.pack()

def update_dt_preview(*args):
    v = fps_var.get().strip()
    if v.lower() == "uncapped":
        dt = 0.0
    else:
        try:
            fps = float(v)
        except ValueError:
            dt_label_var.set("dtMinWait = ? s")
            return
        dt = fps_to_dtmin(fps)
    dt_label_var.set(f"dtMinWait = {dt:.6f} seconds")

fps_var.trace_add("write", update_dt_preview)
update_dt_preview()

def apply():
    path = path_var.get().strip()
    if not path:
        messagebox.showerror("Error", "Choose a .xex / .dol / .elf first.")
        return

    v = fps_var.get().strip()
    if v.lower() == "uncapped":
        fps = -1
    else:
        try:
            fps = int(v)
        except ValueError:
            messagebox.showerror("Error", "Invalid FPS value.")
            return

    try:
        out_path, game_type, dt = patch_file(path, fps)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    fps_text = "Uncapped" if fps <= 0 else f"{fps} FPS"
    messagebox.showinfo(
        "Patched",
        f"Detected: {game_type.upper()}\n"
        f"Target: {fps_text}\n"
        f"dtMinWait set to {dt:.6f} s\n\n"
        f"Saved as:\n{out_path}"
    )

btn = tk.Button(root, text="Patch File",
                font=("Segoe UI", 11, "bold"),
                width=20, height=2,
                command=apply)
btn.pack(pady=12)

root.mainloop()
