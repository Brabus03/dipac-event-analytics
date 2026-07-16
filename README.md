# 📊 DIPAC Event Intelligence Dashboard

Business Intelligence dashboard untuk menganalisis performa event berdasarkan customer spending, collective income, product performance, dan revenue contribution.

Project ini dikembangkan menggunakan Python dan Streamlit untuk membantu pengambilan keputusan berbasis data pada event management.

---

# 🚀 Features

## 1. Executive Event Report

Dashboard menyediakan ringkasan performa event:

- Customer Spending
- Collective Income
- Profit Contribution
- Commission Rate
- Best Performing Menu
- Business Recommendation

## 2. Transaction Analytics

Analisis transaksi berdasarkan:

- Product category
- Menu performance
- Customer revenue
- Collective share
- Profit contribution

## 3. Event Comparison Dashboard

Membandingkan performa antar event:

- Revenue comparison
- Product performance
- Collective contribution
- Event ranking

## 4. AI Business Insight

Sistem menghasilkan insight berdasarkan:

- Collective contribution ratio
- Product performance
- Revenue pattern
- Sales optimization recommendation

## 5. Executive PDF Report

Dashboard dapat menghasilkan laporan PDF otomatis untuk kebutuhan evaluasi event.

---

# 🖥️ Dashboard Preview

![Dashboard](screenshots/dashboard.png)

![Executive Report](screenshots/executive-report.png)

---

## 🏗 Project Structure

```text
dipac-event-analytics/

├── app.py                         # Main Streamlit dashboard application
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation

├── data/
│   └── events/                    # Raw event transaction datasets
│       ├── jakarta_stalk_white_party/
│       │   └── transactions.csv
│       │
│       ├── semarang_dentra_tnf/
│       │   └── transactions.csv
│       │
│       └── semarang_midnight_cell/
│           └── transactions.csv

├── utils/
│   ├── __init__.py
│   ├── analytics.py               # KPI calculation and menu analysis
│   ├── event_comparison.py        # Multi-event comparison analysis
│   ├── forecasting.py             # Revenue forecasting module
│   └── pdf_report.py              # Automated executive PDF report

├── pages/
│   └── event_comparison.py        # Streamlit comparison page

├── screenshots/
│   ├── dashboard.png              # Dashboard preview
│   ├── executive-report.png       # Executive report preview
│   ├── comparison.png             # Event comparison chart
│   └── menu-performance.png       # Menu performance chart

└── docs/
    ├── Dentra_TNF_Semarang_Report.pdf
    ├── Midnight_In_Cell_Semarang_Report.pdf
    └── White_Party_Report.pdf
```

# 🛠️ Technology Stack

## Programming Language

- Python

## Data Processing

- Pandas

## Visualization

- Streamlit
- Plotly

## Reporting

- FPDF

## Analytics Method

- KPI Analysis
- Revenue Analysis
- Product Performance Analysis
- Comparative Event Analytics

---

## 📈 Business Objective

Project ini bertujuan mengubah data transaksi event menjadi insight bisnis yang dapat digunakan untuk:

- Mengevaluasi performa event
- Mengidentifikasi produk dengan kontribusi terbesar
- Mengoptimalkan strategi penjualan
- Mendukung pengambilan keputusan berbasis data

---

## ⚙️ Installation

### Requirements

- Python 3.10+
- pip

### Setup

Clone repository:

```bash
git clone https://github.com/Brabus03/dipac-event-analytics.git

cd dipac-event-analytics

pip install -r requirements.txt
```

Run dashboard:

```bash
streamlit run app.py
```

📂 Sample Reports

Contoh executive report tersedia pada folder:

docs/

👨‍💻 Author

Brabus03

GitHub:
https://github.com/Brabus03

```

```
