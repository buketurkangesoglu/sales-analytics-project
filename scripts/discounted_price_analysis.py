import pandas as pd
import matplotlib.pyplot as plt
import os

base = os.path.join(os.path.dirname(__file__), "..")
prod_path = os.path.join(base, "data", "productss.csv")
df = pd.read_csv(prod_path, sep=";", encoding="cp1254", engine="python")

# temizle numeric
df.columns = df.columns.str.strip()
df["Price"] = pd.to_numeric(df["Price"].astype(str).str.replace(r"[^\d\.\-]", "", regex=True), errors="coerce")
df["Discounted Price"] = pd.to_numeric(df["Discounted Price"].astype(str).str.replace(r"[^\d\.\-]", "", regex=True), errors="coerce")

df["Discount_Amount"] = df["Price"] - df["Discounted Price"]
df["Discount_Rate"] = (df["Discount_Amount"] / df["Price"]) * 100

# en yüksek orana göre top10
plot_df = df.dropna(subset=["Discount_Rate"]).sort_values("Discount_Rate", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10,6))
ax.bar(plot_df["ProductName"], plot_df["Discount_Rate"], color="mediumseagreen", edgecolor="black")
ax.set_title("En Yüksek İndirim Oranına Sahip İlk 10 Ürün (%)")
ax.set_ylabel("İndirim Oranı (%)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

img_path = os.path.join(base, "images", "top10_discount_rate.png")
fig.savefig(img_path, dpi=200, bbox_inches="tight")
print("Kaydedildi:", img_path)
plt.show()