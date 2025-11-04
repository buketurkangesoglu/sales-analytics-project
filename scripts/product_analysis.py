import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
images_dir = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(images_dir, exist_ok=True)

# oku
df = pd.read_csv(os.path.join(data_dir, "productss.csv"), sep=";", encoding="cp1254", engine="python")

# temizle (örnek)
df.columns = df.columns.str.strip()
df["Price"] = pd.to_numeric(df["Price"].astype(str).str.replace(r"[^\d\.\-]", "", regex=True), errors="coerce")

# Price Category bazında ortalama fiyat
avg_price = df.groupby("Price Category")["Price"].mean().sort_values(ascending=False)

# çiz ve kaydet
fig, ax = plt.subplots(figsize=(8,5))
avg_price.plot(kind="bar", ax=ax)
ax.set_title("Price Category Bazında Ortalama Fiyat")
ax.set_ylabel("Ortalama Fiyat (₺)")
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
plt.xticks(rotation=20, ha="right")
plt.tight_layout()

out_path = os.path.join(images_dir, "product_price_category.png")
fig.savefig(out_path, dpi=200, bbox_inches="tight")
print("Kaydedildi:", out_path)
plt.show()