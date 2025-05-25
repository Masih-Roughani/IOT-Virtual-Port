# Serial Sensor Monitor Project

This project is a graphical Python application that reads and displays sensor data received via a virtual serial port. It calculates real-time averages and supports exporting data as a JSON file.

## 📋 Project Report (Steps Taken)

1. Using **Virtual Serial Port Driver**, I created two virtual COM ports: COM1 and COM2.
2. I launched the `terminal.exe` application and sent sensor data from **COM1** to **COM2**.
3. In the Python application I developed, I read data from **COM2**, and used a separate thread to display the live readings in a GUI interface built with Tkinter. I also saved the incoming data and displayed their averages in real time. A JSON export function was implemented to save all data and calculated averages.
4. In this setup:
   - `COM1` acts as the **Transmitter** (data sender)
   - `COM2` acts as the **Receiver** (data reader)

## ✅ Features

- Real-time reading of temperature, pressure, and humidity values.
- Live calculation and display of averages.
- Dark-mode themed Tkinter UI.
- Start/Stop button to control serial listening.
- Export all records + averages to a `.json` file.

## 🛠 Technologies Used

- Python 3
- PySerial
- Tkinter (ttk themed UI)
- JSON for export
- Virtual Serial Port Driver (for testing)

## 🖼 Example Format of Input Data

```
temp=24.7&press=101300&humid=40
```

## 📤 Output File Format (JSON)

```json
{
  "records": [
    {"time": "2025-05-25T12:00:00", "temp": 25.4, "press": 101325, "humid": 50},
    ...
  ],
  "averages": {
    "temp": 25.2,
    "press": 1010,
    "humid": 48.6
  }
}
```

## 📎 How to Run

1. Connect two virtual ports (e.g., COM1 ↔ COM2).
2. Run `terminal.exe` to send data to COM1.
3. Run the Python GUI app.
4. Click **Start** to begin listening on COM2.
5. Click **Export** to save data to JSON.

---

Feel free to fork or improve the project!
