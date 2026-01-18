import asyncio
import edge_tts

async def main():
    text = "اربعهخ"
    voice = "ar-EG-ShakirNeural"   # Male voice
    output_file = text + "boyAE.wav"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

    print(f"Saved audio: {output_file}")

asyncio.run(main())
