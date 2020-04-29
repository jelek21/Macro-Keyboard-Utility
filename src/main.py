import os
import evdev
import tkinter as tk
from tkinter.ttk import *
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

    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)

    if type == ERR:
        B1 = tk.Button(popup, text="Quit", command = _exit_(ERROR))
    else:
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
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

        self.main_tab = tk.Frame(self.notebook)
        self.main_tab_bottom = tk.Frame(self.main_tab, height=10)
        self.main_tab_bottom.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)
        self.main_tab_output = tk.Frame(self.main_tab, height=20)
        self.main_tab_output.pack(side=tk.BOTTOM, fill=tk.Y,expand=True)

        self.find_kbd_bt = tk.Button(self.main_tab_bottom, text="Find keyboards", command=self.find_kbds)
        self.find_kbd_bt.pack(in_=self.main_tab_bottom, side=tk.TOP, pady=5)
        
        self.select_kbd_bt = tk.Button(self.main_tab_bottom, text="Select keyboard", command=self.select_kbd, state="disabled")
        self.select_kbd_bt.pack(in_=self.main_tab_bottom, side=tk.TOP, pady=10)

        self.kbd_listbox = tk.Listbox(self.main_tab, selectmode=tk.SINGLE, height=25)
        self.kbd_listbox.configure(exportselection=False)
        self.kbd_listbox.pack(fill=tk.BOTH, expand=True)
        self.kbd_listbox.bind("<<ListboxSelect>>", self.select_kbd_bt.config(state="active"))
        
        self.macro_tab = tk.Frame(self.notebook)
        self.macro_tab_menubar = tk.Frame(self.macro_tab, height=25)
        self.macro_tab_menubar.pack(fill=tk.X)
        # Icons by Icongeek26 : https://www.flaticon.com/authors/icongeek26
        self.img_create = tk.PhotoImage(file="file.png")
        self.img_mod = tk.PhotoImage(file="edit-file.png")
        self.img_del = tk.PhotoImage(file="remove.png")

        self.new_macro = tk.Button(self.macro_tab_menubar, text="New macro", command=self.create_new_macro, image=self.img_create)
        self.new_macro.pack(side=tk.LEFT)

        self.del_macro = tk.Button(self.macro_tab_menubar, text="Delete macro", command=self.delete_macro, image=self.img_del)
        self.del_macro.pack(side=tk.LEFT)

        self.mod_macro = tk.Button(self.macro_tab_menubar, text="Modify macro", command=self.modify_macro, image=self.img_mod)
        self.mod_macro.pack(side=tk.LEFT)

        self.macros_table = Treeview(self.macro_tab,show="headings")
        self.macros_table["columns"]=("keys", "commands")
        self.macros_table.heading("keys",text="Macro keys")
        self.macros_table.heading("commands",text="Macro commands")
        self.macros_table.pack(fill=tk.BOTH,expand=True)



        self.notebook.add(self.main_tab, text="Keyboard selection")
        self.notebook.add(self.macro_tab, text="Macro definition")

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
        macro_kbd = InputDevice(kbd_list[self.kbd_listbox.curselection()[0]][1])
        if __debug__:
            print('Selected ', macro_kbd.name)
    
    def create_new_macro(self):
        print("Clicked on create new macro")

    def delete_macro(self):
        print("Clicked on delete new macro")

    def modify_macro(self):
        print("Clicked on modify new macro")

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
