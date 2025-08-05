from mido import *
import random, mood_preset

from mido import MidiFile, MidiTrack, Message
import random
import mood_preset


def get_mood_settings(mood):
    return (
        mood_preset.mood_setting[mood]['scale'],
        mood_preset.mood_setting[mood]['rhythm']
    )

def generate_melody(scale, rhythm, randomness, bars):
    notes = []
    last_note_index = len(scale) // 2
    num_steps = 16 * bars

    for _ in range(num_steps):
        jump_range = randomness if randomness > 0 else 1
        jump = random.randint(-jump_range, jump_range)
        note_index = (last_note_index + jump) % len(scale)
        note = scale[note_index]
        duration = random.choice(rhythm)
        velocity = random.randint(60, 100)

        notes.append((note, duration, velocity))
        last_note_index = note_index

    return notes

def add_chords(notes, scale):
    chord_notes = []
    for note, duration, velocity in notes:
        chord = [note]

        index = scale.index(note)
        if index + 2 < len(scale):
            chord.append(scale[index + 2])  # third
            if index + 4 < len(scale):
                chord.append(scale[index + 4])  # fifth
        for pitch in chord:
            chord_notes.append((pitch, duration, velocity))

    return chord_notes

def add_pauses(notes, pause_chance=0.2):
    final = []
    for note in notes:
        if random.random() < pause_chance:
            final.append(None) # pause
        else:
            final.append(note)
    return final

def write_to_midi(notes, filename):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=12, time=0))

    for note_data in notes:
        if note_data is None:
            continue  # pause
        note, duration, velocity = note_data
        track.append(Message('note_on', note=note, velocity=velocity, time=0))
        track.append(Message('note_off', note=note, velocity=velocity, time=duration))

    mid.save(filename)

def create_simple_melody(filename, mood, randomness, bar_length, chords, pauses):
    # Validation
    if mood not in mood_preset.mood_setting:
        raise ValueError("Invalid mood.")
    if not (0 <= randomness <= 5):
        raise ValueError("Randomness must be between 0 and 5.")
    if bar_length <= 0:
        raise ValueError("Bar length must be positive.")

    scale, rhythm = get_mood_settings(mood)
    notes = generate_melody(scale, rhythm, randomness, bar_length)

    if chords:
        notes = add_chords(notes, scale)

    if pauses:
        notes = add_pauses(notes)

    write_to_midi(notes, filename)

    print(f"MIDI saved as {filename} | Mood: {mood} | Randomness: {randomness} | Bars: {bar_length} | Chords: {chords} | Pauses: {pauses}")
