import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Scientific Calculator")
        self.entry_var = tk.StringVar()
        self.history_var = tk.StringVar()
        self.history = []
        self.memory = 0
        self.history_visible = False  
        self.create_widgets()

    def create_widgets(self):
        entry = tk.Entry(self.root, textvariable=self.entry_var, font=("Arial", 20),
                         bd=10, relief=tk.SUNKEN, justify="right")
        entry.grid(row=0, column=0, columnspan=5)

        self.history_frame = tk.Frame(self.root)

        self.history_label = tk.Label(self.history_frame, textvariable=self.history_var,
                                      font=("Arial", 12), wraplength=200, justify="left")
        self.history_label.pack()

        tk.Button(self.history_frame, text="Clear History", font=("Arial", 12),
                  command=self.clear_history, bg="gray").pack(pady=5)

        grid_buttons = [
            ["7", "8", "9", "/", "("],
            ["4", "5", "6", "*", ")"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["sin", "cos", "tan", "sqrt"],
            ["log", "π", "^", "Rad"],
            ["M+", "M-", "MR", "MC"]
        ]

        button_colors = {
            "sin": "khaki", "cos": "khaki", "tan": "khaki",
            "log": "khaki", "sqrt": "burlywood", "Rad": "burlywood",
            "=": "coral", "+": "powder blue", "-": "powder blue",
            "*": "powder blue", "/": "powder blue",
            "^": "khaki", "π": "khaki",
            "M+": "royalblue", "M-": "royalblue",
            "MR": "royalblue", "MC": "royalblue"
        }

        for i, row in enumerate(grid_buttons):
            for j, button in enumerate(row):
                color = button_colors.get(button, 'lavender')
                tk.Button(self.root, text=button, font=("Arial", 15),
                          command=lambda b=button: self.on_click(b),
                          width=5, height=2, bg=color)\
                    .grid(row=i+1, column=j, padx=2, pady=2)

        tk.Button(self.root, text="AC", font=("Arial", 15),
                  command=lambda: self.on_click("C"),
                  width=5, height=2, bg="lightsteelblue")\
            .grid(row=8, column=0, columnspan=1, padx=2, pady=2)

        tk.Button(self.root, text="DEL", font=("Arial", 15),
                  command=lambda: self.on_click("DEL"),
                  width=5, height=2, bg="lightsteelblue")\
            .grid(row=8, column=1, columnspan=1, padx=2, pady=2)

        tk.Button(self.root, text="History", font=("Arial", 15),
                  command=self.toggle_history,
                  width=12, height=2, bg="lightgray")\
            .grid(row=8, column=2, columnspan=2, padx=2, pady=2)

    def toggle_history(self):
        if self.history_visible:
            self.history_frame.grid_forget()
            self.history_visible = False
        else:
            self.history_frame.grid(row=0, column=5, rowspan=10, sticky="nsew")
            self.history_visible = True

    def on_click(self, button_text):
        if button_text == "C":
            self.entry_var.set("")

        elif button_text == "=":
            try:
                expression = self.entry_var.get().replace("^", "**").replace("π", str(math.pi))
                result = eval(expression)
                self.history.append(self.entry_var.get() + " = " + str(result))
                self.history_var.set("\n".join(self.history[-10:]))
                self.entry_var.set(result)
            except:
                messagebox.showerror("Error", "Invalid Expression")

        elif button_text in ["sin", "cos", "tan", "log", "sqrt", "Rad"]:
            try:
                expr = self.entry_var.get()
                num = float(expr)

                if button_text == "sin":
                    result = math.sin(math.radians(num))
                elif button_text == "cos":
                    result = math.cos(math.radians(num))
                elif button_text == "tan":
                    result = math.tan(math.radians(num))
                elif button_text == "log":
                    result = math.log10(num)
                elif button_text == "sqrt":
                    result = math.sqrt(num)
                elif button_text == "Rad":
                    result = math.radians(num)

                self.history.append(expr + " " + button_text + " = " + str(result))
                self.history_var.set("\n".join(self.history[-10:]))
                self.entry_var.set(result)

            except:
                messagebox.showerror("Error", "Invalid Input")

        elif button_text == "DEL":
            self.entry_var.set(self.entry_var.get()[:-1])

        elif button_text == "M+":
            try:
                self.memory += float(self.entry_var.get())
                messagebox.showinfo("Memory", f"Memory + {self.memory}")
            except:
                messagebox.showerror("Error", "Invalid Input for M+")

        elif button_text == "M-":
            try:
                self.memory -= float(self.entry_var.get())
                messagebox.showinfo("Memory", f"Memory - {self.memory}")
            except:
                messagebox.showerror("Error", "Invalid Input for M-")

        elif button_text == "MR":
            self.entry_var.set(self.memory)

        elif button_text == "MC":
            self.memory = 0
            messagebox.showinfo("Memory", "Memory Cleared")

        else:
            current_text = self.entry_var.get()
            self.entry_var.set(current_text + button_text)

    def clear_history(self):
        self.history.clear()
        self.history_var.set("")
        messagebox.showinfo("History", "History Cleared")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
