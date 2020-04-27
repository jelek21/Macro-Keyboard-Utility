import os
import evdev
import tkinter as tk
from tkinter.ttk import Notebook
from evdev import *

ERROR="Error"
WARNING="Warn"
INFO="Information"

## TODO: Create log file in /tmp + message inviting user to post logs on Github
def _exit_(type):
    """
    Exits the programm.

    Parameters:
        type : The reason for our exit.

    type can either be ERR, WARN, INFO or an error code, INFO=0.
    """
    if type == ERR:
        exit(-1)
    elif type == WARN:
        exit(1)
    elif type == INFO:
        exit(0)
    else:
        exit(type)

def _show_popup_(type, msg):
    """
    Prints out a popup at the screen

    Parameters:
        type : The type of message
        msg (str): The message in the popup

    Type can be either ERROR, WARN, or INFO
    Titles and action button depends on the type
    ERROR: button text='Quit' Action=exit(-1)
    No type is a WARN
    """
    popup = tk.Tk()
    if type == ERR:
        popup.title("Error!")
    elif type == INFO:
        popup.title("Info:")
    else:
        popup.wm_title("Warning!")

    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)

    if type == ERR:
        B1 = ttk.Button(popup, text="Quit", command = _exit_(ERROR))
    else:
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

kbd_list=[]

class Root(tk.Tk):
    """
    Main window
    """
    def __init__(self):
        super().__init__()
        self.title("Generic Macro Keyboard Utility")
        self.geometry("500x500")

        self.notebook = Notebook(self)

        main_tab = tk.Frame(self.notebook)
        main_tab_bottom = tk.Frame(main_tab)
        main_tab_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        macro_tab = tk.Frame(self.notebook)

        self.find_kbd_bt = tk.Button(main_tab_bottom, text="Find keyboards", command=self.find_kbds)
        self.find_kbd_bt.pack(in_=main_tab_bottom, side=tk.LEFT)

        self.select_kbd_bt = tk.Button(main_tab_bottom, text="Select keyboard", command=self.select_kbd, state="disabled")
        self.select_kbd_bt.pack(in_=main_tab_bottom, side=tk.RIGHT)

        self.main_text = tk.StringVar(main_tab)
        self.main_text.set("")

        self.kbd_listbox = tk.Listbox(main_tab, selectmode=tk.SINGLE)
        self.kbd_listbox.configure(exportselection=False)
        self.kbd_listbox.pack(expand=True)
        self.kbd_listbox.bind("<<ListboxSelect>>", self.select_kbd_bt.config(state="active"))

        self.notebook.add(main_tab, text="Keyboard selection")
        self.notebook.add(macro_tab, text="Macro definition")

        self.notebook.pack(fill=tk.BOTH, expand=True)

    def find_kbds(self):
        """
        Looks for devices having the EV_KEY capability
        and not the BTN_RIGHT capability (some mouses are registered as keyboards)
        This is not reliable at 100%, some constructors do give weird capabilities
        to their devices.
        List of devices goes in kbd_list
        """
        if __debug__:
            print('Searching for keyboards')
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for dev in devices:
            caps = dev.capabilities()
            capskey = caps.get(evdev.ecodes.EV_KEY, [])
            if evdev.ecodes.EV_KEY not in caps:
                continue
            elif evdev.ecodes.KEY_CAPSLOCK in capskey:
                if evdev.ecodes.BTN_RIGHT not in capskey:
                    kbd_list.append((dev.name,dev.fn))
        if __debug__:
            print('Found ', len(kbd_list), ' keyboards')
        self.kbd_listbox.delete(0, tk.END)
        for i in range(len(kbd_list)):
            self.kbd_listbox.insert(i, kbd_list[i][0])

    def select_kbd(self):
        """
        Function called by the select button, registers which keyboard has been selected.
        Result is stored in macro_kbd
        """
        macro_kbd = InputDevice(kbd_list[self.kbd_listbox.curselection()][1])
        if __debug__:
            print('Selected ', macro_kbd.name)




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
