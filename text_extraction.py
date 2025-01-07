import pdfplumber
import json

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + ' '  
    return text.strip()  

def save_texts_as_jsonl_with_labels(text_list, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for text in text_list:
            # Create a dictionary with 'text' and an empty 'label' array
            record = {"text": text, "label": []}
            # Convert dictionary to JSON string and write to file
            json_record = json.dumps(record)
            f.write(json_record + '\n')


path = 'leases/cleaned/'
pdf_files = ['0.pdf', '1.pdf', '2.pdf', '3.pdf', '4.pdf', '5.pdf', '6.pdf', '7.pdf', '8.pdf', '9.pdf'] 
all_texts = []

for pdf_file in pdf_files:
    text = extract_text_from_pdf(path + pdf_file)
    all_texts.append(text)
    print(f"Extracted text from {pdf_file}")

save_texts_as_jsonl_with_labels(all_texts, 'lease_documents.jsonl')

print(all_texts)