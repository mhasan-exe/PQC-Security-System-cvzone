import math
import customtkinter as ctk
from main import brute

print("PQC FILE STARTED")

PC_SPEED = 1_000_000
SUPER_SPEED = 1_000_000_000
QUANTUM_SPEED = 10_000_000_000  # simulated

def format_time(seconds):
    if seconds < 1:
        return "< 1 second"
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365
    if years > 1:
        return f"{years:.2e} years"
    if days > 1:
        return f"{days:.2f} days"
    if hours > 1:
        return f"{hours:.2f} hours"
    return f"{seconds:.2f} seconds"

def pqc_():
    print("PQC FILE STARTED")

    app = ctk.CTk()
    app.geometry("1000x600")
    app.title("PQC Brute-Force Complexity Simulator")

    left = ctk.CTkFrame(app, width=320, corner_radius=20)
    left.pack(side="left", fill="y", padx=10, pady=10)

    right = ctk.CTkFrame(app, corner_radius=20)
    right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ---------------- CONTROLS ----------------
    btn2 = ctk.CTkButton(master=app, text="Brute Force", command=brute)
    btn2.place(relx=0.5, rely=0.7, anchor="center")
    ctk.CTkLabel(left, text="Password Length", font=("Segoe UI", 16, "bold")).pack(pady=10)
    length_slider = ctk.CTkSlider(left, from_=1, to=12, number_of_steps=11)
    length_slider.set(6)
    length_slider.pack(fill="x", padx=20)

    length_label = ctk.CTkLabel(left, text="Length: 6")
    length_label.pack(pady=5)

    charset_vars = {
        "lower": ctk.BooleanVar(value=True),
        "upper": ctk.BooleanVar(value=False),
        "nums": ctk.BooleanVar(value=False),
        "syms": ctk.BooleanVar(value=False),
    }

    ctk.CTkCheckBox(left, text="Lowercase (a-z)", variable=charset_vars["lower"]).pack(anchor="w", padx=20)
    ctk.CTkCheckBox(left, text="Uppercase (A-Z)", variable=charset_vars["upper"]).pack(anchor="w", padx=20)
    ctk.CTkCheckBox(left, text="Numbers (0-9)", variable=charset_vars["nums"]).pack(anchor="w", padx=20)
    ctk.CTkCheckBox(left, text="Symbols (!@#)", variable=charset_vars["syms"]).pack(anchor="w", padx=20)

    # ---------------- RESULTS ----------------

    result = ctk.CTkTextbox(right, font=("Consolas", 14))
    result.pack(fill="both", expand=True, padx=10, pady=10)
    result.configure(state="disabled")

    def update():
        length = int(length_slider.get())
        length_label.configure(text=f"Length: {length}")

        charset = 0
        if charset_vars["lower"].get(): charset += 26
        if charset_vars["upper"].get(): charset += 26
        if charset_vars["nums"].get(): charset += 10
        if charset_vars["syms"].get(): charset += 10

        if charset == 0:
            return

        keyspace = charset ** length

        pc_time = keyspace / PC_SPEED
        super_time = keyspace / SUPER_SPEED
        quantum_time = math.sqrt(keyspace) / QUANTUM_SPEED

        result.configure(state="normal")
        result.delete("1.0", "end")
        result.insert("end", f"Keyspace: {keyspace:.2e}\n\n")
        result.insert("end", f"🖥️ Normal PC: {format_time(pc_time)}\n")
        result.insert("end", f"🏢 Supercomputer: {format_time(super_time)}\n")
        result.insert("end", f"⚛️ Quantum (Grover): {format_time(quantum_time)}\n\n")
        result.insert(
            "end",
            "Explanation:\n"
            "- Classical brute force scales exponentially.\n"
            "- Supercomputers only reduce time linearly.\n"
            "- Quantum computers reduce complexity, not eliminate it.\n"
            "- PQC keys make brute force infeasible even for quantum systems."
        )
        result.configure(state="disabled")

    length_slider.configure(command=lambda _: update())
    for v in charset_vars.values():
        v.trace_add("write", lambda *_: update())

    update()
    app.mainloop()


if __name__ == "__main__":
    pqc_()

