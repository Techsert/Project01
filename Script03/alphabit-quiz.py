import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os

# ==============================
# CONFIG
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")
IMG_PATH = os.path.join(ASSET_PATH, "img/whatisthis")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/whatIsThis")

QUESTIONS = [
    {
        "sound": "apple.wav",
        "options": ["apple.png", "orange.png", "banana.png", "grape.png"],
        "answer": 0,
        "option_size": (200, 200)
    },
    {
        "sound": "ball.wav",
        "options": ["ball.png", "book.png", "pen.png", "chair.png"],
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

        # Game state
        self.current_index = 0
        self.score = 0
        self.buttons_disabled = False

        # Init pygame mixer
        pygame.mixer.init()
        self.channel_question = pygame.mixer.Channel(0)
        self.channel_feedback = pygame.mixer.Channel(1)

        # Preload sounds
        self.loaded_sounds = {}
        self.preload_sounds()

        # Setup UI
        self.setup_ui()

        # Escape key exits fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen_stop_sounds)

        # Start game
        self.show_question()

    # ==============================
    # SOUND
    # ==============================
    def preload_sounds(self):
        sounds_to_load = ["correct.wav", "wrong.wav"]
        for q in QUESTIONS:
            sounds_to_load.append(q["sound"])

        for s in sounds_to_load:
            sound_file = os.path.join(SOUND_PATH, s)
            if os.path.exists(sound_file):
                self.loaded_sounds[s] = pygame.mixer.Sound(sound_file)
            else:
                print(f"⚠️ Missing sound file: {sound_file}")

    def play_sound(self, sound_name, channel="question"):
        ch = self.channel_question if channel == "question" else self.channel_feedback
        if sound_name in self.loaded_sounds:
            ch.play(self.loaded_sounds[sound_name])
        else:
            print("⚠️ Sound not found:", sound_name)

    # ==============================
    # UI SETUP
    # ==============================
    def setup_ui(self):
        # Replay sound button
        self.replay_button = tk.Button(
            self.root, text="🔊 إعادة الصوت", font=("Arial", 28, "bold"),
            bg="#cce5ff", width=15, height=3, command=self.replay_sound
        )
        self.replay_button.pack(pady=100)

        # Frame for answer choices
        self.answers_frame = tk.Frame(self.root, bg="white")
        self.answers_frame.pack(pady=50)

        # Navigation buttons frame
        nav_frame = tk.Frame(self.root, bg="white")
        nav_frame.pack(side="bottom", pady=20, fill="x")

        # Previous button (RIGHT)
        self.prev_button = tk.Button(nav_frame, text="⬅️ السابق", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.prev_question)
        self.prev_button.pack(side="right", padx=50)

        # Next button (LEFT)
        self.next_button = tk.Button(nav_frame, text="التالي ➡️", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.next_question)
        self.next_button.pack(side="left", padx=50)

        # Exit button (CENTER)
        self.exit_button = tk.Button(nav_frame, text="⏪ إنهاء", font=("Arial", 20, "bold"),
                                     bg="#f8d7da", command=self.root.destroy)
        self.exit_button.pack(side="bottom", pady=10)

    # ==============================
    # QUESTION LOGIC
    # ==============================
    def show_question(self):
        q = QUESTIONS[self.current_index]

        # Clear old answers
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        # Show answer options as buttons
        option_w, option_h = q.get("option_size", (200, 200))
        self.option_buttons = []
        for i, opt_file in enumerate(q["options"]):
            img_path = os.path.join(IMG_PATH, opt_file)
            try:
                img = Image.open(img_path).resize((option_w, option_h))
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print("⚠️ Missing image:", img_path)
                continue

            btn = tk.Button(self.answers_frame, image=photo, bd=2,
                            command=lambda i=i: self.check_answer(i))
            btn.image = photo
            btn.pack(side="left", padx=20)
            self.option_buttons.append(btn)

        # Play the question sound
        self.play_sound(q["sound"], "question")

        # Update navigation button states
        self.prev_button.config(state="normal" if self.current_index > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_index < len(QUESTIONS) - 1 else "disabled")

        self.buttons_disabled = False

    # ==============================
    # ANSWER CHECKING
    # ==============================
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

        w, h = 400, 400
        x = (popup.winfo_screenwidth() - w) // 2
        y = (popup.winfo_screenheight() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

        img_name = "thumbsup.png" if is_correct else "thumbsdown.png"
        img_path = os.path.join(IMG_PATH, img_name)
        try:
            img = Image.open(img_path).resize((w, h))
            photo = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print("⚠️ Missing feedback image:", img_path)
            popup.destroy()
            return

        label = tk.Label(popup, image=photo, bg="pink", borderwidth=0)
        label.image = photo
        label.pack(fill="both", expand=True)

        # Play feedback sound
        sound_file = "correct.wav" if is_correct else "wrong.wav"
        self.play_sound(sound_file, "feedback")

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

        # Allow clicking to skip feedback early
        label.bind("<Button-1>", close_popup)

        # Auto close after 2 seconds
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
    # EXIT HANDLER
    # ==============================
    def replay_sound(self):
        q = QUESTIONS[self.current_index]
        self.play_sound(q["sound"], "question")

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
