import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class LineEquationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora y Graficadora de Líneas Rectas - Precálculo")
        self.root.geometry("1100x700")

        # Estilo de interfaz
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Marco Principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Panel Izquierdo: Controles y Entradas
        control_frame = ttk.LabelFrame(main_frame, text=" Datos de Entrada ", padding="15")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

        # Selección de Modo de Entrada
        ttk.Label(control_frame, text="Seleccione el modo de entrada:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        self.mode_var = tk.StringVar(value="2_points")
        
        modes = [
            ("Dos puntos: (x1, y1) y (x2, y2)", "2_points"),
            ("Punto y Pendiente: (x1, y1) y m", "point_slope"),
            ("Pendiente e Intercepto: m y b", "slope_intercept")
        ]
        
        for text, mode in modes:
            ttk.Radiobutton(control_frame, text=text, value=mode, variable=self.mode_var, command=self.update_inputs).pack(anchor=tk.W, pady=2)

        # Contenedor dinámico de entradas
        self.inputs_frame = ttk.Frame(control_frame, padding="10")
        self.inputs_frame.pack(fill=tk.X, pady=10)

        # Botón para Procesar
        btn_calc = ttk.Button(control_frame, text="Calcular y Graficar", command=self.calculate_and_plot)
        btn_calc.pack(fill=tk.X, pady=10)

        # Área de Resultados
        self.results_frame = ttk.LabelFrame(control_frame, text=" Resultados ", padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.lbl_slope = ttk.Label(self.results_frame, text="Pendiente (m): -", font=("Arial", 10))
        self.lbl_slope.pack(anchor=tk.W, pady=2)
        
        self.lbl_eq_explicit = ttk.Label(self.results_frame, text="Forma Explícita: -", font=("Arial", 10, "bold"))
        self.lbl_eq_explicit.pack(anchor=tk.W, pady=2)
        
        self.lbl_eq_general = ttk.Label(self.results_frame, text="Forma General: -", font=("Arial", 10))
        self.lbl_eq_general.pack(anchor=tk.W, pady=2)

        self.lbl_intercepts = ttk.Label(self.results_frame, text="Interceptos: -", font=("Arial", 10))
        self.lbl_intercepts.pack(anchor=tk.W, pady=2)

        # Panel Derecho: Gráfica Matplotlib
        graph_frame = ttk.LabelFrame(main_frame, text=" Plano Cartesiano ", padding="10")
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.entries = {}
        self.update_inputs()
        self.init_graph()

    def update_inputs(self):
        """Actualiza los campos según el modo seleccionado."""
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        
        self.entries.clear()
        mode = self.mode_var.get()

        if mode == "2_points":
            self.create_entry("x1:", "x1")
            self.create_entry("y1:", "y1")
            self.create_entry("x2:", "x2")
            self.create_entry("y2:", "y2")
        elif mode == "point_slope":
            self.create_entry("x1:", "x1")
            self.create_entry("y1:", "y1")
            self.create_entry("Pendiente (m):", "m")
        elif mode == "slope_intercept":
            self.create_entry("Pendiente (m):", "m")
            self.create_entry("Intercepto Y (b):", "b")

    def create_entry(self, label_text, key):
        frame = ttk.Frame(self.inputs_frame)
        frame.pack(fill=tk.X, pady=2)
        ttk.Label(frame, text=label_text, width=15).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        self.entries[key] = entry

    def init_graph(self):
        """Inicializa los ejes del plano cartesiano."""
        self.ax.clear()
        self.ax.axhline(0, color='black', linewidth=1.2)
        self.ax.axvline(0, color='black', linewidth=1.2)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlabel("Eje X")
        self.ax.set_ylabel("Eje Y")
        self.canvas.draw()

    def calculate_and_plot(self):
        try:
            mode = self.mode_var.get()
            
            # Obtención de parámetros según el modo
            if mode == "2_points":
                x1 = float(self.entries["x1"].get())
                y1 = float(self.entries["y1"].get())
                x2 = float(self.entries["x2"].get())
                y2 = float(self.entries["y2"].get())

                if x1 == x2 and y1 == y2:
                    messagebox.showerror("Error", "Los dos puntos no pueden ser idénticos.")
                    return
                
                is_vertical = (x1 == x2)
                if is_vertical:
                    m = None
                    b = None
                    c = x1
                else:
                    m = (y2 - y1) / (x2 - x1)
                    b = y1 - m * x1

            elif mode == "point_slope":
                x1 = float(self.entries["x1"].get())
                y1 = float(self.entries["y1"].get())
                m = float(self.entries["m"].get())
                b = y1 - m * x1
                is_vertical = False

            elif mode == "slope_intercept":
                m = float(self.entries["m"].get())
                b = float(self.entries["b"].get())
                x1, y1 = 0, b
                is_vertical = False

            # Lógica Matemática
            self.init_graph()

            if is_vertical:
                # Recta Vertical: x = c
                self.lbl_slope.config(text="Pendiente (m): Indefinida")
                self.lbl_eq_explicit.config(text=f"Forma Explícita: x = {c:.2f}")
                self.lbl_eq_general.config(text=f"Forma General: x - {c:.2f} = 0")
                self.lbl_intercepts.config(text=f"Intercepto X: ({c:.2f}, 0) | Y: No tiene")

                self.ax.axvline(x=c, color='red', linewidth=2, label=f'x = {c:.2f}')
                self.ax.plot(c, 0, 'ro')  # Intercepto X
                x_center = c
                y_center = 0
            else:
                # Recta Normal o Horizontal
                slope_str = "0" if abs(m) < 1e-9 else f"{m:.2f}"
                self.lbl_slope.config(text=f"Pendiente (m): {slope_str}")

                # Ecuación explícita y = mx + b
                sign_b = "+" if b >= 0 else "-"
                b_abs = abs(b)
                if abs(m) < 1e-9:
                    eq_exp = f"y = {b:.2f}"
                else:
                    eq_exp = f"y = {m:.2f}x {sign_b} {b_abs:.2f}"
                self.lbl_eq_explicit.config(text=f"Forma Explícita: {eq_exp}")

                # Ecuación general Ax + By + C = 0
                # m*x - y + b = 0
                A = m
                B = -1
                C = b
                sign_C = "+" if C >= 0 else "-"
                self.lbl_eq_general.config(text=f"Forma General: {A:.2f}x - 1.00y {sign_C} {abs(C):.2f} = 0")

                # Interceptos
                int_y = f"(0, {b:.2f})"
                if abs(m) > 1e-9:
                    x_int_val = -b / m
                    int_x = f"({x_int_val:.2f}, 0)"
                    self.ax.plot(x_int_val, 0, 'go', label=f'Intercepto X {int_x}')
                else:
                    int_x = "No tiene"
                
                self.lbl_intercepts.config(text=f"Intercepto X: {int_x} | Y: {int_y}")
                self.ax.plot(0, b, 'bo', label=f'Intercepto Y {int_y}')

                # Generar puntos para graficar
                x_center = x1 if mode != "slope_intercept" else 0
                y_center = y1 if mode != "slope_intercept" else b
                x_vals = np.linspace(x_center - 10, x_center + 10, 400)
                y_vals = m * x_vals + b
                self.ax.plot(x_vals, y_vals, color='red', linewidth=2, label=eq_exp)

            # Si se proporcionaron puntos específicos, marcarlos
            if mode == "2_points":
                self.ax.plot([x1, x2], [y1, y2], 'kx', markersize=8, markeredgewidth=2, label='Puntos Dados')

            # Ajustar límites dinámicamente
            self.ax.set_xlim(x_center - 10, x_center + 10)
            self.ax.set_ylim(y_center - 10, y_center + 10)
            self.ax.legend(loc='upper left')
            self.canvas.draw()

        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LineEquationApp(root)
    root.mainloop()