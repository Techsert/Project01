from pydub import AudioSegment

sound = AudioSegment.from_file("youssef_egyptian_male.mp3")
# Increase pitch by speeding up slightly
child_like = sound._spawn(sound.raw_data, overrides={
    "frame_rate": int(sound.frame_rate * 1.2)
}).set_frame_rate(sound.frame_rate)

child_like.export("youssef_egyptian_childlike.mp3", format="mp3")
