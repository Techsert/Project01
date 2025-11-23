from pydub import AudioSegment

# Load your female TTS audio
sound = AudioSegment.from_file(r"C:\Users\Cybersec\Desktop\Movie\Luna11.mp3")

# Raise pitch without increasing speed
new_frame_rate = int(sound.frame_rate * 1.25)  # 25% higher pitch
pitched_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_frame_rate})

# Reset to original frame rate to keep the speed natural
child_like = pitched_sound.set_frame_rate(sound.frame_rate)

# Export the result
child_like.export(r"C:\Users\Cybersec\Desktop\Movie\littlegirl.mp3", format="mp3")
