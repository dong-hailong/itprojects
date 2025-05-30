"""
简易画图工具
功能：
1. 支持画笔、直线、矩形、椭圆四种绘图工具
2. 可自定义绘图颜色和线条粗细
3. 支持清空画布
4. 实时预览绘图效果

使用说明：
1. 点击工具栏按钮选择绘图工具
2. 在画布上点击并拖动鼠标进行绘制
3. 使用"颜色"按钮更改绘图颜色
4. 使用滑块调整线条粗细
5. 点击"清除"按钮清空画布
"""

import tkinter as tk
from tkinter import colorchooser


class SimpleDrawingApp:
    def __init__(self, root):
        """
        初始化画图应用程序

        参数:
            root: Tkinter根窗口对象
        """
        # 主窗口设置
        self.root = root
        self.root.title("简易画图工具")  # 设置窗口标题
        self.root.geometry("900x700")  # 设置窗口大小

        # 绘图状态变量
        self.current_tool = "pen"  # 当前工具：pen(画笔)/line(直线)/rectangle(矩形)/oval(椭圆)
        self.current_color = "black"  # 当前绘图颜色
        self.line_width = 2  # 当前线条宽度
        self.start_x = None  # 绘图起始点x坐标
        self.start_y = None  # 绘图起始点y坐标
        self.prev_x = None  # 画笔工具前一个点的x坐标
        self.prev_y = None  # 画笔工具前一个点的y坐标
        self.temp_item = None  # 临时图形对象(用于预览)

        # 创建界面组件
        self.create_widgets()

        # 绑定鼠标事件
        self.bind_events()

    def create_widgets(self):
        """创建所有界面组件"""

        # 主画布 - 用于绘图
        self.canvas = tk.Canvas(
            self.root,
            bg="white",  # 白色背景
            width=800,
            height=600,
            relief=tk.SUNKEN,  # 凹陷边框效果
            bd=2  # 边框宽度
        )
        self.canvas.pack(
            side=tk.TOP,  # 放置在顶部
            fill=tk.BOTH,  # 填充可用空间
            expand=True,  # 可扩展
            padx=5,  # 水平边距
            pady=5  # 垂直边距
        )

        # 工具栏框架
        self.toolbar = tk.Frame(
            self.root,
            relief=tk.RAISED,  # 凸起边框效果
            bd=2  # 边框宽度
        )
        self.toolbar.pack(
            side=tk.BOTTOM,  # 放置在底部
            fill=tk.X,  # 水平填充
            padx=5,  # 水平边距
            pady=5  # 垂直边距
        )

        # 创建工具按钮
        tools = [
            ("画笔", "pen"),
            ("直线", "line"),
            ("矩形", "rectangle"),
            ("椭圆", "oval"),
        ]

        # 工具按钮组
        for text, tool in tools:
            btn = tk.Button(
                self.toolbar,
                text=text,
                width=8,
                command=lambda t=tool: self.select_tool(t)
            )
            btn.pack(
                side=tk.LEFT,  # 从左到右排列
                padx=2,  # 水平间距
                pady=2  # 垂直间距
            )

        # 颜色选择按钮
        self.color_btn = tk.Button(
            self.toolbar,
            text="颜色",
            width=8,
            command=self.choose_color
        )
        self.color_btn.pack(
            side=tk.LEFT,
            padx=2,
            pady=2
        )

        # 清空按钮
        self.clear_btn = tk.Button(
            self.toolbar,
            text="清除",
            width=8,
            command=self.clear_canvas
        )
        self.clear_btn.pack(
            side=tk.LEFT,
            padx=2,
            pady=2
        )

        # 画笔大小调节组件
        self.size_frame = tk.Frame(self.toolbar)
        self.size_frame.pack(
            side=tk.LEFT,
            padx=10
        )

        # 大小标签
        tk.Label(
            self.size_frame,
            text="画笔大小:"
        ).pack(side=tk.LEFT)

        # 大小滑块
        self.size_slider = tk.Scale(
            self.size_frame,
            from_=1,  # 最小值
            to=20,  # 最大值
            orient=tk.HORIZONTAL,  # 水平方向
            command=self.change_line_width  # 值改变回调
        )
        self.size_slider.set(self.line_width)  # 设置默认值
        self.size_slider.pack(side=tk.LEFT)

        # 状态栏 - 显示当前工具和颜色
        self.status_bar = tk.Label(
            self.root,
            text=f"当前工具: 画笔 | 颜色: {self.current_color} | 大小: {self.line_width}",
            bd=1,  # 边框宽度
            relief=tk.SUNKEN,  # 凹陷效果
            anchor=tk.W  # 左对齐
        )
        self.status_bar.pack(
            side=tk.BOTTOM,
            fill=tk.X  # 水平填充
        )

    def bind_events(self):
        """绑定鼠标事件处理函数"""
        # 鼠标左键按下 - 开始绘图
        self.canvas.bind("<Button-1>", self.start_drawing)
        # 鼠标左键按下并移动 - 绘图过程
        self.canvas.bind("<B1-Motion>", self.draw)
        # 鼠标左键释放 - 结束绘图
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def select_tool(self, tool):
        """
        选择绘图工具

        参数:
            tool: 工具名称(pen/line/rectangle/oval)
        """
        self.current_tool = tool

        # 更新状态栏显示
        tool_names = {
            "pen": "画笔",
            "line": "直线",
            "rectangle": "矩形",
            "oval": "椭圆"
        }
        self.status_bar.config(
            text=f"当前工具: {tool_names[tool]} | 颜色: {self.current_color} | 大小: {self.line_width}"
        )

    def choose_color(self):
        """打开颜色选择对话框并设置绘图颜色"""
        # 弹出颜色选择对话框
        color = colorchooser.askcolor(
            title="选择颜色",
            initialcolor=self.current_color  # 默认选中当前颜色
        )

        # 如果用户选择了颜色(没有点击取消)
        if color[1]:
            self.current_color = color[1]  # 设置新颜色

            # 更新状态栏
            self.status_bar.config(
                text=f"当前工具: {self.get_tool_name()} | 颜色: {self.current_color} | 大小: {self.line_width}"
            )

    def get_tool_name(self):
        """获取当前工具的中文名称"""
        tool_names = {
            "pen": "画笔",
            "line": "直线",
            "rectangle": "矩形",
            "oval": "椭圆"
        }
        return tool_names.get(self.current_tool, "未知工具")

    def change_line_width(self, value):
        """
        改变线条宽度

        参数:
            value: 新的线条宽度值(来自滑块)
        """
        self.line_width = int(value)  # 转换为整数

        # 更新状态栏
        self.status_bar.config(
            text=f"当前工具: {self.get_tool_name()} | 颜色: {self.current_color} | 大小: {self.line_width}"
        )

    def clear_canvas(self):
        """清空画布"""
        self.canvas.delete("all")  # 删除所有图形

    def start_drawing(self, event):
        """
        开始绘图(鼠标左键按下时调用)

        参数:
            event: 鼠标事件对象，包含坐标等信息
        """
        self.start_x = event.x  # 记录起始x坐标
        self.start_y = event.y  # 记录起始y坐标

        # 如果是画笔工具，记录前一个点的位置
        if self.current_tool == "pen":
            self.prev_x = event.x
            self.prev_y = event.y

    def draw(self, event):
        """
        绘图过程(鼠标左键按下并移动时调用)

        参数:
            event: 鼠标事件对象，包含坐标等信息
        """
        if self.current_tool == "pen":
            # 画笔工具 - 绘制连续线条
            if self.prev_x and self.prev_y:
                self.canvas.create_line(
                    self.prev_x, self.prev_y,  # 起点
                    event.x, event.y,  # 终点
                    fill=self.current_color,  # 颜色
                    width=self.line_width,  # 宽度
                    capstyle=tk.ROUND,  # 线条端点样式
                    joinstyle=tk.ROUND  # 线条连接样式
                )
            # 更新前一点坐标
            self.prev_x = event.x
            self.prev_y = event.y
        else:
            # 其他工具(直线/矩形/椭圆) - 显示预览效果
            self.draw_preview(event)

    def draw_preview(self, event):
        """
        绘制预览图形(用于直线/矩形/椭圆工具)

        参数:
            event: 鼠标事件对象
        """
        # 删除之前的临时图形
        if self.temp_item:
            self.canvas.delete(self.temp_item)

        # 根据当前工具创建新的预览图形
        if self.current_tool == "line":
            self.temp_item = self.canvas.create_line(
                self.start_x, self.start_y,
                event.x, event.y,
                fill=self.current_color,
                width=self.line_width,
                dash=(4, 2)  # 虚线样式(预览效果)
            )
        elif self.current_tool == "rectangle":
            self.temp_item = self.canvas.create_rectangle(
                self.start_x, self.start_y,
                event.x, event.y,
                outline=self.current_color,
                width=self.line_width,
                dash=(4, 2)  # 虚线样式
            )
        elif self.current_tool == "oval":
            self.temp_item = self.canvas.create_oval(
                self.start_x, self.start_y,
                event.x, event.y,
                outline=self.current_color,
                width=self.line_width,
                dash=(4, 2)  # 虚线样式
            )

    def stop_drawing(self, event):
        """
        结束绘图(鼠标左键释放时调用)

        参数:
            event: 鼠标事件对象
        """
        if self.current_tool == "pen":
            # 画笔工具 - 重置前一点坐标
            self.prev_x = None
            self.prev_y = None
        elif self.temp_item:
            # 其他工具 - 删除预览图形并创建最终图形
            self.canvas.delete(self.temp_item)
            self.create_final_shape(event)

        # 重置起始点
        self.start_x = None
        self.start_y = None

    def create_final_shape(self, event):
        """
        创建最终图形(鼠标释放时)

        参数:
            event: 鼠标事件对象
        """
        if self.current_tool == "line":
            self.canvas.create_line(
                self.start_x, self.start_y,
                event.x, event.y,
                fill=self.current_color,
                width=self.line_width
            )
        elif self.current_tool == "rectangle":
            self.canvas.create_rectangle(
                self.start_x, self.start_y,
                event.x, event.y,
                outline=self.current_color,
                width=self.line_width
            )
        elif self.current_tool == "oval":
            self.canvas.create_oval(
                self.start_x, self.start_y,
                event.x, event.y,
                outline=self.current_color,
                width=self.line_width
            )


# 程序入口
if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口
    app = SimpleDrawingApp(root)  # 创建应用程序实例
    root.mainloop()  # 进入主事件循环