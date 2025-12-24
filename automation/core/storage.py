# core/storage.py
import csv

def save_csv(data: dict, path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data.keys())
        writer.writerow(data.values())
