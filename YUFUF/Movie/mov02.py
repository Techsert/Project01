import os
from gtts import gTTS
import subprocess

ffmpeg_path = r"C:\Users\Cybersec\Downloads\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"
cmd = [ffmpeg_path, "-i", input_file, output_file]
subprocess.run(cmd)


# Conversation (speaker, text)
conversation = [
    ("youssef1", "السَّلَامُ عَلَيْكُمْ", "male"),
    ("luna1", "وَعَلَيْكُمُ السَّلَامُ", "female"),
    ("youssef2", "ما إسْمُكِ؟", "male"),
    ("luna2", "إسْمي لونا", "female"),
    ("luna3", "وانت ؟", "female"),
    ("youssef3", "أنا إسْمي يوسف", "male"),
    ("youssef4", "كَيْفَ حالُكِ؟", "male"),
    ("luna4", "أَنَا بِخَيْر، الْحَمْدُ لِلَّه", "female"),
    ("luna5", "وانت ؟", "female"),
    ("youssef5", "أَنَا بِخَيْر، الْحَمْدُ لِلَّه", "male"),
]

# Create output folders
os.makedirs("voices", exist_ok=True)

for filename, text, gender in conversation:
    raw_file = os.path.join("voices", f"{filename}_raw.mp3")
    final_file = os.path.join("voices", f"{filename}.mp3")

    # Step 1: Generate voice with gTTS
    tts = gTTS(text=text, lang='ar')
    tts.save(raw_file)

    # Step 2: Apply FFmpeg filter based on gender
    if gender == "male":
        # Deeper voice
        filter_cmd = "asetrate=44100*0.9,aresample=44100,atempo=1.0"
    else:
        # Higher voice
        filter_cmd = "asetrate=44100*1.1,aresample=44100,atempo=1.0"

    cmd = [
        "ffmpeg", "-y", "-i", raw_file,
        "-filter:a", filter_cmd,
        final_file
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"✅ Saved: {final_file}")

print("🎉 All voices generated successfully in the 'voices' folder!")
