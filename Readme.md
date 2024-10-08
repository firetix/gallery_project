# Image-to-Image Generation App

This Streamlit application allows users to upload an image, which is then analyzed by OpenAI's GPT-4 Vision model to generate a descriptive prompt. This prompt is used to create a similar image using Replicate's Stable Diffusion model.

## Prerequisites

- Python 3.7 or higher
- OpenAI API key with access to GPT-4 Vision
- Replicate API token

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/image-to-image-generation.git
   cd image-to-image-generation
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   REPLICATE_API_TOKEN=your_replicate_api_token_here
   ```

## Running the Application

To run the Streamlit app, use the following command:

```
streamlit run app.py
```

Replace `app.py` with the name of your Python script if it's different.

The application will start, and you should see output similar to this:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.5:8501
```

Open the provided URL in your web browser to use the application.

## Using the Application

1. Upload an image using the file uploader.
2. Click the "Generate Similar Image" button.
3. Wait for the app to process the image, generate a prompt, and create a new image.
4. View the results, including the generated prompt and the new image.

## Requirements

The `requirements.txt` file should contain the following dependencies:

```
streamlit
replicate
python-dotenv
requests
openai
```

You can install these dependencies using the command mentioned in the Installation section.

## Troubleshooting

- If you encounter any API-related errors, make sure your `.env` file is set up correctly with valid API keys.
- Ensure you have access to the GPT-4 Vision model in your OpenAI account.
- If the image generation is slow, be patient - processing images and generating new ones can take some time.

## License

[Include your chosen license here]

## Contributing

[Include guidelines for contributing to your project, if applicable]