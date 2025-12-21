def typewriter(label, full_text, index=0, speed=35):
    if index > len(full_text):
        return
    
    label.configure(text=full_text[:index])
    label.after(speed, lambda: typewriter(label, full_text, index+1, speed)
    )