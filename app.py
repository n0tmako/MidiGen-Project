import streamlit as st
import gen_functions as gf

st.title("MIDI Melody Generator")

mood = st.selectbox("Choose a mood:",
                     ["happy", "sad", "rage", "malancholy"
                      , "dreamy", "mysterious", "energetic"
                      , "calm", "nostalgic", "excited", "romantic"])

randomness = st.slider("Select Randomness (0-3):", 0,3,1)

bar_length = st.number_input("Bar length (beats):", min_value=1, max_value=16, value=8)

# Chords toggle
use_chords = st.checkbox("Include chords?")

# Filename
filename = st.text_input("Output filename:", "melody.mid")
if not filename.lower().endswith(".mid"):
    filename += ".mid"

# Generate button
if st.button("Generate MIDI"):
    gf.create_simple_melody(
        filename=filename,
        mood=mood,
        randomness=randomness,
        bar_length=bar_length,
        chords=use_chords,
    )
    st.success(f"MIDI file '{filename}' generated successfully!")
    st.download_button(
        label="Download MIDI file",
        data=open(filename, "rb").read(),
        file_name=filename,
        mime="audio/midi"
    )
