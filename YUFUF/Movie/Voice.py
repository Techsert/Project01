import asyncio
import edge_tts

async def main():
    text = "السَّلَامُ عَلَيْكُمْ"
    voice = "ar-EG-ShakirNeural"   # Male voice
    output_file = "youssef_boy.mp3"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

    print(f"Saved audio: {output_file}")

asyncio.run(main())
