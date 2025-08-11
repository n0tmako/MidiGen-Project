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
    """Add chord accompaniment to melody notes"""
    chord_notes = []
    
    for note, duration, velocity in notes:
        # Add the original melody note
        chord_notes.append((note, duration, velocity))
        
        # Find the note in the scale
        try:
            base_index = scale.index(note)
        except ValueError:
            # If note not in scale, just add melody note
            continue
            
        # Create chord by adding third and fifth intervals
        # Use modulo to wrap around the scale
        third_index = (base_index + 2) % len(scale)
        fifth_index = (base_index + 4) % len(scale)
        
        third_note = scale[third_index]
        fifth_note = scale[fifth_index]
        
        # Add chord notes with slightly lower velocity
        chord_velocity = max(30, velocity - 20)
        chord_notes.append((third_note, duration, chord_velocity))
        chord_notes.append((fifth_note, duration, chord_velocity))

    return chord_notes

def write_to_midi(notes, filename):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=12, time=0))

    i = 0
    while i < len(notes):
        if notes[i] is None:
            # Insert a rest by delaying the next note
            track.append(Message('note_off', note=0, velocity=0, time=240))
            i += 1
            continue

        # Gather all notes that start at the same time (i.e., a chord)
        current_group = []
        duration = notes[i][1]
        velocity = notes[i][2]

        while i < len(notes) and notes[i] is not None and notes[i][1] == duration and notes[i][2] == velocity:
            current_group.append(notes[i][0])  # just the note
            i += 1

        # Play all chord notes simultaneously
        for note in current_group:
            track.append(Message('note_on', note=note, velocity=velocity, time=0))

        # Turn them all off after duration
        for note in current_group:
            track.append(Message('note_off', note=note, velocity=velocity, time=duration))
    
    mid.save(filename)

def create_simple_melody(filename, mood, randomness, bar_length, chords):
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

    write_to_midi(notes, filename)

    print(f"MIDI saved as {filename} | Mood: {mood} | Randomness: {randomness} | Bars: {bar_length} | Chords: {chords}")

    write_to_midi(notes, filename)

    print(f"MIDI saved as {filename} | Mood: {mood} | Randomness: {randomness} | Bars: {bar_length} | Chords: {chords} | Pauses: {pauses}")
