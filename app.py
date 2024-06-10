import gradio as gr
import pyqrcode
from PIL import Image, ImageDraw, ImageFont
import io

def generate_qr_code(url, title):
    # Generate QR code
    qr = pyqrcode.create(url)
    buffer = io.BytesIO()
    
    # Create the QR code as a PNG
    qr.png(buffer, scale=10)
    
    # Move to the beginning of the StringIO buffer
    buffer.seek(0)
    qr_image = Image.open(buffer)
    
    # Prepare to add title to the image
    image_width = qr_image.width
    image_height = qr_image.height + 70  # Add 70 pixels space for title
    
    # Create a new image with white background
    result_image = Image.new('RGB', (image_width, image_height), 'white')
    # Paste the QR code onto this new image
    result_image.paste(qr_image, (0, 70))
    
    # Draw the title on the image
    draw = ImageDraw.Draw(result_image)
    font_path = "dejavu-sans-bold.ttf"  # Ensure the font path is correct
    font = ImageFont.truetype(font_path, 24)  # Use a specific font size
    text_width, text_height = draw.textsize(title, font=font)
    text_x = (image_width - text_width) / 2  # Center the text
    draw.text((text_x, 20), title, fill="black", font=font)
    
    # Return the final image
    return result_image

# Create the Gradio interface
iface = gr.Interface(
    fn=generate_qr_code,
    inputs=[
        gr.Textbox(label="Enter URL", placeholder="Type or paste URL here..."),
        gr.Textbox(label="Enter Title for QR Code", placeholder="Type the title here...")
    ],
    outputs=gr.Image(label="QR Code Image", type="pil", format="png"),
    title="QR Code Generator",
    description="Enter a URL and a title to generate a QR Code. The title and the QR Code will be displayed in the same image."
)

iface.launch()
