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
        "option_size": (200, 200)
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
        self.root.configure(bg="white")

        # State
        self.current_index = 0
        self.buttons_disabled = False
        self.score = 0

        # Init pygame
        pygame.mixer.init()
        self.channel_question = pygame.mixer.Channel(0)
        self.channel_feedback = pygame.mixer.Channel(1)

        # Preload sounds
        self.loaded_sounds = {}
        self.preload_sounds(QUESTIONS)

        # ✅ Add background image
        self.bg_label = None
        self.set_background()

        # Setup UI
        self.setup_ui()

        # Escape key
        self.root.bind("<Escape>", self.exit_fullscreen_stop_sounds)

        # Start quiz
        self.show_question()

    # ==============================
    # BACKGROUND
    # ==============================
    def set_background(self):
        bg_path = os.path.join(IMG_PATH, "background.png")  # ✅ your background image file
        if not os.path.exists(bg_path):
            print(f"⚠️ Background not found: {bg_path}")
            return

        bg_img = Image.open(bg_path)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        bg_img = bg_img.resize((screen_w, screen_h))
        self.bg_photo = ImageTk.PhotoImage(bg_img)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

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
        ch = self.channel_question if channel == "question" else self.channel_feedback
        if sound_name in self.loaded_sounds:
            ch.play(self.loaded_sounds[sound_name])
        else:
            print("⚠️ Sound not found:", sound_name)

    # ==============================
    # UI
    # ==============================
    def setup_ui(self):
        # ✅ Make frames appear above background
        self.replay_button = tk.Button(
            self.root, text="🔊 إعادة الصوت", font=("Arial", 28, "bold"),
            bg="#cce5ff", width=15, height=3, command=self.replay_sound
        )
        self.replay_button.pack(pady=100)

        self.answers_frame = tk.Frame(self.root, bg="#ffffff")
        self.answers_frame.pack(pady=50)

        nav_frame = tk.Frame(self.root, bg="white")
        nav_frame.pack(side="bottom", pady=20, fill="x")

        self.prev_button = tk.Button(nav_frame, text="⬅️ السابق", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.prev_question_button)
        self.prev_button.pack(side="right", padx=10)

        self.exit_button = tk.Button(nav_frame, text="⏪ إنهاء", font=("Arial", 20, "bold"),
                                     bg="#f8d7da", command=self.root.destroy)
        self.exit_button.pack(side="left", expand=True)

        self.next_button = tk.Button(nav_frame, text="التالي ➡️", font=("Arial", 20, "bold"),
                                     bg="#cce5ff", command=self.next_question_button)
        self.next_button.pack(side="left", padx=10)

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
    # FEEDBACK
    # ==============================
    def show_feedback(self, is_correct=True):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.config(bg="pink")
        popup.wm_attributes('-transparentcolor', 'pink')

        w, h = 840, 810
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        image_path = os.path.join(IMG_PATH, "thumbsup.png" if is_correct else "thumbsdown.png")
        if not os.path.exists(image_path):
            print("⚠️ Image not found:", image_path)
            return

        img = Image.open(image_path).resize((w, h))
        photo = ImageTk.PhotoImage(img)

        label_img = tk.Label(popup, image=photo, bg="pink", borderwidth=0, highlightthickness=0)
        label_img.image = photo
        label_img.pack(fill="both", expand=True)

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

        label_img.bind("<Button-1>", close_popup)
        auto_close_id = popup.after(3000, close_popup)  # show 3 seconds

    # ==============================
    # QUIZ LOGIC
    # ==============================
    def show_question(self):
        q = QUESTIONS[self.current_index]
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        option_width, option_height = q.get("option_size", (200, 200))
        for i, img_file in enumerate(q["options"]):
            img_path = os.path.join(IMG_PATH, img_file)
            if not os.path.exists(img_path):
                print("⚠️ Missing:", img_path)
                continue

            img = Image.open(img_path).resize((option_width, option_height))
            photo = ImageTk.PhotoImage(img)
            btn = tk.Button(self.answers_frame, image=photo, bd=2,
                            command=lambda i=i: self.check_answer(i))
            btn.image = photo
            btn.pack(side="left", padx=20)

        self.buttons_disabled = False
        self.play_sound(q["sound"], "question")

        # Navigation state
        self.prev_button.config(state="normal" if self.current_index > 0 else "disabled")
        self.next_button.config(state="normal" if self.current_index < len(QUESTIONS) - 1 else "disabled")

    def check_answer(self, index):
        q = QUESTIONS[self.current_index]
        if index == q["answer"]:
            self.score += 1
            self.show_feedback(True)
        else:
            self.show_feedback(False)

    def replay_sound(self):
        q = QUESTIONS[self.current_index]
        self.play_sound(q["sound"], "question")

    def show_final_result(self):
        popup = tk.Toplevel(self.root)
        popup.title("🏁 النتيجة النهائية 🏁")
        popup.geometry("500x400")
        popup.configure(bg="#e6ffe6")

        msg = f"أحسنت! نتيجتك: {self.score} من {len(QUESTIONS)}"
        lbl = tk.Label(popup, text=msg, font=("Arial", 28, "bold"), bg="#e6ffe6")
        lbl.pack(expand=True, pady=50)

        tk.Button(popup, text="🔁 إعادة اللعب", font=("Arial", 20, "bold"),
                  bg="#cce5ff", command=lambda: [popup.destroy(), self.restart()]).pack(pady=10)

        tk.Button(popup, text="⏪ إنهاء", font=("Arial", 20, "bold"),
                  bg="#f8d7da", command=self.root.destroy).pack(pady=10)

    def restart(self):
        self.current_index = 0
        self.score = 0
        self.show_question()

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
