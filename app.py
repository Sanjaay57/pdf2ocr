import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io

st.set_page_config(page_title="📄 PDF OCR Extractor", layout="centered")
st.title("📄 Extract Text from Scanned PDF using OCR")

# Upload PDF file
pdf_file = st.file_uploader("Upload a Scanned PDF", type=["pdf"])

if pdf_file:
    st.info("⏳ Converting PDF pages to images...")
    
    # Convert PDF pages to images
    images = convert_from_bytes(pdf_file.read())
    
    extracted_text = ""
    progress = st.progress(0)
    
    for i, image in enumerate(images):
        # OCR using pytesseract
        text = pytesseract.image_to_string(image, lang='eng')
        extracted_text += f"\n\n--- Page {i+1} ---\n{text}"
        progress.progress((i + 1) / len(images))
    
    progress.empty()
    
    # Display extracted text
    st.success("✅ OCR Completed")
    st.text_area("📄 Extracted Text", extracted_text, height=400)
    
    # Download option
    st.download_button(
        label="📥 Download Extracted Text",
        data=extracted_text,
        file_name="ocr_output.txt",
        mime="text/plain"
    )
