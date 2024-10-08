import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import requests
import base64
from openai import OpenAI
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from PIL import Image
import uuid

load_dotenv()

# Set up the Replicate API token
replicate_api_token = os.getenv('REPLICATE_API_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_s3_bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
aws_s3_region = os.getenv('AWS_S3_REGION')

st.title("Image-to-Image Generation")

# Function to encode the image
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')


def upload_to_s3(file, bucket_name, object_name=None):
    if object_name is None:
        object_name = str(uuid.uuid4()) + "_" + file.name

    s3_client = boto3.client('s3', 
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
        return f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    except NoCredentialsError:
        st.error("AWS credentials not available")
        return None
    
def upload_image_to_s3(image_file, filename):
    # import pdb; pdb.set_trace()
    s3_client = boto3.client(
        's3',
        region_name=aws_s3_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    # import pdb; pdb.set_trace()

    try:
        s3_client.upload_fileobj(
            image_file,
            aws_s3_bucket_name,
            filename,
            ExtraArgs={
                'ContentType': image_file.type
            }
        )

        image_url = f"https://{aws_s3_bucket_name}.s3.{aws_s3_region}.amazonaws.com/{filename}"
        return image_url
    # return "test"
    except NoCredentialsError:
        st.error("AWS credentials not available.")
        return None
    except ClientError as e:
        import pdb; pdb.set_trace()
        st.error(f"Client error: {e}")
        return None
    
    
# Input image from the user
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    
    if st.button('Generate Similar Image'):
        with st.spinner('Processing...'):
            try:
                # Upload image to S3
                # s3_url = upload_to_s3(uploaded_file, aws_s3_bucket_name)
                s3_url = "https://mocro-gallery.s3.amazonaws.com/1.jpg"
                image_filename = uploaded_file.name
                s3_url = upload_image_to_s3(uploaded_file, image_filename)
                import pdb; pdb.set_trace()
                if s3_url:
                    # Send the S3 image URL to ChatGPT for analysis
                    client = OpenAI(api_key=openai_api_key)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Generate a prompt from this image"},
                                    {
                                        "type": "image_url",
                                        "image_url": { "url": s3_url }
                                    }
                                ]
                            }
                        ],
                        max_tokens=300
                    )

                    # Extract the generated prompt
                    generated_prompt = response.choices[0].message.content
                    st.write("Generated prompt:", generated_prompt)

                                        # Generate 4 images using the generated prompt
                    images = []
                    for _ in range(4):
                        output = replicate.run(
                            "black-forest-labs/flux-schnell",
                            input={"prompt": generated_prompt}
                        )
                        images.append(output[0])

                    # Display the generated images in a 2x2 grid
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(images[0], caption='Generated Image 1', use_column_width=True)
                        st.image(images[2], caption='Generated Image 3', use_column_width=True)
                    with col2:
                        st.image(images[1], caption='Generated Image 2', use_column_width=True)
                        st.image(images[3], caption='Generated Image 4', use_column_width=True)
                else:
                    st.error("Failed to upload image to S3")

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.write("Note: Make sure to set REPLICATE_API_TOKEN, OPENAI_API_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and S3_BUCKET_NAME in your .env file.")