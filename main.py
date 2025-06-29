import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# --- FUNCIONES FÍSICAS ---

def thermal_velocity(Te, kB=1.38e-23, me=9.11e-31):
    return np.sqrt((3 * kB * Te) / me)

def generate_initial_velocities3(ve, num_particles):
    v03 = np.random.normal(ve , 1, num_particles)
    angulos = np.random.uniform(-np.pi, np.pi, num_particles)
    v0x3 = v03 * np.cos(angulos)
    v0y3 = v03 * np.sin(angulos)
    return np.array(v0x3), np.array(v0y3)

def collision_frequency(lambd, ve, n_i=1e19, Z=1 ,epsilon_0=8.85e-12 , q=1.6e-19, me=9.11e-31):
    return ((n_i * Z**2 * q**4 * lambd) / (4 * np.pi * ve**3 * me**2 * epsilon_0**2))

def metodo_tranfinversa_gaussiana(mu, sigma, N):
    z = np.sqrt(-2*np.log(np.random.rand(N))) * np.cos(2*np.pi*np.random.rand(N))
    return mu + sigma * z

def integrate_trajectory8(v0x3, v0y3, vei, q=1.6e-19, m=9.11e-31, B0=3.4, steps=100):
    dt = 1 / vei
    omega_c = q * B0 / m
    tau_c = 1 / vei

    x, y = np.zeros(steps), np.zeros(steps)
    vx, vy = v0x3, v0y3
    displacements_total = []

    for i in range(1, steps):
        if i % int(tau_c / dt) == 0:
            dtheta = metodo_tranfinversa_gaussiana(mu=0, sigma=0.1, N=1)[0]
            v_complex = (vx + 1j * vy) * np.exp(1j * dtheta)
            vx, vy = np.real(v_complex), np.imag(v_complex)
        
        x[i] = x[i-1] + (vx / omega_c)
        y[i] = y[i-1] + (vy / omega_c)
        displacement_total = np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2)
        displacements_total.append(displacement_total)

    return x, y, np.mean(displacements_total), displacements_total

# --- INTERFAZ GRÁFICA ---

class App:
    def __init__(self, root):
        self.root = root
        root.title("Simulación de Trayectorias de Electrones en un Plasma de Fusión")
        root.geometry("800x700")

        # Entradas
        self.te_entry = self.create_entry("Temperatura (K):", "1.16e7")
        self.n_entry = self.create_entry("Número de partículas:", "10000")
        self.steps_entry = self.create_entry("Número de colisiones:", "100")
        self.b0_entry = self.create_entry("Campo magnético B0 (T):", "3.4")

        # Botones
        ttk.Button(root, text="Simular trayectorias", command=self.simular).pack(pady=5)
        ttk.Button(root, text="Ver distribución de velocidades", command=self.ver_distribucion_velocidades).pack(pady=5)
        ttk.Button(root, text="Ver histograma gaussiano", command=self.ver_histograma).pack(pady=5)

        # Área gráfica de trayectorias
        self.graph_frame = ttk.Frame(root)
        self.graph_frame.pack(expand=True, fill="both")

        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Inicializar variables
        self.v0x3 = None
        self.v0y3 = None
        self.ve = None
        self.vei = None

    def create_entry(self, label, default):
        ttk.Label(self.root, text=label).pack()
        entry = ttk.Entry(self.root)
        entry.insert(0, default)
        entry.pack()
        return entry

    def simular(self):
        try:
            Te = float(self.te_entry.get())
            num_particles = int(self.n_entry.get())
            steps = int(self.steps_entry.get())
            B0 = float(self.b0_entry.get())

            self.ve = thermal_velocity(Te)
            self.v0x3, self.v0y3 = generate_initial_velocities3(self.ve, num_particles)

            # Calcular frecuencia de colisión y ciclotrón
            self.q = 1.6e-19  # Carga del electrón
            self.m = 9.11e-31  # Masa del electrón
            lambd = 17
            self.vei = collision_frequency(lambd, self.ve)
            self.omega_c = self.q * B0 / self.m  # Frecuencia ciclotrón (rad/s)
            self.radio_larmor = self.ve / self.omega_c  # Radio de Larmor (m)
            messagebox.showinfo("Frecuencia de colisión", f"vei = {self.vei:.3e} Hz")
            messagebox.showinfo("Frecuencia ciclotrón", f"ω_c = {self.omega_c:.2e} rad/s")
            messagebox.showinfo("Radio de Larmor", f" r_L = {self.radio_larmor:.2e} m")

            # Limpiar gráfico
            self.ax.clear()

            # Trajectorias
            for i in range (num_particles):  # todas las partículas
                x, y, _, _ = integrate_trajectory8(self.v0x3[i], self.v0y3[i], self.vei, B0=B0, steps=steps)
                self.ax.plot(x, y, alpha=0.5)
            self.ax.set_title("Trayectorias con colisiones")
            self.ax.set_xlabel("x (m)")
            self.ax.set_ylabel("y (m)")
            self.ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_distribucion_velocidades(self):
        if self.v0x3 is None or self.v0y3 is None:
            messagebox.showwarning("Atención", "Primero debes simular las trayectorias.")
            return

        # Crear ventana emergente
        window = tk.Toplevel(self.root)
        window.title("Distribución de velocidades")
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(self.v0x3, self.v0y3, s=1, alpha=0.4)
        ax.set_title("Distribución de velocidades iniciales")
        ax.set_xlabel("v0x")
        ax.set_ylabel("v0y")

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        toolbar.pack()
        canvas.get_tk_widget().pack()

    def ver_histograma(self):
        mu = float(f"{self.ve:.3e}")
        sigma = 1
        N = 10**6
        x = metodo_tranfinversa_gaussiana(mu, sigma, N)

        fig, ax = plt.subplots(figsize=(8, 5))
        counts, bins, _ = ax.hist(x, bins=50, density=True, label="Histograma")
        midpoints = (bins[:-1] + bins[1:]) / 2
        pdf = (1 / np.sqrt(2 * np.pi * sigma**2)) * np.exp(-(midpoints - mu)**2 / (2 * sigma**2))
        ax.plot(midpoints, pdf, label="Distribución Teórica", linewidth=2)
        ax.set_title("Método de transformada inversa - Gaussiana")
        ax.set_xlabel("x")
        ax.set_ylabel("P(x)")
        ax.legend()
        ax.grid(True)

        # Mostrar en nueva ventana
        window = tk.Toplevel(self.root)
        window.title("Histograma de Gaussiana")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        toolbar.pack()
        canvas.get_tk_widget().pack()

# Lanzar interfaz
if __name__ == "__main__":
    
    import sys

    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    root = tk.Tk()
    app = App(root)
    root.mainloop()
