import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab, ImageTk
import time
import os

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 截图工具")
        
        # 设置窗口大小和位置
        self.root.geometry("400x300+500+200")
        
        # 创建UI元素
        self.create_widgets()
        
        # 截图相关变量
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selection_window = None
        
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="截图工具", font=("Arial", 16))
        title_label.pack(pady=10)
        
        # 功能按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        fullscreen_btn = tk.Button(btn_frame, text="全屏截图", command=self.fullscreen_screenshot)
        fullscreen_btn.pack(side=tk.LEFT, padx=10)
        
        region_btn = tk.Button(btn_frame, text="区域截图", command=self.start_region_screenshot)
        region_btn.pack(side=tk.LEFT, padx=10)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack(pady=10)
        
        # 作者信息
        author_label = tk.Label(self.root, text="Python 截图工具 v1.0", fg="gray")
        author_label.pack(side=tk.BOTTOM, pady=10)
    
    def fullscreen_screenshot(self):
        """全屏截图"""
        try:
            # 隐藏主窗口
            self.root.withdraw()
            time.sleep(0.3)  # 等待窗口隐藏
            
            # 截图
            screenshot = ImageGrab.grab()
            
            # 显示主窗口
            self.root.deiconify()
            
            # 保存截图
            self.save_screenshot(screenshot)
            
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("错误", f"截图失败: {str(e)}")
    
    def start_region_screenshot(self):
        """开始区域截图"""
        self.root.withdraw()
        time.sleep(0.3)
        
        # 创建全屏透明窗口用于选择区域
        self.selection_window = tk.Toplevel()
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-alpha", 0.3)
        self.selection_window.attributes("-topmost", True)
        
        # 绑定鼠标事件
        self.selection_window.bind("<ButtonPress-1>", self.on_press)
        self.selection_window.bind("<B1-Motion>", self.on_drag)
        self.selection_window.bind("<ButtonRelease-1>", self.on_release)
        
        # 画布用于绘制选择区域
        self.canvas = tk.Canvas(self.selection_window, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def on_press(self, event):
        """鼠标按下事件"""
        self.start_x = event.x
        self.start_y = event.y
        
        # 如果已有矩形，先删除
        if self.rect:
            self.canvas.delete(self.rect)
        
        # 创建新矩形
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=2, fill="white"
        )
    
    def on_drag(self, event):
        """鼠标拖动事件"""
        if self.rect:
            # 更新矩形大小
            self.canvas.coords(
                self.rect, self.start_x, self.start_y, event.x, event.y
            )
    
    def on_release(self, event):
        """鼠标释放事件"""
        end_x, end_y = event.x, event.y
        
        # 确保结束坐标大于开始坐标
        x1, x2 = sorted([self.start_x, end_x])
        y1, y2 = sorted([self.start_y, end_y])
        
        # 关闭选择窗口
        self.selection_window.destroy()
        self.selection_window = None
        
        # 截图选定区域
        try:
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            self.root.deiconify()
            self.save_screenshot(screenshot)
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("错误", f"截图失败: {str(e)}")
    
    def save_screenshot(self, image):
        """保存截图"""
        # 获取保存路径
        default_filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 图片", "*.png"), ("JPEG 图片", "*.jpg"), ("所有文件", "*.*")],
            initialfile=default_filename
        )
        
        if filepath:
            try:
                image.save(filepath)
                self.status_label.config(text=f"截图已保存到: {filepath}")
                
                # 询问是否打开截图
                if messagebox.askyesno("成功", "截图保存成功！是否要打开文件？"):
                    os.startfile(filepath)
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()