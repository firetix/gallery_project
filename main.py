# Start Generation Here
import streamlit as st
import replicate
import os
import pdb
from dotenv import load_dotenv

load_dotenv()

# Set up the Replicate API token (assumes it's stored in environment variables)


st.title("Generate")
COLUMNS = 2
# Input prompt from the user
user_prompt = st.text_input("Enter a prompt:")

if user_prompt:
    with st.spinner('Generating images...'):
        try:
            # Additional phrases to modify the prompt
            additional_phrases_str = "muted earth tones, soft morning light through windows, film photography aesthetic, shot on Canon 5D"
            additional_phrases = [phrase.strip() for phrase in additional_phrases_str.split(',')]

            # Store generated images
            generated_images = []

            # Model identifier
            model_identifier = "black-forest-labs/flux-schnell"

            for phrase in additional_phrases:
                # Modify the prompt by adding the phrase
                modified_prompt = f"{user_prompt}, {phrase}"

                # Generate the image with the modified prompt
                output = replicate.run(
                    model_identifier,
                    input={"prompt": modified_prompt}
                )

                # Check if output is a list (some models return multiple images)
                if isinstance(output, list):
                    generated_images.extend(output)
                else:
                    generated_images.append(output)

            # Create a grid with 4 columns
            cols = st.columns(COLUMNS)

            for idx, img_url in enumerate(generated_images):
                # Display each image in the corresponding column
                with cols[idx % COLUMNS]:
                    st.image(img_url, use_column_width=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
# End Generation Here

