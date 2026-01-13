import asyncio
import edge_tts

async def main():
    text = "الأعداد"
##    voice = "ar-EG-ShakirNeural"   # Arabic male voice
##    voice = "ar-AE-FatimaNeural"
##    voice = "ar-AE-HamdanNeural"
    voice = "ar-SA-HamedNeural"
##    voice = "ar-SA-ZariyahNeural"
##    voice = "ar-QA-MoazNeural"
##    voice = "ar-EG-ShakirNeural"   # Male voice
##    "ar-EG-SalmaNeural"
    output_file = "AAAAAAA.wav"

    # 🎛️ Adjustable speech settings
    rate = "-10%"      # speed: "-50%" (slower) to "+50%" (faster)
    volume = "+0%"     # volume: "-100%" to "+100%"
    pitch = "+10Hz"     # pitch: "-50Hz" to "+50Hz"

    # 🗣️ Generate speech
    communicate = edge_tts.Communicate(
        text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch=pitch
    )

    await communicate.save(output_file)
    print(f"✅ Saved audio: {output_file}")

# Run the async function
asyncio.run(main())
