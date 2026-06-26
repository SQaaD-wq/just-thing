import os
import sys
import ctypes
import tkinter as tk
from pynput.keyboard import GlobalHotKeys


class QuickNoteApp:
    def __init__(self) -> None:
        self._ensure_single_instance()

        self.root = tk.Tk()
        self.root.title("Quick Note")
        self.root.configure(bg="#11113E")
        self.root.option_add("*Background", "#11113E")
        self.root.option_add("*Foreground", "white")
        self.root.option_add("*HighlightBackground", "#11113E")
        self.root.option_add("*HighlightColor", "#11113E")
        self.root.attributes("-topmost", True)
        self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.text_widget = tk.Text(
            self.root,
            wrap="word",
            bg="#11113E",
            fg="white",
            bd=0,
            padx=16,
            pady=16,
            insertbackground="white",
            highlightthickness=0,
            relief="flat",
            selectbackground="#2B2B5D",
            selectforeground="white",
            font=("Segoe UI", 12),
        )
        self.text_widget.pack(fill="both", expand=True)
        self.root.bind("<Escape>", lambda _event: self.hide_window())

        self.hotkeys = GlobalHotKeys({"<shift>+e": self.toggle_window})
        self.hotkeys.start()

    def _ensure_single_instance(self) -> None:
        if os.name != "nt":
            return

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._mutex = kernel32.CreateMutexW(None, False, "QuickNoteSingleInstanceMutex")
        if self._mutex is None or kernel32.GetLastError() == 183:
            sys.exit(0)

    def show_window(self) -> None:
        self.text_widget.delete("1.0", tk.END)
        self.root.deiconify()
        self.root.geometry("800x600")
        self.root.update_idletasks()
        self.root.lift()
        self.root.focus_force()
        self.text_widget.focus_set()

    def hide_window(self) -> None:
        self.root.withdraw()
        self.root.update_idletasks()

    def toggle_window(self) -> None:
        if self.root.state() == "withdrawn":
            self.show_window()
        else:
            self.hide_window()

    def run(self) -> None:
        self.root.mainloop()
        self.hotkeys.stop()


if __name__ == "__main__":
    app = QuickNoteApp()
    app.run()
