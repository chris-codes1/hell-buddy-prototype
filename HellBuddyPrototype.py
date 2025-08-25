import ctypes
import time
import keyboard
import random
import os
import pygetwindow as gw
import tkinter as tk
from PIL import Image, ImageTk

# Constants for key event
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002

# Vars
macroToggle = True
macroDisabledOverlay = None

# WASD
# keysToHex = {
#     "W": 0x57,
#     "A": 0x41,
#     "S": 0x53,
#     "D": 0x44,
# }

# Arrow keys
keysToHex = {
    "W": 0x26,
    "A": 0x25,
    "S": 0x28,
    "D": 0x27,
}

# Home, Delete, End, Page Down
# keysToHex = {
#     "W": 0x24,
#     "A": 0x2E,
#     "S": 0x23,
#     "D": 0x22,
# }

stratagems = {
  "Machine Gun": ["S", "A", "S", "W", "D"],
  "Anti-Materiel Rifle": ["S", "A", "D", "W", "S"],
  "Stalwart": ["S", "A", "S", "W", "W", "A"],
  "Expendable Anti-Tank": ["S", "S", "A", "W", "D"],
  "Recoilless Rifle": ["S", "A", "D", "D", "A"],
  "Flamethrower": ["S", "A", "W", "S", "W"],
  "Autocannon": ["S", "A", "S", "W", "W", "D"],
  "Heavy Machine Gun": ["S", "A", "W", "S", "S"],
  "Airburst Rocket Launcher": ["S", "W", "W", "A", "D"],
  "Commando": ["S", "A", "W", "S", "D"],
  "Railgun": ["S", "D", "S", "W", "A", "D"],
  "Spear": ["S", "S", "W", "S", "S"],
  "W.A.S.P Launcher": ["S", "S", "W", "S", "D"],
  "Orbital Gatling Barrage": ["D", "S", "A", "W", "W"],
  "Orbital Airburst Strike": ["D", "D", "D"],
  "Orbital 120mm HE Barrage": ["D", "D", "S", "A", "D", "S"],
  "Orbital 380mm HE Barrage": ["D", "S", "W", "W", "A", "S", "S"],
  "Orbital Walking Barrage": ["D", "S", "D", "S", "D", "S"],
  "Orbital Laser": ["D", "S", "W", "D", "S"],
  "Orbital Napalm Barrage": ["D", "D", "S", "A", "D", "W"],
  "Orbital Railcannon Strike": ["D", "W", "S", "S", "D"],
  "Eagle Strafing Run": ["W", "D", "D"],
  "Eagle Airstrike": ["W", "D", "S", "D"],
  "Eagle Cluster Bomb": ["W", "D", "S", "S", "D"],
  "Eagle Napalm Airstrike": ["W", "D", "S", "W"],
  "Jump Pack": ["S", "W", "W", "S", "W"],
  "Eagle Smoke Strike": ["W", "D", "W", "S"],
  "Eagle 110mm Rocket Pods": ["W", "D", "W", "A"],
  "Eagle 500kg Bomb": ["W", "D", "S", "S", "S"],
  "Fast Recon Vehicle": ["A", "S", "D", "S", "D", "S", "W"],
  "Orbital Precision Strike": ["D", "D", "W"],
  "Orbital Gas Strike": ["D", "D", "S", "D"],
  "Orbital EMS Strike": ["D", "D", "A", "S"],
  "Orbital Smoke Strike": ["D", "D", "S", "W"],
  "HMG Emplacement": ["S", "W", "A", "D", "D", "A"],
  "Shield Generator Relay": ["S", "S", "A", "D", "A", "D"],
  "ARC-3 Tesla Tower": ["S", "W", "D", "W", "A", "D"],
  "Grenadier Battlement": ["S", "D", "S", "A", "D"],
  "Anti-Personnel Minefield": ["S", "A", "W", "D"],
  "Supply Pack": ["S", "A", "S", "W", "W", "S"],
  "Grenade Launcher": ["S", "A", "W", "A", "S"],
  "Laser Cannon": ["S", "A", "S", "W", "A"],
  "Incendiary Mines": ["S", "A", "A", "S"],
  "Guard Dog Rover": ["S", "W", "A", "W", "D", "D"],
  "Ballistic Shield Backpack": ["S", "A", "S", "S", "W", "A"],
  "ARC-3 Arc Thrower": ["S", "D", "S", "W", "A", "A"],
  "Anti-Tank Mines": ["S", "A", "W", "W"],
  "Quasar Cannon": ["S", "S", "W", "A", "D"],
  "Shield Generator Pack": ["S", "W", "A", "D", "A", "D"],
  "Gas Mines": ["S", "A", "A", "D"],
  "Machine Gun Sentry": ["S", "W", "D", "D", "W"],
  "Gatling Sentry": ["S", "W", "D", "A"],
  "Mortar Sentry": ["S", "W", "D", "D", "S"],
  "Guard Dog AR-23": ["S", "W", "A", "W", "D", "S"],
  "Autocannon Sentry": ["S", "W", "D", "W", "A", "W"],
  "Rocket Sentry": ["S", "W", "D", "D", "A"],
  "EMS Mortar Sentry": ["S", "W", "D", "S", "D"],
  "Patriot Exosuit": ["A", "S", "D", "W", "A", "S", "S"],
  "Emancipator Exosuit": ["A", "S", "D", "W", "A", "S", "W"],
  "Steriliser": ["S", "A", "W", "S", "A"],
  "Guard Dog Dog Breath": ["S", "W", "A", "W", "D", "W"],
  "Directional Shield": ["S", "W", "A", "D", "W", "W"],
  "Anti-Tank Emplacement": ["S", "W", "A", "D", "D", "D"],
  "Flame Sentry": ["S", "W", "D", "S", "W", "W"],
  "Portable Hellbomb": ["S", "D", "W", "W", "W"],
  "Hover Pack": ["S", "W", "W", "S", "A", "D"],
  "One True Flag": ["S", "A", "D", "D", "W"],
  "De-Escalator": ["A", "D", "W", "A", "D"],
  "Guard Dog ARC-3": ["S", "W", "A", "W", "D", "A"],
  "Epoch": ["S", "A", "W", "A", "D"],
  "Laser Sentry": ["S", "W", "D", "S", "W", "D"],
  "Warp Pack": ["S", "A", "D", "S", "A", "D"],
  "Reinforce": ["W", "S", "D", "A", "W"],
  "SoS Beacon": ["W", "S", "D", "W"],
  "Resupply": ["S", "S", "W", "D"],
  "Eagle Rearm": ["W", "W", "A", "W", "D"],
  "SSSD Delivery": ["S", "S", "S", "W", "W"],
  "Prospecting Drill": ["S", "S", "A", "D", "S", "S"],
  "Super Earth Flag": ["S", "W", "S", "W"],
  "Hellbomb": ["S", "W", "A", "S", "W", "D", "S", "W"],
  "Upload Data": ["A", "D", "W", "W", "W"],
  "Seismic Probe": ["W", "W", "A", "D", "S", "S"],
  "SEAF Artillery": ["D", "W", "W", "S"],
  "Hive Breaker Drill": ["A", "W", "S", "D", "S", "S"]
}

# Bugs
# Bugs with mission stratagem
equippedStratagems = {
    1: "Resupply",
    2: "Autocannon",
    3: "Orbital Gatling Barrage",
    4: "Eagle 500kg Bomb",
    5: "Orbital Napalm Barrage",
    6: "Reinforce",
    7: "Eagle Rearm",
}

# Bugs default
equippedStratagems = {
    1: "Resupply",
    2: "Warp Pack",
    3: "Grenade Launcher",
    4: "Eagle 500kg Bomb",
    5: "Orbital Napalm Barrage",
    6: "Reinforce",
    7: "Eagle Rearm",
}

# Bugs defence
# equippedStratagems = {
#     1: "Resupply",
#     2: "Autocannon Sentry",
#     3: "Rocket Sentry",
#     4: "Gas Mines",
#     5: "Anti-Personnel Minefield",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# Pete synergy
# equippedStratagems = {
#     1: "Resupply",
#     2: "Emancipator Exosuit",
#     3: "Eagle Napalm Airstrike",
#     4: "Eagle 500kg Bomb",
#     5: "Orbital Napalm Barrage",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# equippedStratagems = {
#     1: "Resupply",
#     2: "Grenade Launcher",
#     3: "Orbital Laser",
#     4: "Eagle 500kg Bomb",
#     5: "Orbital Napalm Barrage",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# Bugs defence
# equippedStratagems = {
#     1: "Resupply",
#     2: "Jump Pack",
#     3: "Grenade Launcher",
#     4: "Eagle 500kg Bomb",
#     5: "Orbital Napalm Barrage",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# equippedStratagems = {
#     1: "Resupply",
#     2: "Autocannon",
#     3: "Emancipator Exosuit",
#     4: "Eagle 500kg Bomb",
#     5: "Orbital Napalm Barrage",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# Bugs 2
# equippedStratagems = {
#     1: "Resupply",
#     2: "Orbital Laser",
#     3: "Orbital Gatling Barrage",
#     4: "Eagle 500kg Bomb",
#     5: "Orbital Napalm Barrage",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# # Bots
# equippedStratagems = {
#     1: "Resupply",
#     2: "Hover Pack",
#     3: "Commando",
#     4: "Expendable Anti-Tank",
#     5: "Anti-Tank Emplacement",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# equippedStratagems = {
#     1: "Resupply",
#     2: "Portable Hellbomb",
#     3: "Commando",
#     4: "Expendable Anti-Tank",
#     5: "Anti-Tank Emplacement",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# equippedStratagems = {
#     1: "Resupply",
#     2: "Laser Cannon",
#     3: "Supply Pack",
#     4: "Orbital Laser",
#     5: "Eagle Strafing Run",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# equippedStratagems = {
#     1: "Resupply",
#     2: "Laser Cannon",
#     3: "Supply Pack",
#     4: "Orbital Laser",
#     5: "Anti-Tank Emplacement",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# Illuminate
# equippedStratagems = {aasd
#     2: "Recoilless Rifle",
#     3: "Orbital Laser",
#     4: "Eagle 500kg Bomb",
#     5: "Orbital Napalm Barrage",
#     6: "Reinforce",
#     7: "Eagle Rearm",
# }

# # Numpad 1, 2, 3, 4 etc.
# stratagemKeybinds = {
#     1: {"name": "1", "scan_code": 79},
#     2: {"name": "2", "scan_code": 80},
#     3: {"name": "3", "scan_code": 81},
#     4: {"name": "4", "scan_code": 75},
#     5: {"name": "5", "scan_code": 76},
#     6: {"name": "6", "scan_code": 77},
#     7: {"name": "7", "scan_code": 71},
# }

# Text keys
stratagemKeybinds = {
    1: {"name": "T", "scan_code": 20},
    2: {"name": "Y", "scan_code": 21},
    3: {"name": "H", "scan_code": 35},
    4: {"name": "B", "scan_code": 48},
    5: {"name": "N", "scan_code": 49},
    6: {"name": "J", "scan_code": 36},
    7: {"name": "U", "scan_code": 22},
}

def showMacroDisabledOverlay(root):
    global macroDisabledOverlay
    if macroDisabledOverlay is not None:
        return  # Already shown
    
    macroDisabledOverlay = tk.Frame(root, bg="black")
    macroDisabledOverlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    label = tk.Label(macroDisabledOverlay, text="Macro Disabled", bg="black", fg="white", font=("Arial", 24))
    label.pack(expand=True)


def hideMacroDisabledOverlay():
    global macroDisabledOverlay
    if macroDisabledOverlay is not None:
        macroDisabledOverlay.destroy()
        macroDisabledOverlay = None

def activateStratagem(stratagemNumber):
    active_window = gw.getActiveWindow()
    if macroToggle == False:
        return
    elif active_window.title != "HELLDIVERS™ 2":
        # print(f"Selected window == '{active_window.title}', not 'HELLDIVERS™ 2'")
        return
    elif stratagemNumber not in equippedStratagems:
        print(f"Key number '{stratagemNumber}' is not bound to any stratagem.")
        return
    elif equippedStratagems[stratagemNumber] not in stratagems:
        print(f"No stratagem key combo data was set for '{stratagemNumber}' stratagem.")
        return

    # Left ctrl
    ctypes.windll.user32.keybd_event(0xA2, 0, KEYEVENTF_KEYDOWN, 0)
    time.sleep(0.05)
    # Stratagem
    for key in stratagems[equippedStratagems[stratagemNumber]]:
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(keysToHex[key], 0, KEYEVENTF_KEYDOWN, 0)
        time.sleep(0.03)
        ctypes.windll.user32.keybd_event(keysToHex[key], 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0xA2, 0, KEYEVENTF_KEYUP, 0)

def toggleMacro(root):
    global macroToggle
    macroToggle = not macroToggle
    if not macroToggle:
        showMacroDisabledOverlay(root)
    else:
        hideMacroDisabledOverlay()

# GUI Setup
def createGui():
    root = tk.Tk()
    root.title("Helldivers 2 Macro")
    root.configure(bg="black")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.iconbitmap('HellBuddyPrototypeIcon.ico')
    root.attributes("-alpha", 0.85)
    # root.geometry(f"+960+0")

    # Example custom title bar
    title_bar = tk.Frame(root, bg="gray5", relief="raised", bd=0)
    title_bar.pack(fill="x")

    frame = tk.Frame(root, padx=10, pady=10, bg="black")
    frame.pack()

    title_label = tk.Label(title_bar, text="Helldivers 2 Macro", bg="gray5", fg="white")
    title_label.pack(side="left", padx=10)

    # Close button
    close_button = tk.Button(title_bar, text="X", bg="gray5", fg="white", command=root.destroy, bd=0)
    close_button.pack(side="right", padx=5) 

    # --- Make the window draggable with the title_bar ---
    def start_move(event):
        root.x = event.x_root
        root.y = event.y_root

    def do_move(event):
        dx = event.x_root - root.x
        dy = event.y_root - root.y
        geom = root.geometry()
        # Get current position
        plus = geom.find('+')
        if plus != -1:
            parts = geom[plus+1:].split('+')
            x = int(parts[0])
            y = int(parts[1])
        else:
            x = 0
            y = 0
        root.geometry(f"+{x+dx}+{y+dy}")
        root.x = event.x_root
        root.y = event.y_root

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)

    images = []
    for i, stratagemName in equippedStratagems.items():
        if stratagemName:
            try:
                image_path = os.path.join("StratagemIcons", f"{stratagemName}.png")
                img = Image.open(image_path).resize((50, 50), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                images.append(photo)  # Save reference to avoid garbage collection
                label = tk.Label(
                    frame,
                    image=photo,
                    text=stratagemKeybinds[i]["name"].upper(),
                    compound="top",
                    bg="black",      # Label background
                    fg="white"       # Label text color
                )

                label.pack(side="left", padx=5)
            except Exception as e:
                print(f"Failed to load {stratagemName}: {e}")

    # Macro hotkey bindings
    for key in equippedStratagems.keys():
        bind = stratagemKeybinds[key]
        keyboard.on_press_key(
            bind["name"],
            lambda event, v=key, b=bind: activateStratagem(v) if event.name.upper() == b["name"] and event.scan_code == b["scan_code"] else None
        )

    # Toggle overlay with right ctrl
    keyboard.on_press_key("right ctrl", lambda event: toggleMacro(root) if event.name == "right ctrl" else None)

    # Show overlay initially if macroToggle is False
    if not macroToggle:
        showMacroDisabledOverlay(root)

    root.mainloop()

if __name__ == "__main__":
    createGui()
