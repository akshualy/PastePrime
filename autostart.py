"""
Module to handle the program being written into the Windows autostart.
"""
import logging
import sys
import winreg
from contextlib import contextmanager


class AutoStartHandler:
    def __init__(self):
        """
        Sets up registry key values needed.
        """
        self._registry_key = winreg.HKEY_CURRENT_USER
        self._registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        self._registry_reservation = 0
        self._registry_access = winreg.KEY_ALL_ACCESS
        self._registry_value_name = "PastePrime"
        self._registry_value = (
            f'"{sys.executable}"'  # Put path in quotation marks in case of spaces
            if sys.executable.endswith(".exe")
            else None
        )

    @contextmanager
    def _key_context(self) -> winreg.HKEYType:
        """
        Get the auto start registry context.
        :return: The Windows HKEY responsible for automatically starting programs.
        """
        with winreg.OpenKey(
            self._registry_key,
            self._registry_path,
            self._registry_reservation,
            self._registry_access,
        ) as autostart_key:
            yield autostart_key

    def is_auto_starting(self, _icon: object | None = None) -> bool:
        """
        Check if the program is already registered for auto start.
        :param _icon: Placeholder parameter, needed by the tray icon library.
        :return: Whether the program is registered to be automatically started.
        """
        try:
            with self._key_context() as autostart_key:
                value, _type_id = winreg.QueryValueEx(autostart_key, self._registry_value_name)
            return value == self._registry_value
        except FileNotFoundError:
            # Expected to happen if value does not exist
            pass

        return False

    def _remove_from_auto_start(self) -> None:
        """
        Remove the program from the auto start registry.
        """
        with self._key_context() as autostart_key:
            try:
                winreg.DeleteValue(autostart_key, self._registry_value_name)
                logging.info("Toggled auto start to false.")
            except Exception as e:
                # TODO The user should be informed if this fails.
                logging.exception(e)

    def _add_to_auto_start(self) -> None:
        """
        Add the program to the auto start registry.
        """
        with self._key_context() as autostart_key:
            try:
                winreg.SetValueEx(
                    autostart_key,
                    self._registry_value_name,
                    self._registry_reservation,
                    winreg.REG_SZ,
                    self._registry_value,
                )
                logging.info("Toggled auto start to true.")
            except Exception as e:
                # TODO The user should be informed if this fails.
                logging.exception(e)

    def toggle_auto_start(self) -> None:
        """
        Depending on whether the program is already registered for auto start,
        the registry key will be deleted or written to the registry.
        """
        if not self._registry_value:
            logging.warning("You can not register the python script for auto-start.")
            return

        if self.is_auto_starting():
            self._remove_from_auto_start()
            return

        self._add_to_auto_start()
