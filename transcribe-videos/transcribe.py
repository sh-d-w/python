import json
import os
import soundfile as sf
from vosk import Model, KaldiRecognizer

def format_timestamp(seconds):
    """Converts seconds into standard SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def audio_to_srt(audio_path, model_path="model", srt_path="output.srt"):
    if not os.path.exists(model_path):
        print(f"Error: Model folder '{model_path}' not found. Please extract it here.")
        return

    # Load the audio file and get its sample rate
    # SoundFile handles file reading without needing global FFmpeg environment variables
    data, sample_rate = sf.read(audio_path, dtype='int16')
    
    # Initialize Vosk
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)
    rec.SetWords(True) # Required to get precise word timestamps

    print("Transcribing audio tracks... Please wait.")
    
    # Process audio data in chunks
    chunk_size = 4000
    words = []
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size].tobytes()
        if rec.AcceptWaveform(chunk):
            result = json.loads(rec.Result())
            if "result" in result:
                words.extend(result["result"])
                
    # Catch any remaining text at the end of the file
    final_result = json.loads(rec.FinalResult())
    if "result" in final_result:
        words.extend(final_result["result"])

    if not words:
        print("No speech detected or transcription empty.")
        return

    # Group words into subtitle sentences (roughly 8 words per line)
    srt_lines = []
    sentence_words = []
    subtitle_index = 1
    words_per_line = 8

    for idx, word_info in enumerate(words):
        sentence_words.append(word_info)
        
        # Write out a subtitle block when limit reached or at the very end
        if len(sentence_words) == words_per_line or idx == len(words) - 1:
            start_time = format_timestamp(sentence_words[0]["start"])
            end_time = format_timestamp(sentence_words[-1]["end"])
            text = " ".join([w["word"] for w in sentence_words])
            
            srt_lines.append(f"{subtitle_index}\n{start_time} --> {end_time}\n{text}\n\n")
            subtitle_index += 1
            sentence_words = []

    # Save to file
    with open(srt_path, "w", encoding="utf-8") as f:
        f.writelines(srt_lines)
        
    print(f"Success! Subtitles saved to: {os.path.abspath(srt_path)}")

# Run the function (Make sure audio.mp3 is in this exact folder)
audio_to_srt("audio.mp3")
