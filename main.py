from mido import MidiFile, MidiTrack, Message
import random 

def create_simple_melody(filename, mood, randomenss):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    track.append(Message('program_change', program=12, time=0))


    mood_setting = {
        "happy": {
            "scale": [60, 62, 64, 65, 67, 69, 71, 72],
            "rhythm": [480, 240, 120]
        },
        "sad": {
            "scale": [48, 50, 52, 53, 55, 57, 59, 60],
            "rhythm": [480, 240, 120]
        },
        "rage": {
            "scale": [72, 74, 76, 77, 79, 81, 83, 84],
            "rhythm": [480, 240, 120]
        },
        "malancholy": {
            "scale": [60, 62, 63, 65, 67, 68, 70, 72],
            "rhythm": [480, 240, 120]
        },
        "dreamy": {
            "scale": [55, 57, 59, 60, 62, 64, 66, 68, 70],
            "rhythm": [480, 240, 120]
        },
        "mysterious": {
            "scale": [60, 61, 63, 64, 66, 67, 69, 70],
            "rhythm": [480, 240, 120]
        },
        "energetic": {
            "scale": [72, 74, 76, 77, 79, 81, 83, 84],
            "rhythm": [480, 240, 120]
        },
        "calm": {
            "scale": [48, 50, 52, 53, 55, 57, 59, 60],
            "rhythm": [480, 240, 120]
        },
        "nostalgic": {
            "scale": [60, 62, 64, 65, 67, 69, 71, 72],
            "rhythm": [480, 240, 120]
        },
        "excited": {
            "scale": [72, 74, 76, 77, 79, 81, 83, 84],
            "rhythm": [480, 240, 120]
        },
        "romantic": {
            "scale": [60, 62, 64, 65, 67, 69, 71, 72],
            "rhythm": [480, 240, 120]
        },
    }
    scale = mood_setting[mood]['scale']
    rhythm = mood_setting[mood]['rhythm']

    for i in range(32):
        note = random.choice(scale)
        duration = random.choice(rhythm)
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=duration))

    mid.save(filename)
    print(f"MIDI saved as {filename}")

create_simple_melody("melody3.mid", "romantic", 0.5)