import ctypes
import asyncio

from .constants import keycodes

user32 = ctypes.WinDLL("user32")


class KeyboardHandler:
    def __init__(self, window_handle):
        self.window_handle = window_handle

    async def send_key(self, key, seconds):
        code = keycodes[key]
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendmessagew
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
        user32.PostMessageW(self.window_handle, 0x100, code, 0)
        # Todo: find way to continuously send keys so people can still click in the game window
        await asyncio.sleep(seconds)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
        user32.PostMessageW(self.window_handle, 0x101, code, 0)
