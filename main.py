import gen_functions                                             

if __name__ == "__main__":
    print("🎵 Welcome to the MIDI Melody Generator 🎵\n")

    filename = input("Enter filename (e.g., 'melody.mid'): ")

    print("\nAvailable moods:")
    for mood in gen_functions.mood_preset.mood_setting:
        print(f" - {mood}")
    mood = input("\nEnter a mood: ").strip().lower()

    randomness = int(input("Enter randomness level (0-5): "))
    bar_length = int(input("Enter number of bars: "))

    chords_input = input("Add chords? (y/n): ").strip().lower()
    pauses_input = input("Add pauses? (y/n): ").strip().lower()

    chords = chords_input == "y"
    pauses = pauses_input == "y"

    try:
        gen_functions.create_simple_melody(
            filename=filename,
            mood=mood,
            randomness=randomness,
            bar_length=bar_length,
            chords=chords,
            pauses=pauses
        )
    except Exception as e:
        print(f"Error: {e}")
