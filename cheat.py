import dearpygui.dearpygui as dpg
from pymem import Pymem as pm
from time import sleep
import threading

process = pm("ac_client.exe")
baseAddress = process.base_address

# Offsets

localPlayerOffset = 0x10F4F4
hpOffset = 0xF8
rifleAmmoOffset = 0x150
bombOffset = 0x158
xOffset = 0x34
yOffset = 0x38
zOffset = 0x3C


# Helper functions


def getPointerAddress(base, offsets):
    addr = process.read_int(base)

    if type(offsets) is list:
        for offset in offsets:

            if offset != offsets[-1]:
                addr = process.read_int(addr + offset)

        addr = addr + offsets[-1]
    else:
        addr = addr + offsets

    return addr


def updateWidgets():
    dpg.set_value(
        "hp_widget",
        "Player HP: "
        + str(
            process.read_int(
                getPointerAddress(baseAddress + localPlayerOffset, hpOffset)
            )
        ),
    )

    dpg.set_value(
        "rifle_ammo_widget",
        "Rifle ammo: "
        + str(
            process.read_int(
                getPointerAddress(baseAddress + localPlayerOffset, rifleAmmoOffset)
            )
        ),
    )

    dpg.set_value(
        "bomb_widget",
        "Bomb amount: "
        + str(
            process.read_int(
                getPointerAddress(baseAddress + localPlayerOffset, bombOffset)
            )
        ),
    )

    dpg.set_value(
        "x_widget",
        "X: "
        + str(
            round(
                process.read_float(
                    getPointerAddress(baseAddress + localPlayerOffset, xOffset)
                ),
                2,
            )
        ),
    )

    dpg.set_value(
        "y_widget",
        "Y: "
        + str(
            round(
                process.read_float(
                    getPointerAddress(baseAddress + localPlayerOffset, yOffset)
                ),
                2,
            )
        ),
    )

    dpg.set_value(
        "z_widget",
        "Z: "
        + str(
            round(
                process.read_float(
                    getPointerAddress(baseAddress + localPlayerOffset, zOffset)
                ),
                2,
            )
        ),
    )


def giveHP():
    process.write_int(
        getPointerAddress(baseAddress + localPlayerOffset, hpOffset), 1000
    )


def giveRifleAmmo():
    process.write_int(
        getPointerAddress(baseAddress + localPlayerOffset, rifleAmmoOffset), 1000
    )


def giveBombs():
    process.write_int(
        getPointerAddress(baseAddress + localPlayerOffset, bombOffset), 1000
    )


def threadStart():
    try:
        while dpg.is_dearpygui_running():
            updateWidgets()
            sleep(0.1)
    finally:
        dpg.stop_dearpygui()


# UI & Start


def createUI():
    dpg.create_context()

    with dpg.window(tag="Main"):
        with dpg.group(horizontal=True):
            dpg.add_text("", tag="x_widget")
            dpg.add_text("", tag="y_widget")
            dpg.add_text("", tag="z_widget")

        dpg.add_text("", tag="hp_widget")
        dpg.add_text("", tag="rifle_ammo_widget")
        dpg.add_text("", tag="bomb_widget")

        with dpg.group():
            dpg.add_button(label="1000 HP", callback=giveHP)
            dpg.add_button(label="1000 rifle ammo", callback=giveRifleAmmo)
            dpg.add_button(label="1000 bombs", callback=giveBombs)

    dpg.create_viewport(width=600, height=200, title="Assault Cube Cheat")
    dpg.setup_dearpygui()
    dpg.set_primary_window("Main", True)
    dpg.show_viewport()

    threading.Thread(target=threadStart, daemon=True).start()

    dpg.start_dearpygui()
    dpg.destroy_context()


createUI()
