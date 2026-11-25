import time
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional


class WaterReminderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Напоминание пить воду")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.interval_seconds = 60 * 60
        self.deadline: Optional[float] = None
        self.after_id: Optional[str] = None
        self.interval_var = tk.StringVar(value="60")
        self.status_var = tk.StringVar(value="Напоминания остановлены")

        frame = ttk.Frame(root, padding=20)
        frame.grid()

        ttk.Label(
            frame,
            text="Напоминать каждые (минут):",
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Entry(frame, textvariable=self.interval_var, width=8).grid(
            row=1, column=0, sticky="w", pady=(6, 14)
        )

        self.start_button = ttk.Button(
            frame, text="Начать", command=self.start
        )
        self.start_button.grid(row=2, column=0, sticky="ew", padx=(0, 6))
        self.stop_button = ttk.Button(
            frame, text="Остановить", command=self.stop, state="disabled"
        )
        self.stop_button.grid(row=2, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(frame, textvariable=self.status_var).grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(14, 0)
        )

    def start(self) -> None:
        try:
            minutes = int(self.interval_var.get())
        except ValueError:
            messagebox.showerror(
                "Неверный интервал",
                "Введите целое число минут от 1 до 1440.",
                parent=self.root,
            )
            return

        if not 1 <= minutes <= 1440:
            messagebox.showerror(
                "Неверный интервал",
                "Интервал должен быть от 1 до 1440 минут.",
                parent=self.root,
            )
            return

        self._cancel_tick()
        self.interval_seconds = minutes * 60
        self.deadline = time.monotonic() + self.interval_seconds
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self._tick()

    def stop(self) -> None:
        self._cancel_tick()
        self.deadline = None
        self.status_var.set("Напоминания остановлены")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def _tick(self) -> None:
        if self.deadline is None:
            return

        remaining = max(0, int(self.deadline - time.monotonic() + 0.999))
        if remaining == 0:
            self.root.bell()
            messagebox.showinfo(
                "Пора выпить воды 💧",
                "Сделайте небольшой перерыв и выпейте воды.",
                parent=self.root,
            )
            self.deadline = time.monotonic() + self.interval_seconds
            remaining = self.interval_seconds

        minutes, seconds = divmod(remaining, 60)
        hours, minutes = divmod(minutes, 60)
        self.status_var.set(
            f"Следующее напоминание через {hours:02}:{minutes:02}:{seconds:02}"
        )
        self.after_id = self.root.after(1000, self._tick)

    def _cancel_tick(self) -> None:
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def close(self) -> None:
        self._cancel_tick()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    WaterReminderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
