import os
import sys
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
    image_base64 = load_image(image_path)  # Görüntüyü base64 formatına dönüştür
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "image_url",  # Burada 'image_url' kullanıyoruz, load_image'den dönen base64 string.
            "image_url": image_base64
        },
    )
    return ocr_response

# Çıktıyı metin dosyasına kaydetme
def save_output_to_file(output, file_name="ocr_output.txt"):
    # 'test' klasörüne yolu ayarla
    output_dir = os.path.join(os.path.dirname(__file__), 'test')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, file_name)

    with open(output_path, "w", encoding="utf-8") as f:
        for page in output.pages:
            f.write(f"Sayfa {page.index + 1}:\n{page.markdown}\n\n")

if __name__ == "__main__":
    # Komut satırından gelen dosya yolu parametresini al
    if len(sys.argv) != 2:
        print("Kullanım: python ocr-output.py <dosya_yolu>")
        sys.exit(1)

    image_path = sys.argv[1]  # Komut satırından alınan dosya yolu
    result = perform_ocr(image_path)

    # Çıktı dosyasının ismini ayarla
    file_name = f"ocr_output{os.path.splitext(os.path.basename(image_path))[0]}.txt"

    save_output_to_file(result, file_name)  # Çıktıyı test klasörüne kaydet

    print(f"OCR çıktısı 'test/{file_name}' dosyasına kaydedildi.")
