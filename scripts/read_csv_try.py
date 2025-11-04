import pandas as pd

def safe_read(path):
    encodings = ["utf-8", "cp1254", "latin1", "cp1252"]
    seps = [";", ",", "\t"]
    for enc in encodings:
        for sep in seps:
            try:
                df = pd.read_csv(path, sep=sep, engine="python", encoding=enc)
                print(f"OK: {path} (enc={enc}, sep={repr(sep)}, shape={df.shape})")
                return df
            except Exception:
                continue
    raise RuntimeError(f"Dosya okunamadı: {path}")

if __name__ == "__main__":
    sales = safe_read(r"..\data\saless.csv")
    products = safe_read(r"..\data\productss.csv")
    customers = safe_read(r"..\data\customerss.csv")
    print("\nSales columns:", sales.columns.tolist())
    print("Products columns:", products.columns.tolist())
    print("Customers columns:", customers.columns.tolist())