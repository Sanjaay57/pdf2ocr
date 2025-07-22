import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
from io import BytesIO

# Optional: For local Windows testing
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="PDF OCR Extractor", layout="centered")
st.title("📄 OCR Text Extractor from Scanned PDF")
st.markdown("Upload a **scanned or image-based PDF**. The app will perform OCR and extract the text.")

# Upload PDF
uploaded_pdf = st.file_uploader("📎 Upload Scanned PDF", type=["pdf"])

if uploaded_pdf:
    try:
        st.info("🔄 Converting PDF pages to images...")

        uploaded_pdf.seek(0)
        images = convert_from_bytes(uploaded_pdf.read(), dpi=300)

        st.info("🔍 Performing OCR on each page...")
        all_text = ""
        progress = st.progress(0)

        for i, img in enumerate(images):
            text = pytesseract.image_to_string(img, lang='eng')
            all_text += f"\n\n--- Page {i+1} ---\n{text}"
            progress.progress((i + 1) / len(images))

        progress.empty()
        st.success("✅ OCR Completed!")

        # Display extracted text
        st.subheader("📄 Extracted Text")
        st.text_area("Result", all_text, height=400)

        # Download button
        st.download_button(
            label="📥 Download as Text File",
            data=all_text,
            file_name="ocr_output.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
