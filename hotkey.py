"""
Module to handle the hotkey being recognized and an action being taken.
"""

from pynput import keyboard


class HotkeyHandler:
    def __init__(self, callback):
        """
        Initializes the handler to listen to Ctrl + Shift + V.
        :param callback: The method to call upon hotkey being pressed.
        """
        self._ctrl_pressed = False
        self._shift_pressed = False
        self.listener = None
        self.callback = callback
        self._is_calling_back = False

    def start(self) -> None:
        """
        Start the keyboard listener. Not thread-blocking.
        """
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
            win32_event_filter=self.win32_event_filter,
        )
        self.listener.start()

    def _on_press(self, key) -> None:
        """
        Method to handle key down events.
        Toggles state of left control and left shift.
        :param key: The key being pressed.
        """
        if key == keyboard.Key.ctrl_l:
            self._ctrl_pressed = True

        if key == keyboard.Key.shift_l:
            self._shift_pressed = True

    def _on_release(self, key) -> None:
        """
        Method to handle key up events.
        Toggles state of left control and left shift.
        :param key: The key being pressed.
        """
        if key == keyboard.Key.ctrl_l:
            self._ctrl_pressed = False

        if key == keyboard.Key.shift_l:
            self._shift_pressed = False

    def win32_event_filter(self, message, data) -> None:
        """
        Filters Windows key events, needed to intercept presses and prevent propagation.
        :param message: The message code.
        :param data: An object holding MSLLHOOKSTRUCT information.
        """
        if not self._shift_pressed or not self._ctrl_pressed or self._is_calling_back:
            return

        if message == 257:  # key released
            return

        if data.vkCode != 86:  # v
            return

        # suppress_event raises a SuppressException,
        # so a finally block ensures the exception is raised AND the callback is called.
        try:
            self.listener.suppress_event()
        finally:
            self._is_calling_back = True
            self.callback()
            self._is_calling_back = False

    def stop(self) -> None:
        """
        Stop the hotkey listener.
        """
        self.listener.stop()
