# src/evaluation.py
import os
import sys
import csv
from datetime import datetime
import Levenshtein

def calculate_accuracy(predicted: str, ground_truth: str) -> float:
    distance = Levenshtein.distance(predicted, ground_truth)
    max_len = max(len(predicted), len(ground_truth))
    return 1 - distance / max_len if max_len > 0 else 1.0

def main(pred_file_path):
    # Tahmin dosyasının adını al
    file_name = os.path.basename(pred_file_path)
    file_stem, ext = os.path.splitext(file_name)

    # Hangi klasörden geldiğini anla
    if "pred_hw" in pred_file_path:
        gt_path = f"../dataset/handwritten/{file_stem}.txt"
        type_label = "hw"
    elif "pred_mix" in pred_file_path:
        gt_path = f"../dataset/mixed/{file_stem}.txt"
        type_label = "mix"
    elif "pred_prt" in pred_file_path:
        gt_path = f"../dataset/printed/{file_stem}.txt"
        type_label = "prt"
    else:
        print("Klasör tipi belirlenemedi.")
        return

    if not os.path.exists(gt_path):
        print(f"Ground truth bulunamadı: {gt_path}")
        return

    with open(pred_file_path, 'r', encoding='utf-8') as f_pred:
        pred_text = f_pred.read().strip()

    with open(gt_path, 'r', encoding='utf-8') as f_gt:
        gt_text = f_gt.read().strip()

    acc = calculate_accuracy(pred_text, gt_text)
    acc_percent = round(acc * 100, 2)

    # CSV'ye yaz
    result_file = "../results/eval_resultstxt.csv"
    write_header = not os.path.exists(result_file)

    with open(result_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(["type", "file", "accuracy (%)"])
        writer.writerow([type_label, file_name, acc_percent])

    print(f"{file_name} için doğruluk: {acc_percent:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python evaluation_txt.py results/pred_hw/1.txt")
    else:
        main(sys.argv[1])
