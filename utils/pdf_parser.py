from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file):
    '''
    Extracts text from a PDF file.'''
    pdf = PdfReader(uploaded_file)
    text=""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text