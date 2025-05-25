import serial
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

PORT = 'COM2'
BAUD = 9600


class SensorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Monitor")
        self.root.geometry("480x400")
        self.root.configure(bg="#111111")
        self.data = []
        self.running = False
        self.ser = None
        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#111111", foreground="#EEEEEE", font=("Segoe UI", 11))
        style.configure("Title.TLabel", foreground="#A259FF", font=("Segoe UI", 14, "bold"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#A259FF", foreground="white")
        style.map("TButton", background=[("active", "#9147DB")])

    def build_ui(self):
        ttk.Label(self.root, text="Sensor Monitor", style="Title.TLabel").pack(pady=10)
        self.temp_label = ttk.Label(self.root, text="Temp: -- °C")
        self.temp_label.pack()
        self.pressure_label = ttk.Label(self.root, text="Pressure: -- Pa")
        self.pressure_label.pack()
        self.humidity_label = ttk.Label(self.root, text="Humidity: -- %")
        self.humidity_label.pack()
        ttk.Separator(self.root).pack(fill='x', pady=10)
        ttk.Label(self.root, text="Averages", style="Title.TLabel").pack()
        self.avg_temp = ttk.Label(self.root, text="Avg Temp: --")
        self.avg_temp.pack()
        self.avg_pressure = ttk.Label(self.root, text="Avg Pressure: --")
        self.avg_pressure.pack()
        self.avg_humidity = ttk.Label(self.root, text="Avg Humidity: --")
        self.avg_humidity.pack()
        ttk.Separator(self.root).pack(fill='x', pady=10)
        self.status = tk.Label(self.root, text="Disconnected", bg="#111111", fg="red", font=("Segoe UI", 10, "bold"))
        self.status.pack(pady=5)
        self.toggle_btn = ttk.Button(self.root, text="Start", command=self.toggle_serial)
        self.toggle_btn.pack(pady=5)
        ttk.Button(self.root, text="Export", command=self.export_json).pack(pady=5)

    def toggle_serial(self):
        if self.running:
            self.running = False
            self.toggle_btn.config(text="Start")
            self.status.config(text="Stopped", fg="red")
            if self.ser and self.ser.is_open:
                self.ser.close()
        else:
            try:
                self.ser = serial.Serial(PORT, BAUD, timeout=1)
                self.running = True
                self.toggle_btn.config(text="Stop")
                self.status.config(text="Connected", fg="green")
                threading.Thread(target=self.read_data, daemon=True).start()
            except:
                self.status.config(text="Connection Error", fg="red")

    def read_data(self):
        while self.running:
            try:
                line = self.ser.readline().decode().strip()
                if line:
                    parsed = self.parse_line(line)
                    if parsed:
                        t, p, h = parsed
                        self.data.append({"time": datetime.now().isoformat(), "temp": t, "press": p, "humid": h})
                        self.update_display(t, p, h)
            except:
                break

    def parse_line(self, line):
        try:
            parts = line.split('&')
            t = float(parts[0].split('=')[1])
            p = int(parts[1].split('=')[1])
            h = int(parts[2].split('=')[1])
            return t, p, h
        except:
            return None

    def update_display(self, t, p, h):
        self.temp_label.config(text=f"Temp: {t:.1f} °C")
        self.pressure_label.config(text=f"Pressure: {p} Pa")
        self.humidity_label.config(text=f"Humidity: {h} %")
        self.update_avg()

    def update_avg(self):
        temps = [d["temp"] for d in self.data]
        presses = [d["press"] for d in self.data]
        humids = [d["humid"] for d in self.data]
        if temps:
            self.avg_temp.config(text=f"Avg Temp: {sum(temps) / len(temps):.1f}")
            self.avg_pressure.config(text=f"Avg Pressure: {sum(presses) / len(presses):.1f}")
            self.avg_humidity.config(text=f"Avg Humidity: {sum(humids) / len(humids):.1f}")

    def export_json(self):
        if not self.data:
            messagebox.showwarning("Nothing to export", "No data collected.")
            return
        avg = {
            "temp": sum(d["temp"] for d in self.data) / len(self.data),
            "press": sum(d["press"] for d in self.data) / len(self.data),
            "humid": sum(d["humid"] for d in self.data) / len(self.data)
        }
        output = {
            "records": self.data,
            "averages": avg
        }
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, "w") as f:
                json.dump(output, f, indent=4)
            messagebox.showinfo("Exported", f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root)
    root.mainloop()
