import os
import evdev
import tkinter as tk
from tkinter.ttk import Notebook
from evdev import InputDevice, categorize, ecodes

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generic Marco Keyboard Utility")
        self.geometry("500x500")

        self.notebook = Notebook(self)

        main_tab = tk.Frame(self.notebook)
        macro_tab = tk.Frame(self.notebook)

        self.find_kbd_bt = tk.Button(main_tab,text="Find keyboards",command=self.find_kbd)
        self.find_kbd_bt.pack(side=tk.BOTTOM, fill=tk.X)

        self.main_text = tk.StringVar(main_tab)
        self.main_text.set("")

        self.kbd_listbox = tk.Listbox(main_tab,selectmode=tk.SINGLE)
        self.kbd_listbox.configure(exportselection=False)
        self.kbd_listbox.pack(expand=1)
        # self.kbd_listbox.bind()

        self.notebook.add(main_tab,text="Keyboard selection")
        self.notebook.add(macro_tab, text="Macro definition")

        self.notebook.pack(fill=tk.BOTH, expand=1)

    def find_kbd(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        phys = []
        paths = []
        names = []
        for dev in devices:
            caps = dev.capabilities()
            capskey = caps.get(evdev.ecodes.EV_KEY, [])
            if evdev.ecodes.EV_KEY not in caps:
                continue
            elif evdev.ecodes.KEY_CAPSLOCK in capskey:
                if evdev.ecodes.BTN_RIGHT not in capskey:
                    phys.append(dev.phys)
                    paths.append(dev.fn)
                    names.append(dev.name)

        self.kbd_listbox.delete(0, tk.END)
        for i in range(len(names)):
            self.kbd_listbox.insert(i, names[i])


root = Root()
root.mainloop()


"""
macro_kbd = InputDevice('/dev/input/event8')
main_kbd = InputDevice('/dev/input/event5')
macro_led = 2
numlock_led = 0
ON = 1
OFF = 0
mode='MACROS_OFF'

def set_leds(led, state):
        macro_kbd.set_led(led,state)
        main_kbd.set_led(led,state)


for event in macro_kbd.read_loop():
    if event.type == ecodes.EV_KEY:
        key = categorize(event)
        if key.keystate == key.key_down:
            if mode == 'MACROS_ON':
                if key.keycode == 'KEY_SCROLLLOCK':
                    mode = 'MACROS_OFF'
                    set_leds(macro_led,OFF)
                    macro_kbd.ungrab()
                    set_leds(numlock_led,ON)
                elif key.keycode == 'KEY_F1':
                    os.system('sudo -u g565057 terminator')
                elif key.keycode == 'KEY_F2':
                    os.system('sudo -u g565057 code')
                elif key.keycode == 'KEY_F3':
                    os.system('sudo -u g565057 firefox')
                elif key.keycode == 'KEY_F4':
                    os.system('sudo -u g565057 thuderbird')
                elif key.keycode == 'KEY_SYSRQ':
                    os.system('xkill')
            elif key.keycode == 'KEY_SCROLLLOCK':
                mode = 'MACROS_ON'
                set_leds(macro_led,ON)
                macro_kbd.grab()
"""
