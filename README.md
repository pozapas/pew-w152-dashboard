# Pew W152 — American Trends Panel Analytics Dashboard

Interactive **Streamlit** dashboard for exploring the [Pew Research Center Wave 152 American Trends Panel](https://www.pewresearch.org/) (August 2024, *N* = 5,410).

## Topics Covered

| Theme | Content |
|-------|---------|
| **AI Perceptions** | Awareness, excitement vs concern, future impact across sectors, job displacement, human vs AI, chatbot usage, trust, fairness/discrimination, regulation |
| **Driving Safety** | Driving frequency, perceived hazard types (cellphone, speeding, DUI, aggressive driving), safety trends, road rage |
| **Statistical Analysis** | Chi-square tests, Cramér's V effect sizes, weighted proportions with 95% CIs, interactive cross-tabulations |

## Getting Started

### 1. Clone & install

```bash
git clone https://github.com/pozapas/pew-w152-dashboard.git
cd pew-w152-dashboard
pip install -r requirements.txt
```

### 2. Add data

Place `ATP W152.csv` (from Pew Research Center) in the project root.  
**⚠️ Data is not included** — download from your licensed Pew account.

### 3. Run

```bash
streamlit run app.py
```

## Data Privacy

All data files (`*.csv`, `*.sav`, `*.xlsx`, `*.pdf`) are excluded via `.gitignore` and are **never committed** to this repository.

## License

Research use only. Survey data is copyright © Pew Research Center.
