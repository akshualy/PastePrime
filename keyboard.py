"""
Module to control keyboard actions.
"""

import pyclip
from pynput import keyboard


class KeyboardController:
    def __init__(self):
        """
        Create a keyboard controller.
        """
        self.keyboard_controller = keyboard.Controller()

    def type_clipboard_contents(self) -> bool:
        """
        Get the clipboard contents and type them out as single keystrokes.
        :return: Whether the clipboard had content to be sent as keystrokes.
        """
        clipboard_content = pyclip.paste()
        if not clipboard_content:
            return False

        if isinstance(clipboard_content, bytes):
            clipboard_content = clipboard_content.decode()

        # Not releasing ctrl and shift will trigger other hotkeys.
        self.keyboard_controller.release(keyboard.Key.ctrl_l)
        self.keyboard_controller.release(keyboard.Key.shift_l)
        self.keyboard_controller.type(clipboard_content)
        return True
