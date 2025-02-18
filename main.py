import os.path
import sys

import pystray
from PIL import Image

from autostart import AutoStartHandler
from hotkey import HotkeyHandler
from keyboard import KeyboardController


def get_absolute_image_path() -> str:
    """
    Get the absolute path to the image used in the tray icon.
    :return: String of the path the image is in.
    """
    relative_file_path = "files/januskey.png"

    # Set by the pyinstaller bundler to the directory the actual files are in
    absolute_directory = getattr(sys, "_MEIPASS", None)
    if absolute_directory:
        return os.path.join(absolute_directory, relative_file_path)

    return relative_file_path


def main() -> None:
    keyboard_controller = KeyboardController()

    hotkey_handler = HotkeyHandler(keyboard_controller.type_clipboard_contents)
    hotkey_handler.start()

    autostart_handler = AutoStartHandler()

    tray_icon = pystray.Icon(
        "Paste Prime",
        icon=Image.open(get_absolute_image_path()),
        menu=pystray.Menu(
            pystray.MenuItem(
                "Start with Windows",
                autostart_handler.toggle_auto_start,
                checked=autostart_handler.is_auto_starting,
            ),
            pystray.MenuItem(
                "Exit",
                lambda icon, item: icon.stop(),
            ),
        ),
    )
    tray_icon.run()

    hotkey_handler.stop()


if __name__ == "__main__":
    main()
