import tkinter as tk
from tkinter import ttk
import pandas as pd

# 创建Tkinter窗口
root = tk.Tk()
root.title("DataFrame in Listbox")

# 创建一个Frame用于容纳Listbox
frame = ttk.Frame(root)
frame.pack()

# 创建一个Listbox来显示DataFrame数据
listbox = tk.Listbox(frame)
listbox.pack()

# 创建一个DataFrame（示例数据）
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [25, 30, 35, 40],
}
df = pd.DataFrame(data)

# 获取DataFrame的数据并添加到Listbox中
for row in df.itertuples(index=False):
    listbox.insert(tk.END, row)

# 启动Tkinter主循环
root.mainloop()
