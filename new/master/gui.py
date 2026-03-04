import tkinter as tk
import subprocess
import threading
import os
import signal
from pathlib import Path
from PIL import Image, ImageTk

BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_IMAGE = Path("/home/pi/World_Cup_Display/new/master/background.jpeg")


class VideoPlayer:
    START_YEAR = 1930
    END_YEAR = 2134
    STEP = 4

    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self._exit())
        self.root.config(cursor="none")
        self.root.configure(bg="black")

        self.current_process = None
        self.lock = threading.Lock()

        self._setup_background()
        self._setup_video_frame()
        self._setup_year_display()
        self._setup_volume_popup()

    # ---------- UI setup ----------

    def _setup_background(self):
        if not BACKGROUND_IMAGE.exists():
            raise FileNotFoundError(BACKGROUND_IMAGE)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        image = Image.open(BACKGROUND_IMAGE)
        image = image.resize((screen_w, screen_h), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)

        self.bg_label = tk.Label(self.root, image=self.bg_image, borderwidth=0)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def _setup_video_frame(self):
        self.video_frame = tk.Frame(self.root, bg="", borderwidth=0)
        self.video_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.update()
        self.video_frame.lower()

    def _setup_year_display(self):
        self.year_var = tk.StringVar()
        self.year_label = tk.Label(
            self.root,
            textvariable=self.year_var,
            font=("Arial", 80, "bold"),
            fg="white",
            bg="black"
        )
        self.year_label.place(relx=0.5, rely=0.92, anchor="center")

    def _setup_volume_popup(self):
        self.volume_var = tk.StringVar()

        self.volume_label = tk.Label(
            self.root,
            textvariable=self.volume_var,
            font=("Arial", 32, "bold"),
            fg="white",
            bg="black",
            padx=16,
            pady=8
        )

        self._volume_hide_job = None

    # ---------- Internal helpers ----------

    def _exit(self):
        self.stop()
        self.root.destroy()
        os._exit(0)

    def _play_mpv(self, filename):
        path = BASE_DIR / filename
        if not path.exists():
            print(f"ERROR: Video not found: {path}")
            return

        def target():
            with self.lock:
                if self.current_process and self.current_process.poll() is None:
                    os.kill(self.current_process.pid, signal.SIGKILL)

                # Bring video frame up
                self.video_frame.lift()
                self.hide_year_display()

                # 🔥 Ensure volume popup always stays above video
                self.volume_label.lift()

                wid = self.video_frame.winfo_id()

                self.current_process = subprocess.Popen(
                    [
                        "mpv",
                        f"--wid={wid}",
                        "--no-border",
                        "--really-quiet",
                        "--no-terminal",
                        "--force-window=no",
                        "--keep-open=no",
                        "--vo=x11",
                        str(path)
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            self.current_process.wait()

            with self.lock:
                self.current_process = None

            self.video_frame.lower()
            self.show_year_display()

        threading.Thread(target=target, daemon=True).start()

    # ---------- Public API ----------

    def play_year(self, year):
        if year < self.START_YEAR or year > self.END_YEAR or (year - self.START_YEAR) % self.STEP != 0:
            print(f"ERROR: Invalid year {year}")
            return
        self._play_mpv(f"{year}.mp4")

    def play_by_name(self, name):
        try:
            year = int(name)
        except ValueError:
            print(f"ERROR: Invalid video name '{name}'")
            return
        self.play_year(year)

    def stop(self):
        with self.lock:
            if self.current_process and self.current_process.poll() is None:
                os.kill(self.current_process.pid, signal.SIGKILL)
                self.current_process = None

    def stop_video(self):
        self.stop()
        self.show_year_display()

    def update_year_display(self, text):
        padded = text + "_" * (4 - len(text))
        self.root.after(0, lambda: self.year_var.set(padded))

    def hide_year_display(self):
        self.root.after(0, self.year_label.place_forget)

    def show_year_display(self):
        self.root.after(0, lambda: self.year_label.place(
            relx=0.5, rely=0.92, anchor="center"
        ))

    # ---------- Volume popup ----------

    def show_volume(self, volume_percent):
        def _show():
            self.volume_var.set(f"Volume {volume_percent}%")

            # 📍 Top-left corner with padding
            self.volume_label.place(
                x=20,
                y=20,
                anchor="nw"
            )

            # 🔝 Always above video + background
            self.volume_label.lift()

            if self._volume_hide_job:
                self.root.after_cancel(self._volume_hide_job)

            self._volume_hide_job = self.root.after(1500, self.hide_volume)

        self.root.after(0, _show)

    def hide_volume(self):
        self.volume_label.place_forget()
        self._volume_hide_job = None

    # ---------- Run ----------

    def start(self):
        self.root.mainloop()