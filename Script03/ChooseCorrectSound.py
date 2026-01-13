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

# Example questions
QUESTIONS = [
    {
        "sound": "apple.wav",
        "options": ["apple.png", "orange.png", "banana.png", "grape.png"],
        "answer": 0,
        "answer_sounds": ["apple.wav", "orange.wav", "banana.wav", "grape.wav"],
        "option_size": (200, 200)  # width, height for answer images
    },
    {
        "sound": "ball.wav",
        "options": ["ball.png", "book.png", "pen.png", "chair.png"],
        "answer": 0,
        "answer_sounds": ["ball.wav", "book.wav", "pen.wav", "chair.wav"],
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
        self.root.configure(bg="#ffffff")

        # State
        self.current_index = 0
        self.buttons_disabled = False
        self.score = 0

        # Pygame setup
        pygame.mixer.init()
        self.channel_question = pygame.mixer.Channel(0)
        self.channel_answer = pygame.mixer.Channel(1)
        self.channel_feedback = pygame.mixer.Channel(2)

        # Preload sounds
        self.loaded_sounds = {}
        self.preload_sounds(QUESTIONS)

        # Setup UI
        self.setup_ui()

        # Escape key
        self.root.bind("<Escape>", self.exit_fullscreen_stop_sounds)

        # Start quiz
        self.show_question()

    # ==============================
    # SOUND
    # ==============================
    def preload_sounds(self, questions):
        for q in questions:
            paths = [q["sound"]] + q["answer_sounds"] + ["correct.wav", "wrong.wav"]
            for s in paths:
                sound_file = os.path.join(SOUND_PATH, s)
                if os.path.exists(sound_file):
                    self.loaded_sounds[s] = pygame.mixer.Sound(sound_file)
                else:
                    print(f"⚠️ Missing sound: {sound_file}")


    def play_sound(self, sound_name, channel="question"):
        channel_map = {
            "question": self.channel_question,
            "answer": self.channel_answer,
            "feedback": self.channel_feedback
        }
        if sound_name in self.loaded_sounds:
            channel_map[channel].play(self.loaded_sounds[sound_name])
        else:
            print("⚠️ Sound not found:", sound_name)

    # ==============================
    # UI
    # ==============================
    def setup_ui(self):
        # Replay button (centered where the image was)
        self.replay_button = tk.Button(
            self.root, text="🔊 إعادة الصوت", font=("Arial", 28, "bold"),
            bg="#cce5ff", width=15, height=3, command=self.replay_sound
        )
        self.replay_button.pack(pady=100)  # adjust padding to center

        # Answer images frame (horizontal)
        self.answers_frame = tk.Frame(self.root, bg="#ffffff")
        self.answers_frame.pack(pady=50)

        # Navigation buttons
        nav_frame = tk.Frame(self.root, bg="white")
        nav_frame.pack(side="bottom", pady=20, fill="x")

        self.next_button = tk.Button(nav_frame, text="التالي ➡️", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.next_question_button)
        self.next_button.pack(side="left", padx=50)

        self.exit_button = tk.Button(nav_frame, text="⏪ إنهاء", font=("Arial", 20, "bold"),
                                     bg="#f8d7da", command=self.root.destroy)
        self.exit_button.pack(side="left", expand=True)

        self.prev_button = tk.Button(nav_frame, text="⬅️ السابق", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.prev_question_button)
        self.prev_button.pack(side="right", padx=50)

    # ==============================
    # NAVIGATION
    # ==============================
    def next_question_button(self):
        if self.current_index < len(QUESTIONS) - 1:
            self.current_index += 1
            self.show_question()

    def prev_question_button(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_question()

    # ==============================
    # QUIZ LOGIC
    # ==============================
    def show_question(self):
        q = QUESTIONS[self.current_index]

        # Update answer buttons as images
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        self.option_buttons = []
        option_width, option_height = q.get("option_size", (200, 200))
        for i, img_file in enumerate(q["options"]):
            img_path = os.path.join(IMG_PATH, img_file)
            try:
                img = Image.open(img_path)
                img = img.resize((option_width, option_height))
                photo = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                photo = None
                print("⚠️ Missing answer image:", img_file)

            btn = tk.Button(self.answers_frame, image=photo, bd=2,
                            command=lambda i=i: self.play_answer_sound(i))
            btn.image = photo  # keep reference
            btn.pack(side="left", padx=20)
            self.option_buttons.append(btn)

        # Re-enable input
        self.buttons_disabled = False

        # Play question sound
        self.play_sound(q["sound"], "question")

        # Show/hide previous button
        if self.current_index == 0:
            self.prev_button.pack_forget()
        else:
            self.prev_button.pack(side="right", padx=50)

        # Disable next button on last question
        if self.current_index == len(QUESTIONS) - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")

    def play_answer_sound(self, index):
        if self.buttons_disabled:
            return
        self.buttons_disabled = True
        q = QUESTIONS[self.current_index]
        self.play_sound(q["answer_sounds"][index], "answer")
        self.root.after(1500, lambda: self.check_answer(index))

    def check_answer(self, index):
        q = QUESTIONS[self.current_index]
        if index == q["answer"]:
            self.score += 1
            self.play_sound("correct.wav", "feedback")
        else:
            self.play_sound("wrong.wav", "feedback")
        self.buttons_disabled = False  # allow next attempt

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
