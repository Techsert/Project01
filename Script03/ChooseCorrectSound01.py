import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import random
import os
import time

# ==============================
# CONFIG
# ==============================

# Dynamically find path one folder back from the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "../assets")

IMG_PATH = os.path.join(ASSET_PATH, "img/whatisthis")
SOUND_PATH = os.path.join(ASSET_PATH, "sounds/whatIsThis")


# Example questions (replace with your full list)
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
# CLASS
# ==============================

class WhatIsThis:
    def __init__(self, root):
        self.root = root
        self.root.title("ما هذا؟ 🧠")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#ffffff")

        # --- Flags and state ---
        self.buttons_disabled = False
        self.current_index = 0
        self.score = 0

        # --- Init pygame for sound ---
        pygame.mixer.init()
        self.channel_question = pygame.mixer.Channel(0)
        self.channel_answer = pygame.mixer.Channel(1)
        self.channel_feedback = pygame.mixer.Channel(2)

        # --- Load all sounds ---
        self.loaded_sounds = {}
        self.preload_sounds(QUESTIONS)

        # --- Background Image ---
        self.bg_image = None
        self.setup_background(os.path.join(IMG_PATH, "bg-tr.png"))

        # --- UI setup ---
        self.setup_ui()

        # --- Escape key to exit fullscreen and stop all sounds ---
        self.root.bind("<Escape>", self.exit_fullscreen_stop_sounds)

        # --- Start the quiz ---
        self.show_question()



    # ==============================
    # BACKGROUND IMAGE
    # ==============================
    def setup_background(self, path):
        try:
            img = Image.open(path)
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            img = img.resize((screen_w, screen_h))
            self.bg_image = ImageTk.PhotoImage(img)
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("⚠️ Background image not found:", path)

    # ==============================
    # ESCAPE HANDLER
    # ==============================
    def exit_fullscreen_stop_sounds(self, event=None):
        self.root.attributes('-fullscreen', False)
        pygame.mixer.stop()

    # ==============================
    # SOUND FUNCTIONS
    # ==============================

    def preload_sounds(self, questions):
        for q in questions:
            paths = [q["sound"]] + q["answer_sounds"]
            for s in paths:
                sound_file = os.path.join(SOUND_PATH, s)
                if os.path.exists(sound_file):
                    self.loaded_sounds[s] = pygame.mixer.Sound(sound_file)
                else:
                    print(f"⚠️ Missing sound: {s}")

    def play_sound(self, sound_name, channel="question"):
        """Centralized sound playback with channels"""
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
    # UI SETUP
    # ==============================

    def setup_ui(self):
        # Title
        self.title_label = tk.Label(
            self.root, text="🎯 اِختَر الكَلِمَةُ الصَحيحَة 🎯",
            font=("Arial", 36, "bold"), fg="#333", bg="white"
        )
        self.title_label.pack(pady=30)

        # Image display
        self.image_label = tk.Label(self.root, bg="white")
        self.image_label.pack(pady=20)

        # Options container
        self.buttons_frame = tk.Frame(self.root, bg="white")
        self.buttons_frame.pack(pady=20)

        # Buttons placeholders
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=12,
                height=2,
                bg="#ffccff",
                activebackground="#ff99ff",
                command=lambda i=i: self.play_answer_sound(i)
            )
            btn.grid(row=i // 2, column=i % 2, padx=30, pady=20)
            self.option_buttons.append(btn)

        # Replay / Exit buttons (old)
        self.replay_button = tk.Button(
            self.root, text="🔊 إعادة الصوت", font=("Arial", 20, "bold"),
            bg="#cce5ff", command=self.replay_sound
        )
        self.replay_button.pack(pady=10)

        # =========================
        # Bottom Navigation Buttons
        # =========================
        nav_frame = tk.Frame(self.root, bg="white")
        nav_frame.pack(side="bottom", pady=20, fill="x")

        # Next button → left
        self.next_button = tk.Button(
            nav_frame, text="التالي ➡️", font=("Arial", 20, "bold"),
            bg="#cce5ff", command=self.next_question_button
        )
        self.next_button.pack(side="left", padx=50)

        # Exit button → center
        self.exit_button = tk.Button(
            nav_frame, text="⏪ إنهاء", font=("Arial", 20, "bold"),
            bg="#f8d7da", command=self.root.destroy
        )
        self.exit_button.pack(side="left", expand=True)

        # Previous button → right
        self.prev_button = tk.Button(
            nav_frame, text="⬅️ السابق", font=("Arial", 20, "bold"),
            bg="#cce5ff", command=self.prev_question_button
        )
        self.prev_button.pack(side="right", padx=50)

    # ==============================
    # Navigation button callbacks
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
    # GAME LOGIC
    # ==============================

    def show_question(self):
        q = QUESTIONS[self.current_index]

        # Update image
        try:
            img = Image.open(os.path.join(IMG_PATH, q["image"]))
            img = img.resize((400, 400))
            self.current_photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_photo)
        except FileNotFoundError:
            print("⚠️ Missing image:", q["image"])
            self.image_label.config(image="", text="⚠️ Missing Image ⚠️")

        # Update buttons
        for i, btn in enumerate(self.option_buttons):
            btn.config(text=q["options"][i], state="normal", bg="#ffccff")

        # Play question sound
        self.play_sound(q["sound"], "question")

        # Re-enable input
        self.buttons_disabled = False

    def play_answer_sound(self, index):
        if self.buttons_disabled:
            return
        self.buttons_disabled = True

        q = QUESTIONS[self.current_index]
        self.play_sound(q["answer_sounds"][index], "answer")

        # Wait a bit, then check answer
        self.root.after(1500, lambda: self.check_answer(index))

    def check_answer(self, index):
        q = QUESTIONS[self.current_index]
        if index == q["answer"]:
            self.score += 1
            self.play_sound("correct.wav", "feedback")
            self.show_feedback(True)
        else:
            self.play_sound("wrong.wav", "feedback")
            self.show_feedback(False)

    def show_feedback(self, correct):
        popup = self.make_popup("🎉 نتيجة 🎉", 400, 300, "#e6f7ff")
        msg = "إجابة صحيحة! 🌟" if correct else "إجابة خاطئة ❌"
        lbl = tk.Label(popup, text=msg, font=("Arial", 28, "bold"), bg="#e6f7ff")
        lbl.pack(expand=True, pady=50)
        popup.after(1500, lambda: self.next_question(popup))

    def next_question(self, popup):
        popup.destroy()
        self.current_index += 1
        if self.current_index >= len(QUESTIONS):
            self.show_final_result()
        else:
            self.show_question()

    def show_final_result(self):
        popup = self.make_popup("🏁 النتيجة النهائية 🏁", 500, 400, "#e6ffe6")
        msg = f"أحسنت! نتيجتك: {self.score} من {len(QUESTIONS)}"
        lbl = tk.Label(popup, text=msg, font=("Arial", 28, "bold"), bg="#e6ffe6")
        lbl.pack(expand=True, pady=50)

        tk.Button(
            popup, text="🔁 إعادة اللعب", font=("Arial", 20, "bold"),
            bg="#cce5ff", command=lambda: [popup.destroy(), self.restart()]
        ).pack(pady=10)

        tk.Button(
            popup, text="⏪ رجوع", font=("Arial", 20, "bold"),
            bg="#f8d7da", command=self.root.destroy
        ).pack(pady=10)

    def restart(self):
        self.current_index = 0
        self.score = 0
        self.show_question()

    def replay_sound(self):
        q = QUESTIONS[self.current_index]
        self.play_sound(q["sound"], "question")

    # ==============================
    # POPUP HELPER
    # ==============================

    def make_popup(self, title, width, height, bg):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg=bg)
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        popup.transient(self.root)
        popup.grab_set()
        popup.focus_force()
        return popup


# ==============================
# RUN APP
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatIsThis(root)
    root.mainloop()
