
# 📄 Flask BreakFree 2 — AI-Powered Competency & Readiness Report Generator

## 📌 Overview

**Flask BreakFree 2** is a modular Flask web application designed to:

* Read participant assessment data from Excel files.
* Generate **AI-powered Competency Reports**, **Readiness Analysis**, and **Summaries** using LLM functions.
* Create and send **Word/PDF reports** via email.
* Provide both **UI-based** and **API-based** access to report generation.
* Support leader-based aggregated reporting.

---

## 📂 Project Structure

```
flask-breakfree-2/
│
├── app.py                  # Application entry point
├── .env                    # Environment variables (DB, email, API keys, etc.)
├── requirements.txt        # Python dependencies
├── readme.md                # Documentation (this file)
│
└── application/
    ├── __init__.py         # Flask app factory, DB setup, blueprint registration
    │
    ├── config/             # Application configuration
    │   ├── __init__.py
    │   └── settings.py     # Paths, constants, and configs
    │
    ├── controllers/        # Business logic for reports
    │   ├── data_service.py         # Data fetching from DB
    │   ├── llm_competency.py       # Generate AI-based competency reports
    │   ├── llm_readiness.py        # Prepare readiness data, analysis generation
    │   ├── llm_summary.py          # AI-based summary generation
    │
    ├── middleware/         # (Reserved for request/response middlewares)
    │   └── __init__.py
    │
    ├── models/             # SQLAlchemy ORM models
    │   ├── competencies.py
    │   ├── participant.py
    │   ├── report.py
    │
    ├── routes/             # API and web routes
    │   ├── llmroutes.py    # (Optional) Additional LLM endpoints
    │   ├── llmwork.py      # Main LLM-based reporting routes
    │
    ├── scores/             # Excel score data storage
    │   ├── excel_data_proper.xlsx
    │   ├── old_assement_score.xlsx
    │   └── readliness_score_old_data.xlsx
    │
    └── utils/              # Helper utilities
        ├── emailer.py      # Email sending
        ├── excel.py        # Excel reading functions
        ├── stats.py        # Statistical calculations
        ├── text.py         # Text helpers
        ├── word_report.py  # Word report generation
```

---

## ⚙️ Key Features

### **1. Web UI: `/report_generation`**

* Allows the user to:

  * Select a **participant** or **leader**.
  * Generate a report in **PDF/Word format**.
* Supports **aggregated leader reports** and **Visualize All** mode.
* Reads scores from **multiple Excel files**.
* Calls:

  * `generate_readliness_analysis()` → Creates readiness/application comparison.
  * `generate_competency_report()` → Creates detailed competency insights.
  * `generate_summary()` → Summarizes multiple competencies.
  * `generate_word_report()` → Creates downloadable report.
* Sends the report via `send_email()`.

---

### **2. API Endpoints (JSON-based)**

#### 🔹 **POST** `/api/competency-report`

Generate an AI-powered competency report.

```json
{
  "input_context": {...},  
  "candidate_name": "Alice"
}
```

Returns:

```json
{ "report": "...AI-generated report..." }
```

---

#### 🔹 **POST** `/api/summary`

Generate a high-level AI summary of participant performance.

```json
{
  "summary_data": [
    {"competency": "Communication", "application_score": 3.2, ...}
  ],
  "candidate_first_name": "Alice"
}
```

---

#### 🔹 **POST** `/api/readiness-analysis`

Analyze readiness vs application scores.

```json
{
  "analysis_rows": [
    {"Competency": "Communication", "Readiness": 3.4, "Application": 3.1}
  ],
  "candidate_first_name": "Alice"
}
```

---

#### 🔹 **GET** `/hello`

Simple health check endpoint.

```json
{"message": "Hello from LLM blueprint!"}
```

---

### **3. Background**

* Uses **PostgreSQL** via SQLAlchemy for storing report metadata.
* Uses **Flask-Mail** for sending reports as email attachments.
* Modular **Blueprint** structure for scalability.

---

## 🔑 Environment Variables (`.env`)

Example:

```env
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host/dbname
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_USE_TLS=False
MAIL_USE_SSL=True
```

---

## 🚀 Running the Application

```bash
# 1️⃣ Install dependencies
pip install -r requirements.txt

# 2️⃣ Set environment variables
cp .env.example .env

# 3️⃣ Run the server
python app.py
```

Access at:
🔗 **Web UI:** `http://localhost:5000/report_generation`
🔗 **API:** `http://localhost:5000/api/...`

# 4. Stage your changes
git add .

# 5. Commit your changes
git commit -m "added new endpoints 1 is for the report generation and others are for the LLM based content generation"