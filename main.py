import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dichotomy(a, b, eps, delta, func):
    while abs(b - a) >= eps:
        x1 = (a + b - delta) / 2
        x2 = (a + b + delta) / 2
        f1, f2 = func(x1), func(x2)
        if f1 < f2:
            b = x2
        elif f1 > f2:
            a = x1
        else:
            a, b = x1, x2
    x_opt = (a + b) / 2
    return x_opt, func(x_opt)

def fibonacci(a, b, n, eps, func):
    F = [1, 1]
    for i in range(2, n + 1):
        F.append(F[-1] + F[-2])
    x2 = a + (F[n - 1] / F[n]) * (b - a) + ((-1) ** n * eps) / F[n]
    x4 = a + b - x2
    f2, f4 = func(x2), func(x4)
    for _ in range(n):
        if x4 < x2:
            if f4 < f2:
                b = x2
                x2 = x4
                f2 = f4
                x4 = a + b - x2
                f4 = func(x4)
            else:
                a = x4
                x4 = x2
                f4 = f2
                x2 = a + b - x4
                f2 = func(x2)
        else:
            if f4 < f2:
                a = x2
                x2 = x4
                f2 = f4
                x4 = a + b - x2
                f4 = func(x4)
            else:
                b = x4
                x4 = x2
                f4 = f2
                x2 = a + b - x4
                f2 = func(x2)
    x_opt = (a + b) / 2
    return x_opt, func(x_opt)

def f7(x): return x ** 2 * math.sin(0.5 * x)
def f8(x): return math.log(x) + 3 * math.cos(x)
def f9(x): return -math.sqrt(x) * math.sin(x ** 2 / 100)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа 9")
        self.root.geometry("800x800")

        self.method = tk.StringVar(value="dichotomy")
        self.func_idx = tk.IntVar(value=7)
        self.result = None

        self.method.trace_add("write", self.reset_result)
        self.func_idx.trace_add("write", self.reset_result)

        self.row1_frame = tk.Frame(self.root, pady=10)
        self.row1_frame.pack(fill=tk.X)

        m_method = ttk.OptionMenu(self.row1_frame, self.method, "dichotomy", "dichotomy", "fibonacci")
        m_method.pack(side=tk.LEFT, padx=5)

        m_func = ttk.OptionMenu(self.row1_frame, self.func_idx, 7, 7, 8, 9)
        m_func.pack(side=tk.LEFT, padx=5)

        tk.Button(self.row1_frame, text="Вычислить", command=self.calculate).pack(side=tk.LEFT, padx=5)
        tk.Button(self.row1_frame, text="Загрузить из файла", command=self.loadfile).pack(side=tk.LEFT, padx=5)
        tk.Button(self.row1_frame, text="Сохранить в файл", command=self.savefile).pack(side=tk.LEFT, padx=5)
        tk.Button(self.row1_frame, text="График", command=self.plot_graph).pack(side=tk.LEFT, padx=5)
        tk.Button(self.row1_frame, text="Справка", command=self.show_help).pack(side=tk.LEFT, padx=5)
        tk.Button(self.row1_frame, text="О программе", command=self.show_about).pack(side=tk.LEFT, padx=5)

        row2_frame = tk.Frame(self.root, pady=5)
        row2_frame.pack(fill=tk.X, padx=10)

        tk.Label(row2_frame, text="a:").pack(side=tk.LEFT)
        self.entry_a = tk.Entry(row2_frame, width=6)
        self.entry_a.insert(0, "2")
        self.entry_a.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(row2_frame, text="b:").pack(side=tk.LEFT)
        self.entry_b = tk.Entry(row2_frame, width=6)
        self.entry_b.insert(0, "10")
        self.entry_b.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(row2_frame, text="eps:").pack(side=tk.LEFT)
        self.entry_eps = tk.Entry(row2_frame, width=8)
        self.entry_eps.insert(0, "0.001")
        self.entry_eps.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(row2_frame, text="delta:").pack(side=tk.LEFT)
        self.entry_delta = tk.Entry(row2_frame, width=8)
        self.entry_delta.insert(0, "0.0001")
        self.entry_delta.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(row2_frame, text="n:").pack(side=tk.LEFT)
        self.entry_n = tk.Entry(row2_frame, width=5)
        self.entry_n.insert(0, "10")
        self.entry_n.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(row2_frame, text="Очистить", command=self.cleardata).pack(side=tk.LEFT, padx=5)

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def reset_result(self, *args):
        self.result = None

    def cleardata(self):
        for e in [self.entry_a, self.entry_b, self.entry_eps, self.entry_delta, self.entry_n]:
            e.delete(0, tk.END)

    def loadfile(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.read().split()

                if len(lines) < 5:
                    messagebox.showerror("Ошибка", "Недостаточно данных в файле. Ожидается 5 значений.")
                    return

                entries = [self.entry_a, self.entry_b, self.entry_eps, self.entry_delta, self.entry_n]
                for entry, val in zip(entries, lines[:5]):
                    entry.delete(0, tk.END)
                    entry.insert(0, val)

                self.reset_result()
                messagebox.showinfo("Загрузка", "Данные успешно загружены из файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

    def calculate(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            eps = float(self.entry_eps.get())

            if self.func_idx.get() == 7:
                func = f7
            elif self.func_idx.get() == 8:
                func = f8
            else:
                func = f9

            if self.method.get() == "dichotomy":
                delta = float(self.entry_delta.get())
                x_opt, f_opt = dichotomy(a, b, eps, delta, func)
            else:
                n = int(self.entry_n.get())
                x_opt, f_opt = fibonacci(a, b, n, eps, func)

            self.result = (x_opt, f_opt)
            messagebox.showinfo("Результат", f"x*: {x_opt:.5f}\nf(x*): {f_opt:.5f}")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат данных")

    def savefile(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            eps = float(self.entry_eps.get())

            if self.func_idx.get() == 7:
                func = f7
            elif self.func_idx.get() == 8:
                func = f8
            else:
                func = f9

            if self.method.get() == "dichotomy":
                delta = float(self.entry_delta.get())
                x_opt, f_opt = dichotomy(a, b, eps, delta, func)
            else:
                n = int(self.entry_n.get())
                x_opt, f_opt = fibonacci(a, b, n, eps, func)

            self.result = (x_opt, f_opt)

            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"x*: {x_opt:.5f}\nf(x*): {f_opt:.5f}")
                messagebox.showinfo("Сохранение .txt", "Результат сохранен в файл")

        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат данных")

    def plot_graph(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите числовые значения a и b")
            return

        x = np.linspace(a, b, 1000)

        if self.func_idx.get() == 7:
            y = [f7(xi) for xi in x]
        elif self.func_idx.get() == 8:
            y = [f8(xi) for xi in x]
        else:
            y = [f9(xi) for xi in x]

        self.ax.clear()
        self.ax.plot(x, y, label=f'f{self.func_idx.get()}(x)')

        if self.result:
            self.ax.scatter([self.result[0]], [self.result[1]], color='red', zorder=5, label='Оптимум')

        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def show_help(self):
        if self.method.get() == "dichotomy":
            text = "Метод дихотомии:\nСужает интервал неопределенности путем деления его пополам и проверки двух точек, отстоящих от середины на delta"
        else:
            text = "Метод фибоначчи:\nИспользует числа Фибоначчи для симметричного расположения точек на интервале неопределенности"
        messagebox.showinfo("Справка", text)

    def show_about(self):
        messagebox.showinfo("О программе", "Лабораторная работа 9\nВариант 8\nРазработчик: Сухочев А. В.")

root = tk.Tk()
app = App(root)
root.mainloop()