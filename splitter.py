import fitz
import streamlit as st
from tempfile import NamedTemporaryFile

def split_pdf(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    new_doc = fitz.open()
    
    for page in doc:
        rect = page.rect
        width = rect.width / 2  # Split in the middle
        
        # Left half
        left_page = new_doc.new_page(width=width, height=rect.height)
        left_page.show_pdf_page(left_page.rect, doc, page.number, clip=fitz.Rect(0, 0, width, rect.height))
        
        # Right half
        right_page = new_doc.new_page(width=width, height=rect.height)
        right_page.show_pdf_page(right_page.rect, doc, page.number, clip=fitz.Rect(width, 0, rect.width, rect.height))
    
    new_doc.save(output_pdf)

def main():
    st.title("PDF Page Splitter")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input_path = temp_input.name
        
        output_file_path = temp_input_path.replace(".pdf", "_split.pdf  ")
        split_pdf(temp_input_path, output_file_path)
        
        with open(output_file_path, "rb") as f:
            st.download_button("Download Split PDF", f, file_name="split_pdf.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
