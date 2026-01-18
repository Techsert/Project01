import asyncio
import edge_tts

async def main():
    text = "السلام عليكم" 
    voice = "ar-EG-SalmaNeural"   # Female voice
    output_file = text + "luna_girl.wav"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

    print(f"Saved audio: {output_file}")

asyncio.run(main())
