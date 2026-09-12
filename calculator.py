import ast
import math
import operator
import tkinter as tk
from tkinter import messagebox


class SafeCalculator:
    """Evaluate supported calculator expressions without using eval()."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    FUNCTIONS = {
        "sqrt": math.sqrt,
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
    }

    CONSTANTS = {"pi": math.pi, "e": math.e}

    def calculate(self, expression):
        expression = expression.strip()
        if not expression:
            raise ValueError("Enter an expression.")

        tree = ast.parse(expression, mode="eval")
        result = self._evaluate(tree.body)

        if not math.isfinite(result):
            raise ValueError("Result is not a finite number.")
        return result

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return node.value
            raise ValueError("Invalid value.")

        if isinstance(node, ast.BinOp) and type(node.op) in self.OPERATORS:
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            return self.OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in self.OPERATORS:
            return self.OPERATORS[type(node.op)](self._evaluate(node.operand))

        if isinstance(node, ast.Name) and node.id in self.CONSTANTS:
            return self.CONSTANTS[node.id]

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in self.FUNCTIONS:
                raise ValueError("Function not supported.")
            if len(node.args) != 1 or node.keywords:
                raise ValueError("Use one argument for a function.")
            return self.FUNCTIONS[node.func.id](self._evaluate(node.args[0]))

        raise ValueError("Invalid expression.")


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("390x650")
        self.root.minsize(350, 600)
        self.root.configure(bg="#111827")

        self.calculator = SafeCalculator()
        self.history = []
        self.expression = tk.StringVar()
        self.result = tk.StringVar(value="0")

        self._build_ui()
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear())
        self.root.bind("<BackSpace>", lambda event: self.backspace())

    def _build_ui(self):
        top = tk.Frame(self.root, bg="#111827")
        top.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            top, text="PYTHON CALCULATOR", font=("Arial", 14, "bold"),
            bg="#111827", fg="white"
        ).pack(anchor="w", pady=(0, 10))

        display = tk.Frame(top, bg="#1f2937")
        display.pack(fill="x", pady=(0, 12))

        tk.Label(
            display, textvariable=self.expression, anchor="e",
            font=("Arial", 16), bg="#1f2937", fg="#9ca3af",
            padx=12, pady=12
        ).pack(fill="x")

        tk.Label(
            display, textvariable=self.result, anchor="e",
            font=("Arial", 30, "bold"), bg="#1f2937", fg="white",
            padx=12, pady=12
        ).pack(fill="x")

        buttons = [
            ["C", "⌫", "(", ")"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["0", ".", "%", "+"],
            ["π", "e", "x²", "="],
        ]

        grid = tk.Frame(top, bg="#111827")
        grid.pack(fill="x")

        for r, row in enumerate(buttons):
            for c, text in enumerate(row):
                tk.Button(
                    grid, text=text, font=("Arial", 16, "bold"),
                    height=2, bd=0, relief="flat",
                    command=lambda value=text: self.press(value)
                ).grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            grid.rowconfigure(r, weight=1)

        for c in range(4):
            grid.columnconfigure(c, weight=1)

        tk.Label(
            top, text="Scientific functions", font=("Arial", 12, "bold"),
            bg="#111827", fg="white"
        ).pack(anchor="w", pady=(14, 6))

        scientific = [["sqrt", "sin", "cos", "tan"], ["log", "ln", "abs", "xʸ"]]
        sci = tk.Frame(top, bg="#111827")
        sci.pack(fill="x")

        for r, row in enumerate(scientific):
            for c, text in enumerate(row):
                tk.Button(
                    sci, text=text, font=("Arial", 12), height=2,
                    bd=0, relief="flat",
                    command=lambda value=text: self.press(value)
                ).grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            sci.rowconfigure(r, weight=1)

        for c in range(4):
            sci.columnconfigure(c, weight=1)

        history_bar = tk.Frame(top, bg="#111827")
        history_bar.pack(fill="x", pady=(14, 0))

        tk.Button(
            history_bar, text="View History", command=self.show_history,
            font=("Arial", 11), padx=10, pady=7
        ).pack(side="left")

        tk.Button(
            history_bar, text="Clear History", command=self.clear_history,
            font=("Arial", 11), padx=10, pady=7
        ).pack(side="right")

    def press(self, value):
        if value == "C":
            self.clear()
            return
        if value == "⌫":
            self.backspace()
            return
        if value == "=":
            self.calculate()
            return

        mapping = {"÷": "/", "×": "*", "−": "-", "π": "pi", "x²": "**2", "xʸ": "**"}

        if value in self.calculator.FUNCTIONS:
            self.expression.set(self.expression.get() + value + "(")
        else:
            self.expression.set(self.expression.get() + mapping.get(value, value))

    def clear(self):
        self.expression.set("")
        self.result.set("0")

    def backspace(self):
        self.expression.set(self.expression.get()[:-1])

    def calculate(self):
        expression = self.expression.get()
        try:
            answer = self.calculator.calculate(expression)
            formatted = self._format(answer)
            self.result.set(formatted)
            self.history.append(f"{expression} = {formatted}")
        except (ValueError, SyntaxError, ZeroDivisionError, OverflowError, TypeError, ArithmeticError) as error:
            self.result.set("Error")
            messagebox.showerror("Calculation Error", str(error))

    @staticmethod
    def _format(value):
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.12g}"

    def show_history(self):
        window = tk.Toplevel(self.root)
        window.title("Calculation History")
        window.geometry("420x400")
        window.configure(bg="#111827")

        tk.Label(
            window, text="History", font=("Arial", 16, "bold"),
            bg="#111827", fg="white"
        ).pack(pady=10)

        box = tk.Listbox(window, font=("Arial", 12), bg="#1f2937", fg="white")
        box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        if self.history:
            for item in reversed(self.history):
                box.insert(tk.END, item)
        else:
            box.insert(tk.END, "No calculations yet.")

    def clear_history(self):
        self.history.clear()


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()
