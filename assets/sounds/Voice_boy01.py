import asyncio
import edge_tts

async def main():
    text = "الأعداد"
##    voice = "ar-AE-FatimaNeural"
##    voice = "ar-AE-HamdanNeural"
    voice = "ar-SA-HamedNeural"
##    voice = "ar-SA-ZariyahNeural"
##    voice = "ar-QA-MoazNeural"
##    voice = "ar-EG-ShakirNeural"   # Male voice
##    "ar-EG-SalmaNeural"
    output_file = "AAAAAAA.wav"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

    print(f"Saved audio: {output_file}")

asyncio.run(main())
