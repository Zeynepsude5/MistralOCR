import os
import sys
import json
from mistralai import Mistral
from dotenv import load_dotenv
from load import load_image  # load.py'den load_image fonksiyonunu içe aktar

# .env dosyasındaki API anahtarını yükle
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Mistral istemcisini başlat
client = Mistral(api_key=api_key)

# OCR işlemi
def perform_ocr(image_path):
    image_base64 = load_image(image_path)
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "image_url",
            "image_url": image_base64
        },
    )
    return ocr_response

# OCR sonucunu JSON dosyasına kaydetme
def save_output_as_json(output, file_name="ocr_output.json"):
    output_dir = os.path.join(os.path.dirname(__file__), 'test')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, file_name)

    pages_data = []
    for page in output.pages:
        # OCRPageDimensions gibi nested nesneleri düzleştir
        dimensions = page.dimensions
        dimensions_dict = {
            "dpi": dimensions.dpi,
            "height": dimensions.height,
            "width": dimensions.width
        }

        # Tüm veriyi JSON'a uygun şekilde toparla
        page_dict = {
            "index": page.index,
            "markdown": page.markdown,
            "images": page.images,
            "dimensions": dimensions_dict
        }

        pages_data.append(page_dict)

    output_data = {
        "pages": pages_data
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python ocr_output_json.py <dosya_yolu>")
        sys.exit(1)

    image_path = sys.argv[1]
    result = perform_ocr(image_path)

    file_name = f"ocr_output_{os.path.splitext(os.path.basename(image_path))[0]}.json"
    save_output_as_json(result, file_name)

    print(f"OCR çıktısı 'test/{file_name}' dosyasına JSON formatında kaydedildi.")