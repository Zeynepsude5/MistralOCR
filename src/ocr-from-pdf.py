import os
import sys
from mistralai import Mistral
from dotenv import load_dotenv

# .env dosyasındaki API anahtarını yükle
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Mistral istemcisini başlat
client = Mistral(api_key=api_key)

# Dosyayı yükleme
def upload_file(pdf_path):
    with open(pdf_path, "rb") as f:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": os.path.basename(pdf_path),
                "content": f,
            },
            purpose="ocr"
        )
    return uploaded_pdf.id

# OCR işlemi

def perform_ocr(file_id):
    # Dosyayı imzalı URL olarak al
    signed_url = client.files.get_signed_url(file_id=file_id)

    # OCR işlemini başlat
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        }
    )
    return ocr_response


# Çıktıyı metin dosyasına kaydetme
def save_output_to_file(output, input_file_name):
    output_dir = os.path.join(os.path.dirname(__file__), 'test')
    os.makedirs(output_dir, exist_ok=True)

    output_file_name = f"{os.path.splitext(input_file_name)[0]}-ocr.txt"
    output_path = os.path.join(output_dir, output_file_name)

    with open(output_path, "w", encoding="utf-8") as f:
        for page in output.pages:
            f.write(f"Sayfa {page.index + 1}:\n{page.markdown}\n\n")

    return output_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python ocr-from-pdf.py <pdf_dosyasi_yolu>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    input_file_name = os.path.basename(pdf_path)

    # Dosyayı yükle
    file_id = upload_file(pdf_path)

    # OCR İşlemini gerçekleştir
    result = perform_ocr(file_id)

    # Çıktıyı kaydet
    output_path = save_output_to_file(result, input_file_name)

    print(f"OCR çıktısı '{output_path}' dosyasına kaydedildi.")

