# 請求書自動作成ツール
CSVファイルから、Excel請求書 ＋ PDF請求書を自動生成するPythonツールです。フリーランス・個人事業主向けに作成しました。

---

## 主な機能

- CSVから自動集計
- クライアント別請求書作成
- Excel / PDF同時出力
- ロゴ表示対応
- 見積・請求・領収 切替対応
- 明細付き請求書生成
- ワンクリック実行（GUI対応）

---

## 使用技術

- Python 3
- pandas
- reportlab
- openpyxl
- tkinter（簡易GUI）

---

## 使い方

### ① CSVを準備

data/invoice.csvに以下形式で入力：

date,area,client,product,project,price,quantity

2026-02-01,東京,ABC商事,Web制作,HP制作,50000,1


### ② 実行

% python3 app.py

請求書を作成するを押す

### ③ 出力

- Excel請求書：invoice_取引先_日付.xlsx
- PDF請求書：invoice_取引先_日付.pdf

が自動生成されます。


## 書類切替

main.pyの以下を変更：
doc_type = "invoice"

入力する値:書類

estimate:見積書

invoice:請求書

receipt:領収書

---

## サンプルPDF

- [見積書サンプル](samples/sumple_estimte.ABC商事.pdf)
- [見積書サンプル](samples/sumple_estimte.XYZ株式会社.pdf)
- [請求書サンプル](samples/sumple_invoice.ABC商事.pdf)
- [請求書サンプル](samples/sumple_invoice.XYZ株式会社.pdf)
- [領収書サンプル](samples/sumple_receipt.ABC商事.pdf)
- [領収書サンプル](samples/sumple_receipt.XYZ株式会社.pdf)

👤 Author
	•	Name:稲荷
	•	GitHub: https://github.com/inari-auto

## License

MIT License
