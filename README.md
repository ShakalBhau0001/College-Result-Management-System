# 🎓 College Result Management System

**College Result Management System** is a **Streamlit-based web application** that turns official university result PDFs into an **interactive, analyzable dashboard**, built with **Python, pdfplumber, pandas, and matplotlib**.

The system **parses semester result PDFs**, extracts every student's marks and status, and instantly surfaces performance dashboards, division-wise analysis, subject-wise trends, and top-scorer rankings — with one-click Excel/PDF export for reporting.

This project demonstrates **PDF text-mining, data parsing, statistical visualization, and report generation workflows**, making it ideal for academic mini-projects and portfolio showcases.

---

## ✨ Key Principles

1. **Parse Once, Analyze Everywhere** – A single PDF upload powers every dashboard page via shared session state
2. **Fail-Safe Parsing** – Defensive extraction so one malformed record can't crash the whole report
3. **Report Ready** – One-click Excel and PDF export for any analysis view

This system is both **practical and educational**, demonstrating how raw, unstructured PDF data can be turned into structured, decision-ready insights using Python and Streamlit.

---

## 🧩 System Overview

The application is built around uploading a single result PDF, which then powers seven analysis modules:

### 📤 Upload

- Upload a university result PDF
- Automatic extraction of Seat No, Name, PRN No, Status, Percentage, and subject-wise marks
- Skips unreadable records instead of failing the whole upload

### 📊 Dashboards

- Performance Dashboard – average %, pass rate, percentage distribution
- Division Analysis – custom percentage-range & status filtering with charts
- Pass/Fail Analysis – pass/fail breakdown with visual comparison
- Subject-wise Analysis – average marks & pass rate per subject
- Top Students – top performers above 89%
- Student Search – look up any student's detailed subject-wise marksheet

### 📤 Reports

- Export division-wise results to PDF or CSV
- Export a full subject-wise marks Excel sheet for the entire class

---

## 🔗 Core Workflow

- User uploads a result PDF on the Upload page
- `pdfplumber` extracts text and regex-based parsing builds structured student records
- Parsed data is cached in Streamlit session state for the whole session
- Every dashboard page reads from that shared state and renders live charts
- Any table view can be exported to PDF, CSV, or Excel

> Turns a static result PDF into a live, explorable analytics dashboard in one upload.

---

## ⚙️ Features

- Python web-based application (`Streamlit`)
- PDF result parsing (`pdfplumber` + `regex extraction`)
- Performance dashboard with histogram + density curve
- Custom division/percentage-range analysis with PDF & CSV export
- Pass/Fail breakdown with pie & bar charts
- Subject-wise average marks & pass-rate analysis
- Top-students leaderboard (>89%) with pie & bar charts
- Student search with full subject-wise marksheet view
- Full-class Excel report export (`openpyxl`)
- Defensive parsing — malformed/missing fields are skipped, not crashed on
- Modular page-per-feature architecture

---

## 📁 Project Structure

```bash
College-Result-Management-System/
│
├── assets/                        # Static assets (logo, images, screenshots)
│
├── pages/
│   ├── __init__.py
│   ├── utils.py                   # Shared safe-parsing helpers & status colors
│   ├── upload_pdf.py              # PDF upload & extraction
│   ├── dashboard.py               # Performance dashboard
│   ├── division_analysis.py       # Custom division/percentage analysis
│   ├── pass_fail_analysis.py      # Pass/Fail breakdown
│   ├── subject_analysis.py        # Subject-wise analysis
│   ├── top_students.py            # Top students leaderboard
│   ├── student_search.py          # Student search & marksheet view
│   └── excel_report.py            # Full-class Excel report export
│
├── main.py                        # Entry Point
├── requirements.txt               # Dependencies
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

- Python 3.10+
- Streamlit
- pip package manager

### 2️⃣ Clone Repository

```bash
git clone https://github.com/ShakalBhau0001/College-Result-Management-System.git
cd College-Result-Management-System
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
streamlit run main.py
```

### 5️⃣ Use the App

- Open **Upload PDF** from the sidebar and upload a result PDF
- Switch between dashboard pages from the sidebar to explore the results

---

## 🔑 Modules

### Upload PDF Page

- Upload a result PDF
- Extracts Seat No, Name, PRN No, Status, Percentage, and subject-wise marks
- Reports how many records were skipped, if any

### Performance Dashboard

- Key metrics: average percentage, pass rate, total students
- Percentage distribution histogram with density curve
- Status distribution pie chart

### Division Analysis

- Custom min/max percentage range and status filters
- Status & percentage-band pie charts, distribution histogram
- Download filtered results as PDF or CSV

### Pass/Fail Analysis

- Pass/Fail counts and comparison charts
- Filterable data table (All / Passed / Failed)

### Subject-wise Analysis

- Average marks and pass rate per subject
- Handles grace-mark (`* 5`) and ATKT carry-forward (`$20+10`) notations correctly

### Top Students

- Top performers with percentage above 89%
- Pie and horizontal bar chart ranking

### Student Search

- Search by Seat No or Name
- Full subject-wise marksheet with per-subject marks chart

### Generate Excel Report

- Full-class subject-wise Excel sheet
- Correctly aligns each student's marks under the right subject column, even if subject order differs between students

---

## 🧠 Analysis Logic

|      Feature          |                Description                    |
|-----------------------|-----------------------------------------------|
| Performance Dashboard | Histogram + KDE of overall percentage         |
| Division Analysis     | Custom percentage-range & status filtering    |
| Pass/Fail Analysis    | Pass vs Fail/ATKT breakdown                   |
| Subject-wise Analysis | Average marks & pass rate per subject         |
| Top Students          | Leaderboard for percentage > 89%              |
| Student Search        | Full marksheet lookup per student             |
| Excel Report          | Subject-aligned Excel export for entire class |

> All charts and stats are computed live from the uploaded PDF for the current session — no database required.

---

## 🗄️ Data Model

### Student Record (short form)

```json
{
  "Seat No": "10001",
  "Name": "RAHUL SHARMA",
  "Percentage": "78.50",
  "Status": "Pass"
}
```

### Student Record (detailed, per subject)

```json
{
  "Seat No": "10001",
  "Name": "RAHUL SHARMA",
  "PRN No": "202301078058278",
  "Status": "Pass",
  "Percentage": "78.50",
  "Code": ["BCA-101", "ECS-201", "CC-301"],
  "UA": ["30", "28", "25"],
  "CA": ["15", "14", "13"],
  "Total": ["45", "42", "38"],
  "Status1": ["P", "P", "P"]
}
```

---

## 🖼️ Screenshots

### 1. Upload PDF

![Preview](assets/CRMS-UPLOAD.png)

### 2. Performance Dashboard

![Preview](assets/CRMS-DASH.png)

### 3. Division Analysis

![Preview](assets/CRMS-DIV.png)

### 4. Pass/Fail Analysis

![Preview](assets/CRMS-PF.png)

### 5. Subject-wise Analysis

![Preview](assets/CRMS-SUB.png)

### 6. Top Students

![Preview](assets/CRMS-TOP.png)

### 7. Student Search

![Preview](assets/CRMS-SEARCH.png)

### 8. Excel Report

![Preview](assets/CRMS-REPORT.png)

---

## 🛣️ Future Improvements

- Multi-PDF batch upload & year-over-year comparison
- Admin login/authentication
- Persistent database storage (currently session-only)
- Email report generator
- Support for additional university result PDF formats

---

## 🙏 Acknowledgments

- Python community
- Streamlit
- pdfplumber
- Open-source contributors

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Contributors

> **Developer: Shakal Bhau & Rajlaxmi Patil**

> **GitHub: [ShakalBhau0001](https://github.com/ShakalBhau0001) & [Rajlaxmi-1307](https://github.com/Rajlaxmi-1307)**

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!

---
