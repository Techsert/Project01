import tkinter as tk
import threading
from tkinter import PhotoImage
import os
import pygame
import time
from PIL import Image, ImageTk
#from alphabit_name import run_alphabit_name
from alphabit_name import run_alphabit_name as run_alphabit_name
from alphabit_sound import run_alphabit_sound as run_alphabit_sound
##from colors_quiz import run_quiz as run_colors_quiz
##from words_quiz import run_quiz as run_words_quiz

# Initialize sound system
pygame.mixer.init()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Learning World")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.show_welcome_screen()

        # Hovering Sound
    def play_hover_sound(self, sound_path):
        try:
            sound = pygame.mixer.Sound(sound_path)
            pygame.mixer.Channel(1).play(sound)
        except Exception as e:
            print(f"Hover sound error for {sound_path}:", e)
        
    def exit_fullscreen(self, event=None):
        pygame.mixer.music.stop()  # Stop background music
        self.root.attributes("-fullscreen", False)
        
        #Start button with sound
    def start_with_sound(self):
        try:
            click_sound = pygame.mixer.Sound(os.path.join("../assets/sounds/main/lets_start.mp3"))
            #pygame.mixer.music.set_volume(0.9)  # Optional: adjust volume


            click_sound.play()
        except Exception as e:
            print("Start sound error:", e)

        # Delay transition until sound finishes (e.g., 1.5 seconds)
        self.root.after(2000, self.show_section_screen)

        # Launch Alphabit Name Script
    def launch_alphabit_name(self):
        print("Launching Alphabit Name...")

        def delayed_launch():
            print("✅ run_alphabit_name about to be called")
            run_alphabit_name(self.root, self)  # 👈 pass self as main_app
        self.root.after(1500, delayed_launch)

        try:
            pygame.mixer.music.stop()
            pygame.mixer.Sound(os.path.join("../assets/sounds/main/quizStart.mp3")).play()
        except Exception as e:
            print("alphabit_name start sound error:", e)

        # ✅ schedule safely on Tkinter mainloop
        self.root.after(1500, delayed_launch)


        # Launch Alphabit Sound Script
    def launch_alphabit_sound(self):
        print("Launching Alphabit Sound DD...")

        def delayed_launch():
            print("✅ run_Alphabit Sound about to be called")
            run_alphabit_sound(self.root, main_app=self)  # ✅ pass self
        self.root.after(1500, delayed_launch)
            
        try:
            pygame.mixer.music.stop()
            pygame.mixer.Sound(os.path.join("../assets/sounds/main/quizStart.mp3")).play()
        except Exception as e:
            print("alphabit_sound start sound error:", e)

        


        # Welcome Screen   
    def show_welcome_screen(self):
        self.clear_screen()

        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Load and resize background image
        try:
            raw_img = Image.open(os.path.abspath("../assets/img/main/background.png"))
            resized_img = raw_img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(resized_img)  # Store as instance variable

            bg_label = tk.Label(self.root, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            print("Background image placed.")
        except Exception as e:
            print("Background image error:", e)

        # Welcome text and start button
        tk.Label(self.root, text="مرحباً", font=("Scheherazade", 250, "bold"), fg="#333333").place(relx=0.4, rely=0.3, anchor="center")
        tk.Button(self.root, text="هيا نبدأ", font=("Scheherazade", 72, "bold"), bg="#777799", fg="#ff6600", command=self.start_with_sound).place(relx=0.4, rely=0.7, anchor="center")

        # Delayed welcome sound
        self.root.after(0, self.play_welcome_sound)

    def play_welcome_sound(self):
        try:
            #pygame.mixer.Sound("../assets/sounds/main/bg_sound.mp3").play()
            pygame.mixer.music.load("../assets/sounds/main/bg_sound.mp3")
            pygame.mixer.music.set_volume(0.3)  # Optional: adjust volume
            pygame.mixer.music.play(loops=-1)   # Loop indefinitely


        except Exception as e:
            print("Sound error:", e)

    def show_section_screen(self):
        self.clear_screen()

        # Ensure screen dimensions are accurate
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Load and resize background image
        try:
            raw_img = Image.open(os.path.abspath("../assets/img/main/section_bg.png"))  # Use your section background image
            resized_img = raw_img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.section_bg_img = ImageTk.PhotoImage(resized_img)

            bg_label = tk.Label(self.root, image=self.section_bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Section background image error:", e)

        # Title
        #tk.Label(self.root, text="Choose a Quiz Section", font=("Arial", 20, "bold"), bg="#ffffff").place(relx=0.35, rely=0.1, anchor="center")

        # Button specs: relx, rely, label, action, hover sound
        button_specs = [
            (0.15, 0.36, "أسماء الحُروف", self.launch_alphabit_name, "../assets/sounds/main/hover_alphabetNames.wav"),
            (0.50, 0.36, "أصوات الحُروف", self.launch_alphabit_sound, "../assets/sounds/main/hover_alphabetSounds.wav"),
#            (0.85, 0.36, "الألوان", self.launch_colors_quiz, "../assets/sounds/hover_colors.mp3"),
##            (0.15, 0.88, "الكَلِمات", self.launch_words_quiz, "../assets/sounds/hover_words.mp3"),
            # Add more buttons here as needed
        ]

        for relx, rely, name, action, hover_sound in button_specs:
            btn = tk.Button(
                self.root,
                text=name,
                font=("Arial", 99, "bold"),
                bg="#ffffff",
                fg="#333333",
                highlightthickness=0,
                borderwidth=0,
                command=action,
                padx=0,   # horizontal padding
                pady=0    # vertical padding
            )
            btn.place(relx=relx, rely=rely, anchor="center")

            # Bind hover sound
            btn.bind("<Enter>", lambda e, path=hover_sound: self.play_hover_sound(path))


    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Play intro sound before GUI loads

    try:
        pygame.mixer.init()
        intro_sound = pygame.mixer.Sound(os.path.join("../assets/sounds/main/intro.mp3"))
        pygame.mixer.music.set_volume(1.5)  # Optional: adjust volume

        intro_sound.play()
    except Exception as e:
        print("Intro sound error:", e)

    # Launch GUI
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
