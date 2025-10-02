"""
Image Captioning App using BLIP Model
====================================

This Gradio application generates descriptive captions for uploaded images
using Salesforce's BLIP (Bootstrapping Language-Image Pre-training) model.

Author: Hazm Talab
Model: Salesforce/blip-image-captioning-base
Framework: Gradio + Transformers
"""

import gradio as gr
import numpy as np
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
import torch

# Configuration
MODEL_NAME = "Salesforce/blip-image-captioning-base"
MAX_LENGTH = 50
TITLE = "AI Image Captioning Tool"
DESCRIPTION = """
Upload an image and get an AI-generated caption describing what's in the picture.
This tool uses Salesforce's BLIP model to analyze images and generate natural language descriptions.
"""

# Load the pretrained processor and model
print("Loading BLIP model and processor...")
try:
    processor = AutoProcessor.from_pretrained(MODEL_NAME)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    raise

def generate_caption(image: np.ndarray) -> str:
    """
    Generate a caption for the input image.
    
    Args:
        image (np.ndarray): Input image as numpy array from Gradio
        
    Returns:
        str: Generated caption describing the image
        
    Raises:
        ValueError: If image is None or invalid
        RuntimeError: If model inference fails
    """
    if image is None:
        raise ValueError("No image provided. Please upload an image.")
    
    try:
        # Convert numpy array to PIL Image and ensure RGB format
        pil_image = Image.fromarray(image).convert('RGB')
        
        # Process the image for the model
        inputs = processor(pil_image, return_tensors="pt")
        
        # Generate caption with controlled parameters
        with torch.no_grad():  # Disable gradient computation for inference
            output = model.generate(
                **inputs,
                max_length=MAX_LENGTH,
                num_beams=4,  # Beam search for better quality
                early_stopping=True,
                do_sample=False
            )
        
        # Decode the generated tokens to text
        caption = processor.decode(output[0], skip_special_tokens=True)
        
        return caption
        
    except Exception as e:
        error_msg = f"Error generating caption: {str(e)}"
        print(error_msg)
        return error_msg

def main():
    """
    Create and launch the Gradio interface.
    """
    # Create the interface
    interface = gr.Interface(
        fn=generate_caption,
        inputs=gr.Image(
            label="Upload Image",
            type="numpy",
            sources=["upload", "webcam"],  # Allow both upload and webcam
            height=400
        ),
        outputs=gr.Textbox(
            label="Generated Caption",
            placeholder="Caption will appear here...",
            lines=3,
            show_copy_button=True  # Allow users to copy the caption
        ),
        title=TITLE,
        description=DESCRIPTION,
        examples=[
            # You can add example images here if you want
            # ["example1.jpg"],
            # ["example2.jpg"]
        ],
        article="""
        ### How it works:
        1. **Upload an image** using the upload button or take a photo with your camera
        2. **Click Submit** to generate a caption
        3. **Copy the result** using the copy button if needed
        
        ### Model Information:
        - **Model**: Salesforce BLIP (Bootstrapping Language-Image Pre-training)
        - **Purpose**: Generate natural language descriptions of images
        - **Performance**: Optimized for general image understanding
        
        ### Tips for best results:
        - Use clear, well-lit images
        - Ensure main subjects are clearly visible
        - Works best with common objects and scenes
        """,
        theme = gr.themes.Glass(),  # Nice visual theme
        allow_flagging="never"  # Disable flagging for cleaner interface
    )
    
    # Launch the interface
    interface.launch(
        share=False,  # Set to True for temporary public link during testing
        server_name="0.0.0.0",  # Required for HuggingFace Spaces
        server_port=7860,  # Standard port for Spaces
        show_error=True  # Show detailed error messages
    )

if __name__ == "__main__":
    main()
