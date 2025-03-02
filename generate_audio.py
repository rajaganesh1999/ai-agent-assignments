import wave

# Generate a blank test audio file
with wave.open("sample_audio.wav", "w") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(b"\x00" * 44100)  # 1 second of silence

print("Sample audio file created: sample_audio.wav")
