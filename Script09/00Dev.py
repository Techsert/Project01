import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os

# ==============================
# CONFIG
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")
IMG_PATH = os.path.join(ASSET_PATH, "img/alphabitSound")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/alphabitSound")

QUESTIONS = [
    {
        "sound": "01alef-s.wav",
        "options": ["05gem.png", "01alef.png", "08dal.png", "12sen.png"],
        "answer": 0,
        "option_size": (200, 200)
    },
    {
        "sound": "02ba-s.wav",
        "options": ["03ta.png", "04tha.png", "02ba.png", "16taa.png"],
        "answer": 0,
        "option_size": (250, 250)
    }
]

# ==============================
# APP CLASS
# ==============================
class WhatIsThis:
    def __init__(self, root):
        self.root = root
        self.root.title("ما هذا؟ 🧠")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="white")

        # State
        self.current_index = 0
        self.score = 0
        self.buttons_disabled = False

        # Pygame setup
        pygame.mixer.init()
        self.channel_question = pygame.mixer.Channel(0)
        self.channel_feedback = pygame.mixer.Channel(1)

        # Preload sounds
        self.loaded_sounds = {}
        self.preload_sounds()

        # Setup UI
        self.setup_ui()

        # Escape key to exit
        self.root.bind("<Escape>", self.exit_fullscreen_stop_sounds)

        # Start quiz
        self.show_question()

    # ==============================
    # SOUND
    # ==============================
    def preload_sounds(self):
        for s in ["correct.wav", "wrong.mp3"]:
            sound_file = os.path.join(SOUND_PATH, s)
            if os.path.exists(sound_file):
                self.loaded_sounds[s] = pygame.mixer.Sound(sound_file)
            else:
                print(f"⚠️ Missing sound: {sound_file}")
        for q in QUESTIONS:
            sound_file = os.path.join(SOUND_PATH, q["sound"])
            if os.path.exists(sound_file):
                self.loaded_sounds[q["sound"]] = pygame.mixer.Sound(sound_file)
            else:
                print(f"⚠️ Missing question sound: {sound_file}")

    def play_sound(self, sound_name, channel="question"):
        ch_map = {"question": self.channel_question, "feedback": self.channel_feedback}
        if sound_name in self.loaded_sounds:
            ch_map[channel].play(self.loaded_sounds[sound_name])
        else:
            print("⚠️ Sound not found:", sound_name)

    # ==============================
    # UI
    # ==============================
    def setup_ui(self):
        # Question Image Placeholder
        self.question_image_label = tk.Label(self.root, bg="white")
        self.question_image_label.pack(pady=50)

        # Answer Images Frame
        self.answers_frame = tk.Frame(self.root, bg="white")
        self.answers_frame.pack(pady=20)

        # Navigation Buttons
        nav_frame = tk.Frame(self.root, bg="white")
        nav_frame.pack(side="bottom", pady=20, fill="x")

        # Next button on the RIGHT
        self.next_button = tk.Button(nav_frame, text="التالي ➡️", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.next_question)
        self.next_button.pack(side="left", padx=50)

        # Previous button on the LEFT
        self.prev_button = tk.Button(nav_frame, text="⬅️ السابق", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.prev_question)
        self.prev_button.pack(side="right", padx=50)

        self.exit_button = tk.Button(nav_frame, text="⏪ إنهاء", font=("Arial", 20, "bold"),
                                     bg="#f8d7da", command=self.root.destroy)
        self.exit_button.pack(side="bottom", pady=10)

    # ==============================
    # QUIZ LOGIC
    # ==============================
    def show_question(self):
        q = QUESTIONS[self.current_index]

        # Load question image
        img_path = os.path.join(IMG_PATH, q["options"][q["answer"]])
        try:
            img = Image.open(img_path).resize((300, 300))
            self.question_photo = ImageTk.PhotoImage(img)
            self.question_image_label.config(image=self.question_photo)
        except FileNotFoundError:
            print("⚠️ Missing question image:", img_path)

        # Clear previous answer buttons
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        # Display answer buttons
        self.option_buttons = []
        option_width, option_height = q.get("option_size", (200, 200))
        for i, option_file in enumerate(q["options"]):
            path = os.path.join(IMG_PATH, option_file)
            try:
                img = Image.open(path).resize((option_width, option_height))
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print("⚠️ Missing answer image:", path)
                photo = None
            btn = tk.Button(self.answers_frame, image=photo, bd=2,
                            command=lambda i=i: self.check_answer(i))
            btn.image = photo
            btn.pack(side="left", padx=20)
            self.option_buttons.append(btn)

        # Play question sound
        self.play_sound(q["sound"], "question")

        # Update navigation buttons
        self.prev_button.config(state="normal" if self.current_index > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_index < len(QUESTIONS) - 1 else "disabled")  # Disable next until feedback is closed

    def check_answer(self, index):
        if self.buttons_disabled:
            return
        self.buttons_disabled = True

        q = QUESTIONS[self.current_index]
        is_correct = index == q["answer"]
        if is_correct:
            self.score += 1

        self.show_feedback(is_correct)

    # ==============================
    # FEEDBACK
    # ==============================
    def show_feedback(self, is_correct):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.config(bg="pink")
        popup.wm_attributes("-transparentcolor", "pink")

        # Load feedback image
        img_file = "thumbsup.png" if is_correct else "thumbsdown.png"
        img_path = os.path.join(IMG_PATH, img_file)
        try:
            img = Image.open(img_path).resize((400, 400))
            photo = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print("⚠️ Missing feedback image:", img_path)
            return

        label_img = tk.Label(popup, image=photo, bg="pink", borderwidth=0, highlightthickness=0)
        label_img.image = photo
        label_img.pack(expand=True)

        # Play feedback sound
        sound_file = "correct.wav" if is_correct else "wrong.mp3"
        self.play_sound(sound_file, "feedback")

        # Center popup
        popup.update_idletasks()
        w, h = 400, 400
        x = (popup.winfo_screenwidth() - w) // 2
        y = (popup.winfo_screenheight() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

        # Function to close feedback
        def close_popup(event=None):
            try:
                popup.after_cancel(auto_close_id)
            except:
                pass
            popup.destroy()
            self.buttons_disabled = False
            self.current_index += 1
            if self.current_index >= len(QUESTIONS):
                self.show_final_result()
            else:
                self.show_question()

        # Bind click to skip feedback
        label_img.bind("<Button-1>", close_popup)

        # Auto-close after 2 seconds
        auto_close_id = popup.after(2000, close_popup)

    # ==============================
    # FINAL RESULT
    # ==============================
    def show_final_result(self):
        popup = tk.Toplevel(self.root)
        popup.title("🏁 النتيجة النهائية 🏁")
        popup.geometry("500x400")
        popup.configure(bg="#e6ffe6")

        msg = f"أحسنت! نتيجتك: {self.score} من {len(QUESTIONS)}"
        tk.Label(popup, text=msg, font=("Arial", 28, "bold"), bg="#e6ffe6").pack(expand=True, pady=50)

        tk.Button(popup, text="🔁 إعادة اللعب", font=("Arial", 20, "bold"),
                  bg="#cce5ff", command=lambda: [popup.destroy(), self.restart()]).pack(pady=10)

        tk.Button(popup, text="⏪ إنهاء", font=("Arial", 20, "bold"),
                  bg="#f8d7da", command=self.root.destroy).pack(pady=10)

    def restart(self):
        self.current_index = 0
        self.score = 0
        self.show_question()

    # ==============================
    # NAVIGATION
    # ==============================
    def next_question(self):
        if self.current_index < len(QUESTIONS) - 1:
            self.current_index += 1
            self.show_question()

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_question()

    # ==============================
    # MISC
    # ==============================
    def exit_fullscreen_stop_sounds(self, event=None):
        self.root.attributes('-fullscreen', False)
        pygame.mixer.stop()

# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = WhatIsThis(root)
    root.mainloop()
