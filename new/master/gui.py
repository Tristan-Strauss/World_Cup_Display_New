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
        # Tkinter fullscreen window
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self._exit())
        self.root.config(cursor="none")

        # Track player process
        self.current_process = None
        self.lock = threading.Lock()

        # Setup UI
        self._setup_background()
        self._setup_video_frame()
        self._setup_year_display()

    # ---------- UI helpers ----------
    def _setup_background(self):
        # Set root bg to black to prevent initial white flash
        self.root.configure(bg="black")

        if not BACKGROUND_IMAGE.exists():
            raise FileNotFoundError(f"Background image not found: {BACKGROUND_IMAGE}")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        image = Image.open(BACKGROUND_IMAGE)
        image = image.resize((screen_w, screen_h), Image.LANCZOS)

        self.bg_image = ImageTk.PhotoImage(image)

        if hasattr(self, "bg_label"):
            # Already exists, just update image
            self.bg_label.config(image=self.bg_image)
        else:
            self.bg_label = tk.Label(
                self.root,
                image=self.bg_image,
                borderwidth=0,
                highlightthickness=0
            )
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def _setup_video_frame(self):
        # Frame that mpv will render into
        self.video_frame = tk.Frame(
            self.root,
            bg="",
            borderwidth=0,
            highlightthickness=0
        )
        self.video_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # VERY IMPORTANT: force window creation so winfo_id() works
        self.root.update()
    
    def _setup_year_display(self):
        self.year_var = tk.StringVar()
        self.year_label = tk.Label(
            self.root,
            textvariable=self.year_var,
            font=("Arial", 80, "bold"),
            fg="white",
            bg="black"
        )
        # Position bottom center
        self.year_label.place(
            relx=0.5,
            rely=0.92,
            anchor="center"
        )

    # ---------- Internal helpers ----------

    def _exit(self):
        self.stop()
        self.root.destroy()
        os._exit(0)

    def _play_mpv(self, filename: str):
        path = BASE_DIR / filename
        if not path.exists():
            print(f"ERROR: Video not found: {path}")
            return

        def target():
            with self.lock:
                # Kill any running video
                if self.current_process and self.current_process.poll() is None:
                    os.kill(self.current_process.pid, signal.SIGKILL)
                    self.current_process = None

                # Make sure video frame is on top while playing
                self.video_frame.lift()
                wid = self.video_frame.winfo_id()
                self.hide_year_display()

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
                        str(path),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            # Wait for video to finish
            self.current_process.wait()

            with self.lock:
                self.current_process = None

            # Clear video frame to reveal background
            self.video_frame.lower()  # Push video frame behind background
            self.show_year_display()

        threading.Thread(target=target, daemon=True).start()

    # ---------- Public API ----------

    def play_year(self, year: int):
        if (
            year < self.START_YEAR
            or year > self.END_YEAR
            or (year - self.START_YEAR) % self.STEP != 0
        ):
            print(f"ERROR: Invalid year {year}")
            return

        self._play_mpv(f"{year}.mp4")

    def play_by_name(self, name: str):
        try:
            year = int(name)
        except ValueError:
            print(f"ERROR: Invalid video name '{name}'")
            return

        print(f"[DEBUG] Starting video with name: {name}")
        self.play_year(year)

    def stop(self):
        with self.lock:
            if self.current_process and self.current_process.poll() is None:
                os.kill(self.current_process.pid, signal.SIGKILL)
                self.current_process = None

    def update_year_display(self, text):
        # Pad with underscores so it always shows 4 slots
        padded = text + "_" * (4 - len(text))
        self.root.after(0, lambda: self.year_var.set(padded))
    
    def hide_year_display(self):
        self.root.after(0, lambda: self.year_label.place_forget())

    def show_year_display(self):
        self.root.after(0, lambda: self.year_label.place(
            relx=0.5,
            rely=0.92,
            anchor="center"
        ))

    def stop_video(self):
        with self.lock:
            if self.current_process and self.current_process.poll() is None:
                os.kill(self.current_process.pid, signal.SIGKILL)
                self.current_process = None

        # Make sure UI resets
        self.show_year_display()

    # ---------- Run ----------

    def start(self):
        self.root.mainloop()