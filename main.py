import pandas as pd
from datetime import datetime
from pdf_tool import make_pdf

TAX_RATE = 0.1

# CSV読み込み
df = pd.read_csv("sumples/sumple_invoice.csv")

# 日付をdatetimeに変換（計算用）
df["date_dt"] = pd.to_datetime(df["date"])

# 表示用（Excel用）
df["date"] = df["date_dt"].dt.strftime("%Y-%m-%d")

# 月別用
df["month"] = df["date_dt"].dt.to_period("M")

# 合計列
df["total"] = df["price"] * df["quantity"]

df = df.drop(columns=["date_dt"])

# 列名を日本語に変更
df = df.rename(columns={
    "date": "日付",
    "area": "エリア",
    "client": "取引先",
    "product": "商品名",
    "project": "案件名",
    "price": "単価",
    "quantity": "数量",
    "total": "合計金額",
    "month": "対象月"
})

today = datetime.now().strftime("%Y%m%d")

# クライアント別処理
for client, client_df in df.groupby("取引先"):

    subtotal = client_df["合計金額"].sum()
    tax = int(subtotal * TAX_RATE)
    grand_total = subtotal + tax

    invoice_no = f"INV-{today}-{client}"

    # 請求情報
    summary = pd.DataFrame([
        ["請求先", client],
        ["請求書番号", invoice_no],
        ["発行日", today],
        ["小計", subtotal],
        ["消費税", tax],
        ["合計金額", grand_total]
    ], columns=["項目", "内容"])

    # Excel出力
    excel_name = f"invoice_{client}_{today}.xlsx"

    with pd.ExcelWriter(excel_name) as writer:
        client_df.to_excel(writer, sheet_name="明細", index=False)
        summary.to_excel(writer, sheet_name="請求情報", index=False)

    # PDF出力用データ作成（明細をPDF形式に変換）
    items = []

    for _, row in client_df.iterrows():
        items.append({
            "name": row["商品名"],
            "price": int(row["単価"]),
            "qty": int(row["数量"])
        })

    # PDFファイル名
    pdf_name = f"invoice_{client}_{today}.pdf"

    # 書類タイプ（estimate / invoice / receipt）
    doc_type = "receipt"

    make_pdf(pdf_name, doc_type, client, grand_total, today, items)

    print("作成:", client)