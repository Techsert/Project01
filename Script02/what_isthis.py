import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame  # 🎵 Sound engine
import os

# 🎵 Sound Effects Setup
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("../assets/sounds/whatIsThis/correct.wav")
wrong_sound = pygame.mixer.Sound("../assets/sounds/whatIsThis/wrong.mp3")

def play_correct():
    correct_sound.play()

def play_wrong():
    wrong_sound.play()

class WhatIsThis:
    def __init__(self, root):
        self.root = root
        self.root.title("Kids' words Quiz Game 🎉")
        self.root.attributes('-fullscreen', True)

        self.buttons_disabled = False

        # 🖼️ Background
        bg_image = Image.open("../assets/img/whatisthis/cartoon_bg.png")
        self.bg_photo = ImageTk.PhotoImage(bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight())))
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.score = 0
        self.q_index = 0
        random.shuffle(questions)

        # 🧩 Main container
        self.main_frame = tk.Frame(root, bg="#ffffff", bd=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1900, height=990)

        # 🖼️ Image section
        self.image_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=5, relief="groove")
        self.image_frame.place(x=50, y=30, width=900, height=850)

        self.image_label = tk.Label(self.image_frame, bg="#ffffff")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        # 📋 Question section
        self.qa_frame = tk.Frame(self.main_frame, bg="#ffffff", bd=5, relief="ridge")
        self.qa_frame.place(x=950, y=30, width=900, height=850)

        self.qa_inner = tk.Frame(self.qa_frame, bg="#ffffff")
        self.qa_inner.place(relx=0.5, rely=0.5, anchor="center")

        self.question_label = tk.Label(
            self.qa_inner,
            text="",
            font=("Scheherazade", 80, "bold"),
            wraplength=750,
            bg="#ffffff",
            justify="right",
            anchor="e"
        )
        self.question_label.pack(pady=(0, 2), fill="x")

        # 🔁 Replay button
        self.replay_button = tk.Button(
            self.qa_inner,
            text="🔁 إعادة تشغيل الصوت",
            font=("Scheherazade", 12),
            bg="#ccffcc",
            command=self.replay_question_sound
        )
        self.replay_button.pack(pady=(2, 0))

        # 🧠 Answer buttons with sound buttons
        self.answer_frames = []
        self.buttons = []
        self.sound_buttons = []
        for i in range(4):
            frame = tk.Frame(self.qa_inner, bg="#ffffff")
            frame.pack(pady=10)

            btn = tk.Button(
                frame,
                text="",
                font=("Scheherazade", 30, "bold"),
                width=25,
                bg="#ffccff",
                command=lambda i=i: self.check_answer(i)
            )
            btn.pack(side="right", padx=(5, 0))
            self.buttons.append(btn)

            sound_btn = tk.Button(
                frame,
                text="🔊",
                font=("Scheherazade", 12),
                bg="#ccffcc",
                command=lambda i=i: self.play_answer_sound(i)
            )
            sound_btn.pack(side="right")
            self.sound_buttons.append(sound_btn)

            self.answer_frames.append(frame)

        # 📊 Progress Tracker
        self.progress_label = tk.Label(
            self.main_frame,
            text="",
            font=("Scheherazade", 28, "bold"),  # ← larger and bold
            bg="#f0f0f0",
            fg="#333333",
            bd=2,
            relief="ridge",
            padx=5,
            pady=5
        )
        self.progress_label.place(relx=0.5, rely=0.95, anchor="center")

        self.next_question()

        # 🔙 Escape key to exit fullscreen
        root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))


    def show_feedback(self, title, message, is_correct=True):
        # Create popup
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)

        # Transparent background workaround (Windows)
        popup.config(bg="pink")
        popup.wm_attributes('-transparentcolor', 'pink')

        w, h = 400, 400
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        # Load image
        image_path = "../assets/img/whatisthis/correct.png" if is_correct else "../assets/img/whatisthis/wrong.png"
        if not os.path.exists(image_path):
            print("⚠️ Image not found:", image_path)
            return

        img = Image.open(image_path).resize((w, h))
        photo = ImageTk.PhotoImage(img)

        label_img = tk.Label(popup, image=photo, bg="pink", borderwidth=0, highlightthickness=0)
        label_img.image = photo  # keep reference
        label_img.pack(fill="both", expand=True)

        # Auto-close popup and continue
        popup.after(10000, lambda: self.close_feedback_and_continue(popup))



    def close_feedback_and_continue(self, popup):
        popup.destroy()
        self.buttons_disabled = False  # Re-enable buttons
        self.q_index += 1
        self.next_question()

    def fade_in(self, widget):
        widget.after(100, lambda: widget.config(fg="#000000"))

    def next_question(self):
        if self.q_index < len(questions):
            q = questions[self.q_index]
            self.question_label.config(text=q["question"], fg="#ffffff")
            self.fade_in(self.question_label)

            for i, choice in enumerate(q["choices"]):
                self.buttons[i].config(text=choice)

            img = Image.open(f"../assets/img/whatisthis/{q['image']}")
            img = img.resize((850, 800))
            self.photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

            self.progress_label.config(text=f"السؤال {self.q_index + 1} من {len(questions)} | النتيجة: {self.score}")

            # 🔊 Play question narration from question["sound"]
            sound_file = f"../assets/sounds/whatIsThis/{q['sound']}"
            pygame.mixer.Sound(sound_file).play()
        else:
            self.show_final_result()

    def show_final_result(self):
        popup = tk.Toplevel(self.root)
        popup.title("نتيجة اللعبة")

        # 📐 Size and centering
        w, h = 700, 700
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (w // 2)
        y = (popup.winfo_screenheight() // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.configure(bg="#e6f7ff")
        popup.transient(self.root)
        popup.grab_set()

        # 🏆 Praise based on performance
        percentage = self.score / len(questions)
        if percentage >= 0.9:
            praise = "🌟 ممتاز!"
        elif percentage >= 0.7:
            praise = "👍 جيد جدًا!"
        elif percentage >= 0.5:
            praise = "🙂 جيد!"
        else:
            praise = "💪 حاول مرة أخرى!"

        # 📝 Save to leaderboard
        try:
            with open("leaderboard.txt", "a", encoding="utf-8") as f:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - Score: {self.score}/{len(questions)}\n")
        except Exception as e:
            print("Failed to save leaderboard:", e)

        # 🎉 Emoji header
        emoji_label = tk.Label(
            popup,
            text="🎉",
            font=("Arial", 80),
            bg="#e6f7ff"
        )
        emoji_label.pack(pady=(30, 0))

        # 🧠 Score message
        label = tk.Label(
            popup,
            text=f"{praise}\nلقد حصلت على {self.score} من {len(questions)}!",
            font=("Scheherazade", 40, "bold"),
            bg="#e6f7ff",
            fg="#003366",
            wraplength=500,
            justify="center"
        )
        label.pack(pady=(10, 30))

        # 🔁 Play Again button
        play_again_btn = tk.Button(
            popup,
            text="🔁 إعادة اللعب",
            font=("Scheherazade", 18, "bold"),
            bg="#ccffcc",
            activebackground="#b3ffb3",
            command=lambda: self.restart_game(popup)
        )
        play_again_btn.pack(pady=10)

        # ❌ Exit button
        exit_btn = tk.Button(
            popup,
            text="إنهاء",
            font=("Scheherazade", 18, "bold"),
            bg="#ffffff",
            activebackground="#f2f2f2",
            command=self.root.destroy
        )
        exit_btn.pack(pady=10)


    def restart_game(self, popup):
        popup.destroy()
        self.score = 0
        self.q_index = 0
        random.shuffle(questions)
        self.next_question()

    def replay_question_sound(self):
        sound_file = f"../assets/sounds/whatIsThis/{questions[self.q_index]['sound']}"
        pygame.mixer.Sound(sound_file).play()

    def play_answer_sound(self, index):
        if self.buttons_disabled:
            return  # Optional: prevent replay while in feedback
        pygame.mixer.stop()  # Stop any previous sound
        sound_file = f"../assets/sounds/whatIsThis/{questions[self.q_index]['answer_sounds'][index]}"
        pygame.mixer.Sound(sound_file).play()


    def check_answer(self, choice_index):
        if self.buttons_disabled:
            return  # Ignore clicks while feedback is showing
        self.buttons_disabled = True  # Disable further clicks

        q = questions[self.q_index]
        selected = q["choices"][choice_index]

        # 🔊 Play chosen answer sound first
        answer_sound = f"../assets/sounds/whatIsThis/{q['answer_sounds'][choice_index]}"
        pygame.mixer.stop()  # Stop any previous sound
        pygame.mixer.Sound(answer_sound).play()

        # ⏱️ Delay before playing correct/wrong sound
        self.root.after(2500, lambda: self.evaluate_answer(selected, q["answer"]))


    def evaluate_answer(self, selected, correct_answer):
        if selected == correct_answer:
            self.score += 1
            play_correct()
            self.show_feedback("صحيح!", "! أحسنت ✅", is_correct=True)
        else:
            play_wrong()
            self.show_feedback("خطأ", f"الإجابة الصحيحة هي ❌:\n{correct_answer}", is_correct=False)
    

# 🧠 Quiz data with embedded sound filenames
questions = [
    {
        "question": "السَّلَامُ عَلَيْكُم",
        "choices": ["إِسْمِي يُوسُف", "وَعَلَيْكُمُ السَّلَام", "بِخَيْر الْحَمْدُ لِلَّه", "كَيْفَ حَالُكَ"],
        "answer": "وَعَلَيْكُمُ السَّلَام",
        "image": "salam.png",
        "sound": "Salam.wav",
        "answer_sounds": ["myNameIsYusuf.wav", "salamAnswer.wav", "fineThankYou.wav", "howAreYou.wav"]
    },
    {
        "question": "كَيْفَ حَالُكَ؟",
        "choices": ["بِخَيْر الْحَمْدُ لِلَّه", "كَيْفَ حَالُكَ", "إِسْمِي يُوسُف", "وَعَلَيْكُمُ السَّلَام"],
        "answer": "بِخَيْر الْحَمْدُ لِلَّه",
        "image": "howAreYou.png",
        "sound": "howAreYou.wav",
        "answer_sounds": ["fineThankYou.wav", "howAreYou.wav", "myNameIsYusuf.wav", "salamAnswer.wav"]
    },
    {
        "question": "مَا إِسْمُكَ؟",
        "choices": ["كَيْفَ حَالُكَ", "وَعَلَيْكُمُ السَّلَام", "إِسْمِي يُوسُف", "بِخَيْر الْحَمْدُ لِلَّه"],
        "answer": "إِسْمِي يُوسُف",
        "image": "whatIsYourName.png",
        "sound": "whatIsYourName.wav",
        "answer_sounds": ["howAreYou.wav", "salamAnswer.wav", "myNameIsYusuf.wav", "fineThankYou.wav"]
    },
    {
        "question": "كَمْ عُمْرُكَ؟",
        "choices": ["عُمْرِي ثَلاثُ سَنَوَاتٍ", "عُمْرِي سَبْعُ سَنَوَاتٍ", "عُمْرِي تِسْعُ سَنَوَاتٍ", "عُمْرِي خَمْسُ سَنَوَاتٍ"],
        "answer": "عُمْرِي سَبْعُ سَنَوَاتٍ",
        "image": "howOldAreYou.png",
        "sound": "howOldAreYou.wav",
        "answer_sounds": ["3yearsOld.wav", "7yearsOld.wav", "9YearsOld.wav", "5yearsOld.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا كِتَاب", "هَذَا قَلَم", "هَذَا مَسْجِد", "هَذَا بَيْت"],
        "answer": "هَذَا بَيْت",
        "image": "house.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["book.wav", "pen.wav", "masged.wav", "house.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا بَيْت", "هَذَا قَلَم", "هَذَا مَكْتَب", "هَذَا سَرِير"],
        "answer": "هَذَا قَلَم",
        "image": "pen.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["house.wav", "pen.wav", "desk.wav", "bed.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا كِتَاب", "هَذَا نَجْم", "هَذَا قَمِيص", "هَذَا بَاب"],
        "answer": "هَذَا قَمِيص",
        "image": "shirt.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["book.wav", "star.wav", "shirt.wav", "door.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا بَاب", "هَذَا كُرْسِي", "هَذَا مَكْتَب", "هَذَا سَرِير"],
        "answer": "هَذَا مَكْتَب",
        "image": "desk.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["door.wav", "chair.wav", "desk.wav", "bed.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا كِتَاب", "هَذَا مَسْجِد", "هَذَا بَاب", "هَذَا بَيْت"],
        "answer": "هَذَا مَسْجِد",
        "image": "masged.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["book.wav", "masged.wav", "door.wav", "house.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا بَيْت", "هَذَا قَلَم", "هَذَا مَكْتَب", "هَذَا نَجْم"],
        "answer": "هَذَا نَجْم",
        "image": "star.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["house.wav", "pen.wav", "desk.wav", "star.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا بَاب", "هَذَا شُبَّاك", "هَذَا قَمِيص", "هَذَا مَكْتَب"],
        "answer": "هَذَا بَاب",
        "image": "door.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["door.wav", "window.wav", "shirt.wav", "desk.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا مَسْجِد", "هَذَا قَلَم", "هَذَا كُرْسِي", "هَذَا سَرِير"],
        "answer": "هَذَا كُرْسِي",
        "image": "chair.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["masged.wav", "pen.wav", "chair.wav", "bed.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا كِتَاب", "هَذَا مِفْتَاح", "هَذَا مَسْجِد", "هَذَا بَيْت"],
        "answer": "هَذَا مِفْتَاح",
        "image": "key.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["book.wav", "key.wav", "masged.wav", "house.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا بَيْت", "هَذَا قَلَم", "هَذَا كُرْسِي", "هَذَا سَرِير"],
        "answer": "هَذَا سَرِير",
        "image": "bed.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["house.wav", "pen.wav", "chair.wav", "bed.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا كِتاب", "هَذَا مِفْتَاح", "هَذَا مَكْتَب", "هَذَا سَرِير"],
        "answer": "هَذَا كِتاب",
        "image": "book.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["book.wav", "key.wav", "desk.wav", "bed.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا بَاب", "هَذَا قَلَم", "هَذَا شُبَّاك", "هَذَا مَكْتَب"],
        "answer": "هَذَا شُبَّاك",
        "image": "window.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["door.wav", "pen.wav", "window.wav", "desk.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا أَسَد", "هَذَا أَرْنَب", "هَذَا جَمَل", "هَذَا ضِفْدَع"],
        "answer": "هَذَا أَسَد",
        "image": "lion.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["lion.wav", "rabbit.wav", "camel.wav", "frog.wav"]
    },
    {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا ثُعْبَان", "هَذِهِ ذُبَابَة", "هَذَا أَرْنَب", "هَذَا تِمْسَاح"],
        "answer": "هَذَا أَرْنَب",
        "image": "rabbit.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["snake.wav", "flies.wav", "rabbit.wav", "croc.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذِهِ بَقَرَة", "هَذِهِ شَجَرَة", "هَذِهِ قِطَّه", "هَذِهِ بَطَّه"],
        "answer": "هَذِهِ بَطَّه",
        "image": "duck.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["cow.wav", "tree.wav", "cat.wav", "duck.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذِهِ بَقَرَة", "هَذِهِ دَرَّاجَة", "هَذِهِ دَجَاجَة", "هَذِهِ رِيشَة"],
        "answer": "هَذِهِ بَقَرَة",
        "image": "cow.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["cow.wav", "bike.wav", "chicken.wav", "feather.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا ذِئْب", "هَذَا تِمْسَاح", "هَذَا طَاوُوس", "هَذَا صُرْصَار"],
        "answer": "هَذَا تِمْسَاح",
        "image": "croc.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["wolf.wav", "croc.wav", "peacock.mp3", "cockroach.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا عَنْكَبُوت", "هَذِهِ سَمَكَه", "هَذَا ثُعْبَان", "هَذَا راكون"],
        "answer": "هَذَا ثُعْبَان",
        "image": "snake.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["spider.wav", "fish.wav", "snake.wav", "raccoon.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا كَلْب", "هَذَا أَسَد", "هَذَا عَنْكَبُوت", "هَذَا جَمَل"],
        "answer": "هَذَا جَمَل",
        "image": "camel.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["dog.wav", "lion.wav", "spider.wav", "camel.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا حِصَان", "هَذَا راكون", "هَذَا أَسَد", "هَذَا غُرَاب"],
        "answer": "هَذَا حِصَان",
        "image": "horse.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["horse.wav", "raccoon.wav", "lion.wav", "craw.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا حِصَان", "هَذَا راكون", "هَذَا حِمار", "هَذَا غُرَاب"],
        "answer": "هَذَا حِمار",
        "image": "donkey.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["horse.wav", "raccoon.wav", "donkey.wav", "craw.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا أَسَد", "هَذَا خَرُوف", "هَذَا غُرَاب", "هَذِهِ دَرَّاجَة"],
        "answer": "هَذَا خَرُوف",
        "image": "sheep.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["lion.wav", "sheep.wav", "craw.wav", "bike.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا كَلْب", "هَذَا عَنْكَبُوت", "هَذَا دِيك", "هَذِهِ سَمَكَه"],
        "answer": "هَذَا دِيك",
        "image": "rooster.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["dog.wav", "spider.wav", "rooster.mp3", "fish.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذَا صَارُوخ", "هَذِهِ طَائِرَة", "هَذِهِ كُرَة", "هَذِهِ دَرَّاجَه"],
        "answer": "هَذِهِ دَرَّاجَه",
        "image": "bike.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["rocket.wav", "plane.wav", "ball.wav", "bike.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذِهِ دَجَاجَه", "هَذِهِ نَمْلَةٌ", "هَذِهِ ذُبَابَه", "هَذِهِ زَرَافَه"],
        "answer": "هَذِهِ دَجَاجَه",
        "image": "chicken.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["chicken.wav", "ant.wav", "flies.wav", "giraffe.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذِهِ زَرَافَه", "هَذَا ذِئْب", "هَذَا ثَعْلَب", "هَذِهِ دَجَاجَه"],
        "answer": "هَذَا ذِئْب",
        "image": "wolf.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["giraffe.wav", "wolf.wav", "fox.wav", "chicken.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذِهِ زَرَافَه", "هَذِهِ قِطَّه", "هَذِهِ ذُبَابَه", "هَذِهِ نَمْلَةٌ"],
        "answer": "هَذِهِ ذُبَابَه",
        "image": "flies.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["giraffe.wav", "cat.wav", "flies.wav", "ant.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذِهِ كُرَة", "هَذِهِ سَمَكَه", "هَذَا ذِئْب", "هَذِهِ رِيشَة"],
        "answer": "هَذِهِ رِيشَة",
        "image": "feather.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["ball.wav", "fish.wav", "wolf.wav", "feather.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا راكون", "هَذَا حِصَان", "هَذَا قَارِب", "هَذَا حِمار"],
        "answer": "هَذَا راكون",
        "image": "raccoon.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["raccoon.wav", "horse.wav", "boat.wav", "donkey.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذَا قِرْد", "هَذِهِ زَرَافَه", "هَذَا ثَعْلَب", "هَذَا صَارُوخ"],
        "answer": "هَذِهِ زَرَافَه",
        "image": "giraffe.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["monkey.wav", "giraffe.wav", "fox.wav", "rocket.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذِهِ كُرَة", "هَذَا حِمار", "هَذِهِ سَمَكَه", "هَذَا ذِئْب"],
        "answer": "هَذِهِ سَمَكَه",
        "image": "fish.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["ball.wav", "donkey.wav", "fish.wav", "wolf.wav"]
    },
        {
        "question": "مَا هَذِهِ؟",
        "choices": ["هَذِهِ كُرَة", "هَذَا قِرْد", "هَذَا ضِفْدَع", "هَذِهِ شَجَرَة"],
        "answer": "هَذِهِ شَجَرَة",
        "image": "tree.png",
        "sound": "whatIsThis.mp3",
        "answer_sounds": ["ball.wav", "monkey.wav", "frog.wav", "tree.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا صُرْصَار", "هَذِهِ نَمْلَةٌ", "هَذِهِ ذُبَابَه", "هَذَا ضِفْدَع"],
        "answer": "هَذَا صُرْصَار",
        "image": "cockroach.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["cockroach.wav", "ant.wav", "flies.wav", "frog.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذَا طَاوُوس", "هَذَا صَارُوخ", "هَذَا ذِئْب", "هَذَا عَنْكَبُوت"],
        "answer": "هَذَا صَارُوخ",
        "image": "rocket.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["peacock.mp3", "rocket.wav", "wolf.wav", "spider.wav"]
    },
        {
        "question": "مَا هَذَا؟",
        "choices": ["هَذِهِ زَرَافَه", "هَذَا حِمار", "هَذَا صُنْدُوق", "هَذَا ثَعْلَب"],
        "answer": "هَذَا صُنْدُوق",
        "image": "box.png",
        "sound": "whatIsThis.wav",
        "answer_sounds": ["giraffe.wav", "donkey.wav", "box.wav", "fox.wav"]
    },

]

def run_quiz():
    import tkinter as tk
    root = tk.Tk()
    app = WhatIsThis(root)
    root.mainloop()


# 🚀 Launch the game
if __name__ == "__main__":
    root = tk.Tk()
    game = WhatIsThis(root)
    root.mainloop()


