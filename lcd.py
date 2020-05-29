from tkinter import *
import serial
from tkinter.font import Font
screenSizeX = 320
screenSizeY = 100

modes = {
    "DCV": {
        "B": "V",
        "C": "V",
        "D": "V",
        "E": "V",
        "F": "V"
    },
    "R2": {
        "B": "Ω",
        "C": "kΩ",
        "D": "kΩ",
        "E": "kΩ",
        "F": "MΩ",
        "G": "MΩ",
        "H": "MΩ"
    }
}

try:
    serial = serial.Serial(
        port='COM26',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        dsrdtr=TRUE,
    )
except serial.SerialException:
    print("Device was not found!")

root = Tk()
root.title('')
root.configure(background='#00ff00')
# root.configure(bg='#0000ff')


root.geometry("%d%s%d" % (screenSizeX, "x", screenSizeY))
root.resizable(0, 0)

canvas = Canvas(root, width=screenSizeX, height=screenSizeY, bg='#00ff00')
canvas.pack()

mode = canvas.create_text(280, 35, font="LcdStd 20", text="DC", anchor=NW, fill="#fff")
value = canvas.create_text(5, 0, font="LcdStd 60", text="-0.0000 V", anchor=NW, fill="#fff")
modifier = canvas.create_text(280, 35, font="LcdStd 25", text="V", anchor=NW, fill="#fff")

def drawText():
    serial.write("CONF?".encode('utf-8'))
    query = getMode(serial.read_until())
    modeText = query[0]
    modifierText = query[1]

    serial.write("READ?".encode('utf-8'))
    data = serial.read_until()
    canvas.itemconfigure(value, text=data)
    canvas.itemconfigure(modifier, text=modifierText)
    canvas.itemconfigure(mode, text=modeText)

    font = Font(family="LcdStd", size=60)
    length = font.measure(data)
    canvas.coords(modifier, length, 38)
    canvas.coords(mode, length, 13)

    serial.write("SYSTEM:LOCAL?".encode('utf-8'))
    root.after(100, drawText)


def getMode(mode):
    query = mode.decode("utf-8").split(',')
    mode = query[0]
    unit = getUnit(mode, query[1])

    text = ""

    if (mode == "DCV"):
        text = "DC"
    elif (mode == "ACV"):
        text = "AC"
    elif (mode == "R2"):
        text = "RES"
    elif (mode == "FREQ"):
        text = "FRQ"
    elif (mode == "PERIOD"):
        text = "PRD"
    elif (mode == "CONT"):
        text = "CONT"
    elif (mode == "DIOD"):
        text = "DIODE"
    return [text, unit]


def getUnit(mode, unit):
    modeT = ""
    if mode in modes:
        if unit in modes[mode]:
            modeT = modes[mode][unit]
    return modeT


drawText()
root.mainloop()
