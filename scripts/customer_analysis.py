import pandas as pd
import matplotlib.pyplot as plt
import os

base = os.path.join(os.path.dirname(__file__), "..")
sales = pd.read_csv(os.path.join(base, "data", "saless.csv"), sep=";", encoding="cp1254", engine="python")
customers = pd.read_csv(os.path.join(base, "data", "customerss.csv"), sep=";", encoding="cp1254", engine="python")

# temizleme
customers = customers.loc[:, ~customers.columns.str.contains("^Unnamed")]
customers.columns = customers.columns.str.strip()
sales.columns = sales.columns.str.strip()

# Total Sales hesap / dönüşüm (eğer yoksa)
if "Total Sales" not in sales.columns:
    if "Quantity" in sales.columns and ("Price" in sales.columns or "Products.Price" in sales.columns):
        price_col = "Price" if "Price" in sales.columns else "Products.Price"
        sales["Total Sales"] = pd.to_numeric(sales["Quantity"], errors="coerce") * pd.to_numeric(sales[price_col], errors="coerce")
    else:
        raise RuntimeError("Total Sales yok ve hesaplayacak Price/Quantity bulunamadı.")
sales["Total Sales"] = pd.to_numeric(sales["Total Sales"].astype(str).str.replace(r"[^\d\.\-]", "", regex=True), errors="coerce")

# merge
merged = pd.merge(sales, customers, on="CustomerID", how="left")

# groupby ve grafik (Top10)
customer_sales = merged.groupby("Name")["Total Sales"].sum().reset_index().sort_values("Total Sales", ascending=False)
top10 = customer_sales.head(10)

fig, ax = plt.subplots(figsize=(10,6))
ax.bar(top10["Name"], top10["Total Sales"], color="steelblue", edgecolor="black")
ax.set_title("En Çok Harcayan 10 Müşteri")
ax.set_ylabel("Toplam Harcama (₺)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

img_path = os.path.join(base, "images", "top10_customers.png")
fig.savefig(img_path, dpi=200, bbox_inches="tight")
print("Kaydedildi:", img_path)
plt.show()