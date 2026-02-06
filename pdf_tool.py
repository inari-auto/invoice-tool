from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.utils import ImageReader
import os

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

def make_pdf(filename, doc_type, client, total, issue_date, items=None):

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # =====================
    # パス設定
    # =====================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "logo.png")

    # =====================
    # 外枠デザイン
    # =====================
    c.setLineWidth(1)
    c.rect(30, 30, width-60, height-60)

    # =====================
    # ロゴ表示
    # =====================
    if os.path.exists(logo_path):

        logo = ImageReader(logo_path)

        LOGO_W = 90
        LOGO_X = width - LOGO_W - 80
        LOGO_Y = height - 220

        c.drawImage(
            logo,
            LOGO_X,
            LOGO_Y,
            width=LOGO_W,
            preserveAspectRatio=True,
            mask='auto'
        )

    # =====================
    # タイトル（書類タイプ対応）
    # =====================
    TITLE_MAP = {
        "estimate": "御 見 積 書",
        "invoice": "請 求 書",
        "receipt": "領 収 書"
    }

    title = TITLE_MAP.get(doc_type, "請 求 書")

    c.setFont("HeiseiKakuGo-W5", 22)
    c.drawCentredString(width/2, height-60, title)

    # =====================
    # 発行元情報
    # =====================
    c.setFont("HeiseiKakuGo-W5", 11)

    c.drawString(50, height-90, "発行元：Trusta")
    c.drawString(50, height-105, "住所：東京都xx区xx1-2-3")
    c.drawString(50, height-120, "TEL：090-xxxx-xxxx")
    c.drawString(50, height-135, "Email：example@gmail.com")

    # =====================
    # 基本情報
    # =====================
    c.setFont("HeiseiKakuGo-W5", 12)

    c.drawString(50, height-165, f"請求先：{client}")
    c.drawString(50, height-190, f"発行日：{issue_date}")

    # =====================
    # 明細エリア枠
    # =====================
    table_top = height - 200
    table_bottom = height - 470

    c.rect(40, table_bottom, width-80, table_top-table_bottom)

    # =====================
    # 明細ヘッダー
    # =====================
    c.setFont("HeiseiKakuGo-W5", 11)

    c.drawString(50, table_top-25, "No")
    c.drawString(90, table_top-25, "商品名")
    c.drawString(260, table_top-25, "単価")
    c.drawString(340, table_top-25, "数量")
    c.drawString(410, table_top-25, "金額")

    # ヘッダー線
    c.line(45, table_top-35, width-45, table_top-35)

    # =====================
    # 明細データ
    # =====================
    y = table_top - 60

    if items:

        for i, item in enumerate(items, 1):

            name = item["name"]
            price = item["price"]
            qty = item["qty"]
            amount = price * qty

            c.drawString(50, y, str(i))
            c.drawString(90, y, name)
            c.drawRightString(310, y, f"¥{price:,}")
            c.drawRightString(370, y, str(qty))
            c.drawRightString(460, y, f"¥{amount:,}")

            y -= 25

    else:
        c.drawString(60, y, "（明細データなし）")

    # =====================
    # 合計欄
    # =====================
    c.setFont("HeiseiKakuGo-W5", 13)

    total_y = table_bottom - 40

    c.line(300, total_y+15, width-45, total_y+15)

    c.drawString(310, total_y, "合計金額：")
    c.drawRightString(width-55, total_y, f"¥{total:,}")

    # =====================
    # メッセージ
    # =====================
    c.setFont("HeiseiKakuGo-W5", 11)

    c.drawString(50, 90, "お振込みをお願いいたします。")
    c.drawString(50, 70, "ご不明点がございましたらご連絡ください。")

    c.save()