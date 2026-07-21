# 🎓 Student Performance Dashboard

An interactive web dashboard built with [Plotly Dash](https://dash.plotly.com/) that
visualizes student scores across subjects — with filtering, click-to-highlight
charts, and auto-generated insights.

## Features

- 📊 **Bar chart** of each student's average score across all subjects
- 🎯 **Dropdown filter** to select one or more students to display
- 🖱️ **Click-to-highlight**: click a student's bar to see their subject-by-subject
  breakdown in the line chart
- 📈 **Class-wide subject averages** shown in a separate bar chart
- 💡 **Auto-generated text insights** summarizing top performers and trends

## Project structure

```
.
├── dashboard_app.py              # The runnable Dash application
├── dashboard_app_explained.ipynb # Step-by-step notebook walkthrough of the code
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Install dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the app

```bash
python dashboard_app.py
```

Then open your browser to:

```
http://127.0.0.1:8050
```

## How it works

The dashboard uses a small sample dataset of 5 students and their scores across 5
subjects (Math, Science, English, History, Art). Swap in your own data by replacing
the `students`, `subjects`, and `scores_data` variables in `dashboard_app.py` — or
load a CSV with `pandas.read_csv(...)` instead.

For a detailed, section-by-section explanation of the code, see
[`dashboard_app_explained.ipynb`](./dashboard_app_explained.ipynb) — GitHub renders
it directly in the browser, so it doubles as documentation.

## Tech stack

- [Dash](https://dash.plotly.com/) — web app framework
- [Plotly Express](https://plotly.com/python/plotly-express/) — charting
- [Pandas](https://pandas.pydata.org/) — data handling

## License

Add a license of your choice (e.g. MIT) here.
