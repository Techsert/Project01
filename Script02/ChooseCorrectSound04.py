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
        self.root.configure(bg="white")

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
    # Feedback
    # ==============================
    def show_feedback(self, is_correct=True):
        # Create popup
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        # Transparent background (Windows workaround)
        popup.config(bg="pink")
        popup.wm_attributes('-transparentcolor', 'pink')

        w, h = 400, 400  # size of feedback popup
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        # Feedback image
        image_path = "../assets/img/whatisthis/thumbsup.png" if is_correct else "../assets/img/whatisthis/thumbsdown.png"
        if not os.path.exists(image_path):
            print("⚠️ Image not found:", image_path)
            return

        img = Image.open(image_path).resize((w, h))
        photo = ImageTk.PhotoImage(img)

        label_img = tk.Label(popup, image=photo, bg="pink", borderwidth=0, highlightthickness=0)
        label_img.image = photo  # keep reference
        label_img.pack(fill="both", expand=True)

        # Play corresponding sound immediately
        sound_file = "../assets/sounds/whatIsThis/correct.wav" if is_correct else "../assets/sounds/whatIsThis/wrong.wav"
        if os.path.exists(sound_file):
            pygame.mixer.Sound(sound_file).play()

        # Close popup on click or after 1.5s
        def close_popup(event=None):
            try:
                popup.after_cancel(auto_close_id)
            except:
                pass
            popup.destroy()
            self.buttons_disabled = False
            self.current_index += 1  # move to next question

            if self.current_index < len(QUESTIONS):
                self.show_question()  # show next question
            else:
                self.show_final_result()  # show final result popup instead


        label_img.bind("<Button-1>", close_popup)
        auto_close_id = popup.after(1500, close_popup)


    def close_popup(event=None):
        try:
            popup.after_cancel(auto_close_id)
        except:
            pass
        popup.destroy()
        self.buttons_disabled = False
        self.current_index += 1

        if self.current_index < len(QUESTIONS):
            self.show_question()
        else:
            self.show_final_result()  # Make sure this method exists



    def next_question(self):
        if self.current_index < len(QUESTIONS):
            q = QUESTIONS[self.current_index]
            # Update your question UI here
            self.show_question()
        else:
            self.show_final_result()

    def restart(self):
        """Reset the quiz and start from the first question."""
        self.current_index = 0
        self.score = 0
        # Show the first question again
        self.show_question()





##    def close_feedback_and_continue(self, popup):
##        popup.destroy()
##        self.buttons_disabled = False  # Re-enable buttons
##        self.q_index += 1
##        self.next_question()

##    def fade_in(self, widget):
##        widget.after(100, lambda: widget.config(fg="#000000"))

##    def next_question(self):
##        if self.q_index < len(questions):
##            q = questions[self.q_index]
##            self.question_label.config(text=q["question"], fg="#ffffff")
##            self.fade_in(self.question_label)
##
##            for i, choice in enumerate(q["choices"]):
##                self.buttons[i].config(text=choice)
##
##            img = Image.open(f"../assets/img/whatisthis/{q['image']}")
##            img = img.resize((850, 800))
##            self.photo = ImageTk.PhotoImage(img)
##            self.image_label.config(image=self.photo)
##            self.image_label.image = self.photo
##
##            self.progress_label.config(text=f"السؤال {self.q_index + 1} من {len(questions)} | النتيجة: {self.score}")
##
##            # 🔊 Play question narration from question["sound"]
##            sound_file = f"../assets/sounds/whatIsThis/{q['sound']}"
##            pygame.mixer.Sound(sound_file).play()
##        else:
##            self.show_final_result()
            

    def show_final_result(self):
        popup = tk.Toplevel(self.root)
        popup.title("🏁 النتيجة النهائية 🏁")
        popup.geometry("500x400")
        popup.configure(bg="#e6ffe6")

        msg = f"أحسنت! نتيجتك: {self.score} من {len(QUESTIONS)}"
        lbl = tk.Label(popup, text=msg, font=("Arial", 28, "bold"), bg="#e6ffe6")
        lbl.pack(expand=True, pady=50)

        tk.Button(
            popup, text="🔁 إعادة اللعب", font=("Arial", 20, "bold"),
            bg="#cce5ff", command=lambda: [popup.destroy(), self.restart()]
        ).pack(pady=10)

        tk.Button(
            popup, text="⏪ إنهاء", font=("Arial", 20, "bold"),
            bg="#f8d7da", command=self.root.destroy
        ).pack(pady=10)



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
        """Handle answer click without playing sound"""
        if self.buttons_disabled:
            return
        self.buttons_disabled = True

        # Immediately check answer instead of waiting
        self.check_answer(index)

    def check_answer(self, index):
        """Check correctness and show feedback popup"""
        q = QUESTIONS[self.current_index]
        if index == q["answer"]:
            self.score += 1
            self.show_feedback(True)
        else:
            self.show_feedback(False)

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
