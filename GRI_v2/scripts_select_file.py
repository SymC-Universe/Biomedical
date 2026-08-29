import sys
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
title = sys.argv[1] if len(sys.argv) > 1 else 'Select file'
path = filedialog.askopenfilename(title=title)
root.destroy()
if path:
    print(path)
