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
        "options": ["01alef.png", "02ba.png", "03ta.png", "04tha.png"],
        "answer": 0,
        "option_size": (200, 200),
        "difficulty": "easy"
    },
    {
        "sound": "02ba-s.wav",
        "options": ["01alef-f.png", "01alef-k.png", "01alef-d.png", "01alef.png"],
        "answer": 0,
        "option_size": (250, 250),
        "difficulty": "hard"
    },
    {
        "sound": "01alef-s.wav",
        "options": ["01alef.png", "02ba.png", "03ta.png", "04tha.png"],
        "answer": 0,
        "option_size": (200, 200),
        "difficulty": "medium"
    },
    {
        "sound": "02ba-s.wav",
        "options": ["01alef-f.png", "01alef-k.png", "01alef-d.png", "01alef.png"],
        "answer": 0,
        "option_size": (250, 250),
        "difficulty": "hard"
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

        # Welcome Screen
        self.show_welcome_screen()

        # Start game
        #self.show_question()

        # Difficulty State
        self.selected_difficulty = None  # Will be set from welcome screen

        
    @property
    def filtered_questions(self):
        return [q for q in QUESTIONS if q.get("difficulty") == self.selected_difficulty]

    # ==============================
    # Welcome Screen
    # ==============================
    def show_welcome_screen(self):
        self.clear_screen()

        # === Full Background ===
        bg_path = os.path.join(IMG_PATH, "background.png")
        try:
            bg_image = Image.open(bg_path).resize(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
            )
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_photo, borderwidth=0)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("⚠️ Missing background image:", bg_path)
            self.root.configure(bg="black")  # fallback

        # === Title Label ===
        title_label = tk.Label(
            self.root,
            text="اختر المستوى",
            font=("Arial", 48, "bold"),
            fg="#ffffff",         # white text
            bg="#000000",         # use black or match background image tone
            borderwidth=0,
            highlightthickness=0
        )
        title_label.place(relx=0.5, rely=0.15, anchor="center")

        # === Difficulty Images as Buttons ===
        difficulties = ["easy", "medium", "hard"]
        self.difficulty_photos = {}
        positions = [0.3, 0.5, 0.7]

        for idx, level in enumerate(difficulties):
            img_path = os.path.join(IMG_PATH, f"{level}.png")
            try:
                img = Image.open(img_path).resize((350, 550))  # adjust size if needed
                photo = ImageTk.PhotoImage(img)
                self.difficulty_photos[level] = photo

                btn = tk.Label(
                    self.root,
                    image=photo,
                    borderwidth=0,
                    highlightthickness=0,
                    bg="#000000",  # match background (no white halo)
                    cursor="hand2"
                )
                btn.place(relx=positions[idx], rely=0.55, anchor="center")

                # Bind click event
                btn.bind("<Button-1>", lambda e, lvl=level: self.select_difficulty(lvl))

            except FileNotFoundError:
                print(f"⚠️ Missing difficulty image: {img_path}")



    # ==============================
    # Start Game with Selected Difficulty
    # ==============================
    
    def start_game(self):
        # self.selected_difficulty is already set by select_difficulty()
        if not self.selected_difficulty:
            print("⚠️ No difficulty selected!")
            return

        if not self.filtered_questions:
            from tkinter import messagebox
            messagebox.showwarning("⚠️ لا توجد أسئلة", "لا توجد أسئلة في هذا المستوى بعد.")
            return

        self.current_index = 0
        self.score = 0

        # Rebuild the main game interface after clearing welcome screen
        self.clear_screen()
        self.setup_ui()

        # Show the first question
        self.show_question()

    
    # ==============================
    # Centralized Screen Clearing
    # ==============================
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==============================
    # SOUND
    # ==============================
    def preload_sounds(self):
        sounds_to_load = ["correct.wav", "wrong.wav", "welcome.wav"]
        for q in QUESTIONS:
            sounds_to_load.append(q["sound"])

        for s in sounds_to_load:
            sound_file = os.path.join(SOUND_PATH, s)
            if os.path.exists(sound_file):
                self.loaded_sounds[s] = pygame.mixer.Sound(sound_file)
            else:
                print(f"⚠️ Missing sound file: {sound_file}")


    # ==============================
    # PLAY SOUND (ADDED FUNCTION)
    # ==============================
    def play_sound(self, filename, channel_type="question"):
        """Play a sound by name using the correct channel."""
        sound = self.loaded_sounds.get(filename)
        if not sound:
            print(f"⚠️ Sound not found: {filename}")
            return

        if channel_type == "question":
            self.channel_question.stop()
            self.channel_question.play(sound)
        elif channel_type == "feedback":
            self.channel_feedback.stop()
            self.channel_feedback.play(sound)


    # ==============================
    # UI SETUP
    # ==============================
    def setup_ui(self):
        # Background image
        bg_path = os.path.join(IMG_PATH, "background.png")
        try:
            bg_image = Image.open(bg_path).resize((self.root.winfo_screenwidth(),
                                                   self.root.winfo_screenheight()))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("⚠️ Missing background image:", bg_path)

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
        q = self.filtered_questions[self.current_index]

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

        q = self.filtered_questions[self.current_index]
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

        msg = f"لقد حصلت على {self.score} من {len(self.filtered_questions)} 🎉"

        self.next_button.config(state="normal" if self.current_index < len(self.filtered_questions) - 1 else "disabled")
        tk.Label(popup, text=msg, font=("Arial", 28, "bold"), bg="#e6ffe6").pack(expand=True, pady=50)

        tk.Button(popup, text="🔁 إعادة اللعب", font=("Arial", 20, "bold"),
                  bg="#cce5ff", command=lambda: [popup.destroy(), self.restart()]).pack(pady=10)

        tk.Button(popup, text="⏪ إنهاء", font=("Arial", 20, "bold"),
                  bg="#f8d7da", command=self.root.destroy).pack(pady=10)
        
        tk.Button(popup, text="🏠 العودة إلى القائمة", font=("Arial", 20, "bold"),
          bg="#fff3cd", command=lambda: [popup.destroy(), self.show_welcome_screen()]).pack(pady=10)

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
        q = self.filtered_questions[self.current_index]
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
