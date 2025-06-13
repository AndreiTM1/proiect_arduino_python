import serial.tools.list_ports
from tkinter import *

# cfg window
window = Tk()
window.geometry("350x280")
window.title("Proiect <SS2>")
window.configure(bg="#e0f7fa")

# titlu
titlu = Label(window, text="Stație Meteo", font=('Arial', 16, 'bold'),
              bg="#e0f7fa", fg="#006064")
titlu.pack(pady=10)

serialInst = serial.Serial()
portVar = None

# functie conectare la port
def conecteaza_serial():
    global serialInst, portVar

    if serialInst.is_open:
        serialInst.close()

    ports = serial.tools.list_ports.comports()
    portList = []

    for onePort in ports:
        portList.append(str(onePort))
        print(str(onePort))

    val = input("Select Port: COM")
    portVar = None
    for x in range(len(portList)):
        if portList[x].startswith("COM" + str(val)):
            portVar = "COM" + str(val)
            print(f"Conectat la: {portVar}")

    if portVar:
        try:
            serialInst.port = portVar
            serialInst.baudrate = 9600
            serialInst.timeout = 1
            serialInst.open()
            status_bar.config(text=f"Conectat la {portVar}")
        except Exception as e:
            status_bar.config(text=f"Eroare la conectare {portVar}")
            print("Eroare:", e)
    else:
        status_bar.config(text="Port invalid")

# frame pentru date
data_frame = Frame(window, relief=GROOVE, borderwidth=2, bg="#b2ebf2")
data_frame.pack(padx=15, pady=10, fill="x")

# Labeluri pentru valori
temp_ext_label = Label(data_frame, text="Temp ext: -- °C", font=("Arial", 11),
                       anchor="w", bg="#b2ebf2")
temp_ext_label.pack(fill="x", padx=5, pady=2)

umid_ext_label = Label(data_frame, text="Umid ext: -- %", font=("Arial", 11),
                       anchor="w", bg="#b2ebf2")
umid_ext_label.pack(fill="x", padx=5, pady=2)

temp_int_label = Label(data_frame, text="Temp int: -- °C", font=("Arial", 11),
                       anchor="w", bg="#b2ebf2")
temp_int_label.pack(fill="x", padx=5, pady=2)

umid_int_label = Label(data_frame, text="Umid int: -- %", font=("Arial", 11),
                       anchor="w", bg="#b2ebf2")
umid_int_label.pack(fill="x", padx=5, pady=2)

# buton 
conect_btn = Button(window, text="Conectare", command=conecteaza_serial,
                    bg="#00796b", fg="white", font=('Arial', 10, 'bold'))
conect_btn.pack(pady=5)

# actualizare date
def update():
    if serialInst.is_open:
        while serialInst.in_waiting:
            linie = serialInst.readline().decode('utf-8', errors='ignore').strip()

            if linie.startswith("Temp ext:"):
                valoare = linie.split(":")[1].strip()
                temp_ext_label.config(text=f"Temp ext: {valoare} °C")

            elif linie.startswith("Umidit ext:"):
                valoare = linie.split(":")[1].strip()
                umid_ext_label.config(text=f"Umid ext: {valoare} %")

            elif linie.startswith("Temp int:"):
                valoare = linie.split(":")[1].strip()
                temp_int_label.config(text=f"Temp int: {valoare} °C")

            elif linie.startswith("Umidit int:"):
                valoare = linie.split(":")[1].strip()
                umid_int_label.config(text=f"Umid int: {valoare} %")

    window.after(500, update)

update()

# bara de jos
status_bar = Label(window, text="Neconectat", bd=1, relief=SUNKEN,
                   anchor="w", bg="#b2dfdb")
status_bar.pack(side="bottom", fill="x")

window.mainloop()
