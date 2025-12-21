import customtkinter as ctk
import threading
import itertools
import string
import time
from queue import Queue

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MAX_TRIES = 500_000   # SAFETY CAP (IMPORTANT)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Brute Force Complexity Visualizer")
        self.geometry("720x520")

        self.running = False
        self.tries = 0
        self.start_time = 0
        self.queue = Queue()

        # ---------------- TOP ----------------
        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20, pady=15)

        self.entry = ctk.CTkEntry(top, placeholder_text="Optional target text (lowercase)")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(top, text="Start", width=80, command=self.start).pack(side="left", padx=5)
        ctk.CTkButton(top, text="Stop", width=80, command=self.stop).pack(side="left", padx=5)

        # ---------------- MID ----------------
        mid = ctk.CTkFrame(self)
        mid.pack(fill="x", padx=20)

        self.len_label = ctk.CTkLabel(mid, text="Length: 3")
        self.len_label.pack(side="left")

        self.slider = ctk.CTkSlider(
            mid, from_=1, to=6,
            number_of_steps=5,
            command=self.update_len
        )
        self.slider.set(3)
        self.slider.pack(side="left", fill="x", expand=True, padx=15)

        # ---------------- STATS ----------------
        self.stats = ctk.CTkLabel(
            self,
            text="Tries: 0 | Speed: 0/s | Status: Idle",
            font=("Consolas", 12)
        )
        self.stats.pack(pady=10)

        self.box = ctk.CTkTextbox(self, height=240, font=("Consolas", 13))
        self.box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.box.configure(state="disabled")

    def update_len(self, value):
        self.len_label.configure(text=f"Length: {int(value)}")

    def start(self):
        if self.running:
            return

        self.running = True
        self.tries = 0
        self.start_time = time.time()

        self.box.configure(state="normal")
        self.box.delete("1.0", "end")
        self.box.insert("end", "Brute force started...\n")
        self.box.configure(state="disabled")

        target = self.entry.get().strip().lower()
        length = len(target) if target else int(self.slider.get())

        threading.Thread(
            target=self.worker,
            args=(length, target),
            daemon=True
        ).start()

        self.update_ui()

    def stop(self):
        self.running = False

    def worker(self, length, target):
        for combo in itertools.product(string.ascii_lowercase, repeat=length):
            if not self.running or self.tries >= MAX_TRIES:
                self.queue.put("⛔ Stopped (Limit Reached)")
                self.running = False
                return

            self.tries += 1

            if target and "".join(combo) == target:
                self.queue.put(f"✅ FOUND at {self.tries} tries")
                self.running = False
                return

        self.queue.put("❌ Target not found")
        self.running = False

    def update_ui(self):
        while not self.queue.empty():
            msg = self.queue.get()
            self.box.configure(state="normal")
            self.box.insert("end", f"{msg}\n")
            self.box.see("end")
            self.box.configure(state="disabled")

        elapsed = time.time() - self.start_time
        speed = int(self.tries / elapsed) if elapsed > 0 else 0
        status = "Running" if self.running else "Stopped"

        self.stats.configure(
            text=f"Tries: {self.tries} | Speed: {speed}/s | Status: {status}"
        )

        if self.running:
            self.after(200, self.update_ui)

def brute():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    brute()

