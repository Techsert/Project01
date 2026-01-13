import tkinter as tk
from PIL import Image, ImageTk
import pygame
import os
#from functools import partial


# Initialize pygame mixer
pygame.mixer.init()

# Sample slide data
slides = [
        # Intro Slide
##    {
##        "title": "الحُروف العَرَبية",
##        "narration": "../assets/sounds/alphabitSound/intro.wav",
##        "images": [
##            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
##            {"path": "../assets/img/alphabitSound/hard.png", "sound": "../assets/sounds/alphabitSound/areyouready.wav", "delay": 4000, "scale": (0.25, 0.55), "position": "center"},
##        ]
##    },
##        # Slide 1 - Alef
##    {
##        "title": "حرف الألف",
##        "narration": "../assets/sounds/alphabitSound/01alef.wav",
##        "images": [
##            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
##            {"path": "../assets/img/alphabitSound/01alef.png", "sound": "../assets/sounds/alphabitSound/01alef.wav", "delay": 0, "scale": (0.04, 0.40), "position": "center"}
##        ]
##    },
##        # Slide 2 - Ba
##    {
##        "title": "حرف الباء",
##        "narration": "../assets/sounds/alphabitSound/02ba.wav",
##        "images": [
##            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
##            {"path": "../assets/img/alphabitSound/02ba.png", "sound": "../assets/sounds/alphabitSound/02ba.wav", "delay": 0, "scale": (0.20, 0.30), "position": "center"}
##        ]
##    },
##        # Slide 3 - Ta
##    {
##        "title": "حرف التاء",
##        "narration": "../assets/sounds/alphabitSound/03ta.wav",
##        "images": [
##            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
##            {"path": "../assets/img/alphabitSound/03ta.png", "sound": "../assets/sounds/alphabitSound/03ta.wav", "delay": 0, "scale": (0.20, 0.35), "position": "center"}
##        ]
##    },
        # Slide 4 - Tha
    {
        "title": "حرف الثاء",
        "narration": "../assets/sounds/alphabitSound/04tha.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/04tha.png", "sound": "../assets/sounds/alphabitSound/04tha.wav", "delay": 0, "scale": (0.20, 0.38), "position": "center"}
        ]
    },
            # Slide 5 - Gem
    {
        "title": "حرف الجيم",
        "narration": "../assets/sounds/alphabitSound/05gem.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/05gem.png", "sound": "../assets/sounds/alphabitSound/05gem.wav", "delay": 0, "scale": (0.25, 0.40), "position": "center"}
        ]
    },
            # Slide 6 - 7a
    {
        "title": "حرف الحاء",
        "narration": "../assets/sounds/alphabitSound/06-7a.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/06ha.png", "sound": "../assets/sounds/alphabitSound/06-7a.wav", "delay": 0, "scale": (0.25, 0.40), "position": "center"}
        ]
    },
            # Slide 7 - 7'a
    {
        "title": "حرف الخاء",
        "narration": "../assets/sounds/alphabitSound/07-7-a.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/07ka.png", "sound": "../assets/sounds/alphabitSound/07-7-a.wav", "delay": 0, "scale": (0.30, 0.50), "position": "center"}
        ]
    },
            # Slide 8 - Dal
    {
        "title": "حرف الدال",
        "narration": "../assets/sounds/alphabitSound/08dal.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/08dal.png", "sound": "../assets/sounds/alphabitSound/08dal.wav", "delay": 0, "scale": (0.25, 0.40), "position": "center"}
        ]
    },
            # Slide 9 - Thal
    {
        "title": "حرف الذال",
        "narration": "../assets/sounds/alphabitSound/09thal.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/09thal.png", "sound": "../assets/sounds/alphabitSound/09thal.wav", "delay": 0, "scale": (0.25, 0.50), "position": "center"}
        ]
    },
            # Slide 10 - Ra
    {
        "title": "حرف الراء",
        "narration": "../assets/sounds/alphabitSound/10ra.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/10ra.png", "sound": "../assets/sounds/alphabitSound/10ra.wav", "delay": 0, "scale": (0.25, 0.50), "position": "center"}
        ]
    },
            # Slide 11 - Zay
    {
        "title": "حرف الزاي",
        "narration": "../assets/sounds/alphabitSound/11zay.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/11zay.png", "sound": "../assets/sounds/alphabitSound/11zay.wav", "delay": 0, "scale": (0.25, 0.50), "position": "center"}
        ]
    },
            # Slide 12 - Sen
    {
        "title": "حرف السين",
        "narration": "../assets/sounds/alphabitSound/12sen.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/12sen.png", "sound": "../assets/sounds/alphabitSound/12sen.wav", "delay": 0, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
            # Slide 13 - Shen
    {
        "title": "حرف الشين",
        "narration": "../assets/sounds/alphabitSound/13shen.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/13shen.png", "sound": "../assets/sounds/alphabitSound/13shen.wav", "delay": 0, "scale": (0.30, 0.50), "position": "center"}
        ]
    },
            # Slide 14 - Sad
    {
        "title": "حرف الصاد",
        "narration": "../assets/sounds/alphabitSound/14sad.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/14sad.png", "sound": "../assets/sounds/alphabitSound/14sad.wav", "delay": 0, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
            # Slide 15 - Dad
    {
        "title": "حرف الضاد",
        "narration": "../assets/sounds/alphabitSound/15dad.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/15dad.png", "sound": "../assets/sounds/alphabitSound/15dad.wav", "delay": 0, "scale": (0.30, 0.50), "position": "center"}
        ]
    },
            # Slide 16 - Taa
    {
        "title": "حرف الطاء",
        "narration": "../assets/sounds/alphabitSound/16taa.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/16taa.png", "sound": "../assets/sounds/alphabitSound/16taa.wav", "delay": 0, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
            # Slide 17 - Zaa
    {
        "title": "حرف الظاء",
        "narration": "../assets/sounds/alphabitSound/17zaa.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/17zaa.png", "sound": "../assets/sounds/alphabitSound/17zaa.wav", "delay": 0, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
            # Slide 18 - Aen
    {
        "title": "حرف العين",
        "narration": "../assets/sounds/alphabitSound/18ayn.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/18aen.png", "sound": "../assets/sounds/alphabitSound/18ayn.wav", "delay": 0, "scale": (0.25, 0.50), "position": "center"}
        ]
    },
            # Slide 19 - Gaen
    {
        "title": "حرف الغين",
        "narration": "../assets/sounds/alphabitSound/19gean.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/19gean.png", "sound": "../assets/sounds/alphabitSound/19gean.wav", "delay": 0, "scale": (0.20, 0.50), "position": "center"}
        ]
    },
            # Slide 20 - Feh
    {
        "title": "حرف الفاء",
        "narration": "../assets/sounds/alphabitSound/20feh.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/20feh.png", "sound": "../assets/sounds/alphabitSound/20feh.wav", "delay": 0, "scale": (0.25, 0.40), "position": "center"}
        ]
    },
            # Slide 21 - Kf
    {
        "title": "حرف القاف",
        "narration": "../assets/sounds/alphabitSound/21kf.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/21kf.png", "sound": "../assets/sounds/alphabitSound/21kf.wav", "delay": 0, "scale": (0.25, 0.40), "position": "center"}
        ]
    },
            # Slide 22 - Kaf
    {
        "title": "حرف الكاف",
        "narration": "../assets/sounds/alphabitSound/22kaf.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/22kaf.png", "sound": "../assets/sounds/alphabitSound/22kaf.wav", "delay": 0, "scale": (0.25, 0.40), "position": "center"}
        ]
    },
            # Slide 23 - Lam
    {
        "title": "حرف اللام",
        "narration": "../assets/sounds/alphabitSound/23lam.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/23lam.png", "sound": "../assets/sounds/alphabitSound/23lam.wav", "delay": 0, "scale": (0.20, 0.50), "position": "center"}
        ]
    },
            # Slide 24 - Meam
    {
        "title": "حرف الميم",
        "narration": "../assets/sounds/alphabitSound/24meam.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/24meam.png", "sound": "../assets/sounds/alphabitSound/24meam.wav", "delay": 0, "scale": (0.20, 0.50), "position": "center"}
        ]
    },
            # Slide 25 - Noon
    {
        "title": "حرف النون",
        "narration": "../assets/sounds/alphabitSound/25noon.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/25noon.png", "sound": "../assets/sounds/alphabitSound/25noon.wav", "delay": 0, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
            # Slide 26 - Heh
    {
        "title": "حرف الهاء",
        "narration": "../assets/sounds/alphabitSound/26heh.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/26heh.png", "sound": "../assets/sounds/alphabitSound/26heh.wav", "delay": 0, "scale": (0.25, 0.50), "position": "center"}
        ]
    },
                # Slide 27 - Waw
    {
        "title": "حرف الواو",
        "narration": "../assets/sounds/alphabitSound/27waw.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/27waw.png", "sound": "../assets/sounds/alphabitSound/27waw.wav", "delay": 0, "scale": (0.20, 0.40), "position": "center"}
        ]
    },
                # Slide 28 - Yaa
    {
        "title": "حرف الياء",
        "narration": "../assets/sounds/alphabitSound/28yaa.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/28yaa.png", "sound": "../assets/sounds/alphabitSound/28yaa.wav", "delay": 0, "scale": (0.30, 0.50), "position": "center"}
        ]
    },
                # End Slid
    {
        "title": "أحسنت",
        "narration": "../assets/sounds/alphabitSound/areyouready.wav",
        "images": [
            {"path": "../assets/img/alphabitSound/bg-nt.png", "delay": 0, "scale": (0.95, 0.82), "position": "center"},
            {"path": "../assets/img/alphabitSound/k2.png", "sound": "../assets/sounds/alphabitSound/tha.wav", "delay": 0, "scale": (0.30, 0.40), "position": "center"}
        ]
    },
    
]

class AlphabitNameApp:
    def __init__(self, root, main_app=None):
        self.root = root
        self.main_app = main_app  # store reference to QuizApp
        self.root.title("Alphabet Names - أسماء الحروف")
        self.root.attributes('-fullscreen', True)
        self.slide_index = 0
        self.image_labels = []
        self.photos = []  
        self.scheduled_tasks = []  
        self.root.configure(bg="white")

        root.bind("<Escape>", self.on_escape)
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Title
        self.title_label = tk.Label(root, text="", font=("Scheherazade", 60, "bold"), bg="#ffffff", bd=0, relief="flat")
        self.title_label.pack(pady=.05)
        self.title_label.pack(padx=0.05)

        # Image container (center)
        self.image_frame = tk.Frame(root, bg="#ffffff", height=400)
        self.image_frame.pack(fill="both", expand=True, pady=0)

        # Navigation (bottom bar)
        self.nav_frame = tk.Frame(root, bg="#ffffff", height=100)
        self.nav_frame.pack(side="bottom", fill="x")

        self.load_slide()

    def on_close(self):
        """Stop all sounds and quit the mixer before closing window."""
        self.stop_sounds()         # stop music and channels
        pygame.mixer.quit()        # fully shutdown Pygame mixer
        self.root.destroy()        # close the Tk window


    def on_escape(self, event=None):
        """Handle Escape key: stop sounds and exit fullscreen."""
        self.stop_sounds()  # ✅ stop narration + hover sounds
        self.root.attributes('-fullscreen', False)


    def load_slide(self):
        self.clear_scheduled_tasks()
        self.clear_images()
        
        slide = slides[self.slide_index]
        self.title_label.config(text=slide["title"])
        print("Slide title:", slide["title"])

        # Stop any currently playing narration
        pygame.mixer.music.stop()


        # Play narration using mixer.music
        try:
            pygame.mixer.music.load(slide["narration"])
            pygame.mixer.music.set_volume(1.0)  # Full volume
            pygame.mixer.music.play()
        except Exception as e:
            print("Narration error:", e)

        # Schedule images with delay
        for img_data in slide["images"]:
            delay = img_data.get("delay", 0)
            task_id = self.root.after(delay, self.make_image_callback(img_data))
            self.scheduled_tasks.append(task_id)

        self.add_back_button()  # add persistent Back button
        self.update_navigation_buttons()
        
##################################################
        def load_slide(self):
            self.clear_scheduled_tasks()
            self.clear_images()


##################################
    def add_back_button(self):
        back_btn = tk.Button(
            self.nav_frame,
            text="⬅ العودة",
            font=("Scheherazade", 25, "bold"),
            bg="#ffcccc",
            fg="#000000",
            command=self.back_to_main
        )
        back_btn.place(relx=0.5, rely=0.5, anchor="center")

    def back_to_main(self):
        # 1️⃣ Stop all playing sounds
        self.stop_sounds()  

        # 2️⃣ Clear scheduled slide tasks
        self.clear_scheduled_tasks()

        # 3️⃣ Clear all widgets from root
        for widget in self.root.winfo_children():
            widget.destroy()

        # 4️⃣ Return to main menu if reference exists
        if self.main_app:
            print("🔙 Returning to Main Menu")
            self.main_app.show_section_screen()
        else:
            print("⚠ No main_app reference provided")
            self.root.destroy()







####################################



        #Stop sound when moving to next slid
    def stop_sounds(self):
        try:
            # Stop narration
            pygame.mixer.music.stop()
            # Stop all sound channels (hover sounds, effects, etc.)
            for i in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(i).stop()
        except Exception as e:
            print("Stop sound error:", e)



    def make_image_callback(self, img_data):
        def callback():
            # Only show if we’re still on the same slide
            if img_data in slides[self.slide_index]["images"]:
                self.show_image(img_data)
        return callback


    def clear_scheduled_tasks(self):
        for task_id in self.scheduled_tasks:
            try:
                self.root.after_cancel(task_id)
            except Exception:
                pass
        self.scheduled_tasks.clear()


    def show_image(self, img_data):
        # ✅ If frame is destroyed (like when back to main menu), skip
        if not self.image_frame.winfo_exists():
            return  

        abs_path = os.path.abspath(img_data["path"])
        if not os.path.exists(abs_path):
            print("❌ Image not found:", abs_path)
            fallback = tk.Label(self.image_frame, text="Image missing", bg="white", font=("Arial", 12))
            fallback.place(relx=0.5, rely=0.5, anchor="center")
            return

        try:
            # Get screen size
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()

            # Use scale if provided, otherwise default 0.2 x 0.3
            scale = img_data.get("scale", (0.2, 0.3))
            img_w = int(screen_w * scale[0])
            img_h = int(screen_h * scale[1])

            img = Image.open(abs_path).resize((img_w, img_h))
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(self.image_frame, image=photo, bg=self.image_frame["bg"])
            label.image = photo
            self.photos.append(photo)

            # Position
            pos = img_data.get("position", "center")
            position_map = {
                "center":      {"relx": 0.5, "rely": 0.5, "anchor": "center"},
                "top-left":    {"relx": 0.0, "rely": 0.0, "anchor": "nw"},
                "top-right":   {"relx": 1.0, "rely": 0.0, "anchor": "ne"},
                "bottom-left": {"relx": 0.02, "rely": 0.98, "anchor": "sw"},
                "bottom-right":{"relx": 0.98, "rely": 0.98, "anchor": "se"},
            }
            opts = position_map.get(pos, position_map["center"])
            label.place(**opts)

            self.image_labels.append(label)
            self.image_frame.lift()

        except Exception as e:
            print("❌ Image error:", e)
            if self.image_frame.winfo_exists():  # ✅ double check
                fallback = tk.Label(self.image_frame, text="Image error", bg="#ffffff", font=("Scheherazade", 12))
                fallback.place(relx=0.5, rely=0.5, anchor="center")



    def play_hover_sound(self, path):
        try:
            sound = pygame.mixer.Sound(path)
            pygame.mixer.Channel(1).play(sound)
        except Exception as e:
            print("Hover sound error:", e)

    def clear_images(self):
        for lbl in self.image_labels:
            lbl.destroy()
        self.image_labels.clear()
        self.stop_sounds()   # ✅ stop audio when slide cleared

    def next_slide(self):
        if self.slide_index < len(slides) - 1:
            self.stop_sounds()   # ✅ stop old sounds
            self.slide_index += 1
            self.load_slide()

    def prev_slide(self):
        if self.slide_index > 0:
            self.stop_sounds()   # ✅ stop old sounds
            self.slide_index -= 1
            self.load_slide()

    def update_navigation_buttons(self):
        # Clear old buttons
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        # Previous button (not on first slide)
        if self.slide_index > 0:
            prev_btn = tk.Button(
                self.nav_frame, text="السابق ⏭", font=("Scheherazade", 25, "bold"),
                command=self.prev_slide, bg="#ddddff"
            )
            prev_btn.place(relx=0.9, rely=0.5, anchor="center")

        # ✅ Back to main (always visible, bottom center)
        back_btn = tk.Button(
            self.nav_frame, text="⬅ العودة", font=("Scheherazade", 25, "bold"),
            command=self.back_to_main, bg="#ffcccc"
        )
        back_btn.place(relx=0.5, rely=0.5, anchor="center")

        # Next or Exit button
        if self.slide_index < len(slides) - 1:
            next_btn = tk.Button(
                self.nav_frame, text="⏮ التالي", font=("Scheherazade", 25, "bold"),
                command=self.next_slide, bg="#ccffcc"
            )
            next_btn.place(relx=0.1, rely=0.5, anchor="center")
        else:
            exit_btn = tk.Button(
                self.nav_frame, text="الخروج x", font=("Scheherazade", 25, "bold"),
                command=self.root.destroy, bg="#ffcccc"
            )
            exit_btn.place(relx=0.1, rely=0.5, anchor="center")


def run_alphabit_name(root=None, main_app=None):
    if root is None:
        root = tk.Tk()
        app = AlphabitNameApp(root, main_app)
        root.mainloop()
    else:
        # ✅ Clear any old widgets from main menu
        for widget in root.winfo_children():
            widget.destroy()

        app = AlphabitNameApp(root, main_app)


if __name__ == "__main__":
    run_alphabit_name()

