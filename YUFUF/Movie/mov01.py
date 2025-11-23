from gtts import gTTS
import warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="pkg_resources"
)

from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip,
    concatenate_audioclips, CompositeVideoClip, TextClip
)
import os

# الحوار (speaker, text)
dialogue = [
    ("يوسف", "السَّلَامُ عَلَيْكُمْ"),
    ("لونا", "وَعَلَيْكُمُ السَّلَامُ"),
    ("يوسف", "ما إسْمُكِ؟"),
    ("لونا", "إسْمي لونا"),
    ("لونا", "وانت ؟"),
    ("يوسف", "أنا إسْمي يوسف"),
    ("يوسف", "كَيْفَ حالُكِ؟"),
    ("لونا", "أَنَا بِخَيْر، الْحَمْدُ لِلَّه"),
    ("لونا", "وانت ؟"),
    ("يوسف", "أَنَا بِخَيْر، الْحَمْدُ لِلَّه"),
]

# مجلد الأصوات
os.makedirs("voices", exist_ok=True)

# إنشاء ملفات الصوت
voice_clips = []
for i, (speaker, text) in enumerate(dialogue):
    filename = f"voices/line_{i}.mp3"
    if not os.path.exists(filename):
        tts = gTTS(text=text, lang="ar")
        tts.save(filename)
    voice_clips.append(AudioFileClip(filename))

# تجميع الصوت
full_audio = concatenate_audioclips(voice_clips)

# الخلفية
background = ImageClip("park_background.jpg").set_duration(full_audio.duration).resize((1280,720))

# الشخصيات (صور يوسف و لونا، مع سبرايتات لحركة الفم)
youssef_neutral = ImageClip("youssef_neutral.png").resize(height=400).set_position(("left","bottom"))
youssef_talk = ImageClip("youssef_talk.png").resize(height=400).set_position(("left","bottom"))

luna_neutral = ImageClip("luna_neutral.png").resize(height=400).set_position(("right","bottom"))
luna_talk = ImageClip("luna_talk.png").resize(height=400).set_position(("right","bottom"))

# تجميع الفيديو مع الحوارات
video_layers = [background]
time_cursor = 0

for i, (speaker, text) in enumerate(dialogue):
    dur = voice_clips[i].duration

    # تحديد من يتكلم
    if speaker == "يوسف":
        char = youssef_talk.set_duration(dur).set_start(time_cursor)
        idle = luna_neutral.set_duration(dur).set_start(time_cursor)
    else:
        char = luna_talk.set_duration(dur).set_start(time_cursor)
        idle = youssef_neutral.set_duration(dur).set_start(time_cursor)

    # فقاعات الكلام
    subtitle = (TextClip(f"{speaker}: {text}",
                         fontsize=50, font="Amiri-Bold", color="white", bg_color="black")
                .set_duration(dur).set_start(time_cursor).set_position(("center","top")))

    video_layers += [char, idle, subtitle]
    time_cursor += dur

# إنشاء الفيديو النهائي
video = CompositeVideoClip(video_layers, size=(1280,720))
video = video.set_audio(full_audio)

video.write_videofile("conversation.mp4", fps=24, codec="libx264")
