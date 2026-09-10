# FixNaija Intelligence

An intelligent civic problem detection, evidence, routing, and accountability platform for Nigeria.

## Core Mission

Transform scattered citizen reports into structured community intelligence that helps authorities understand which problems are recurring, where they are concentrated, how serious they are, whether they are getting worse, and whether previous interventions actually worked.

## Workflow

```
Citizen → Report → Evidence → Intelligence → Authority → Action → Verification → Accountability
```

## Key Features

### Intelligence Engine
- **Duplicate Detection**: Identify when multiple citizens report the same problem
- **Hotspot Detection**: Locate where specific problems occur with unusual frequency
- **Trend Analysis**: Detect if problems are increasing, decreasing, stable, or recurring
- **Priority Scoring**: Explainable scoring based on frequency, severity, recency, and more
- **Failed Resolution Detection**: Flag when problems recur after marked resolution
- **Recurring Problem Detection**: Identify locations with repeated issues

### Authority Routing & Accountability
- Smart routing to appropriate authorities based on location and category
- Evidence-backed case alerts with supporting data
- Status tracking workflow (Submitted → Routed → Sent → Acknowledged → Under Review → In Progress → Resolved → Verified)
- Resolution verification and citizen feedback
- Automatic escalation if no response within configured timeframe

### Community Intelligence Dashboard
- Interactive map-based visualization
- Hotspot and trend charts
- Problems by category, location, and time
- Recurring and failed resolution tracking
- Export community intelligence reports

## Project Structure

```
fixnaija/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration and constants
├── requirements.txt                # Python dependencies
├── data/
│   ├── schema.py                   # Data models and schemas
│   └── sample_data.py              # Sample reports for testing
├── database/
│   ├── __init__.py
│   ├── models.py                   # Database table definitions
│   └── connection.py               # Database initialization and connection
├── analysis/
│   ├── __init__.py
│   ├── cleaning.py                 # Data cleaning and validation
│   ├── duplicates.py               # Duplicate/related report detection
│   ├── hotspots.py                 # Hotspot detection algorithm
│   ├── trends.py                   # Trend analysis
│   ├── recurrence.py               # Recurring problem detection
│   └── priority.py                 # Priority scoring logic
├── authorities/
│   ├── __init__.py
│   ├── routing.py                  # Authority routing logic
│   ├── alerts.py                   # Authority alert management
│   └── jurisdiction.py             # Jurisdiction and authority data
├── reports/
│   ├── __init__.py
│   ├── submission.py               # Report submission handling
│   ├── export.py                   # Report export functionality
│   └── intelligence_report.py      # Intelligence report generation
├── visualization/
│   ├── __init__.py
│   ├── maps.py                     # Map visualizations
│   ├── charts.py                   # Chart and dashboard components
│   └── dashboard.py                # Authority dashboard
├── utils/
│   ├── __init__.py
│   ├── geolocation.py              # Geolocation utilities
│   ├── validators.py               # Input validation
│   └── constants.py                # Constants and enums
└── tests/
    ├── __init__.py
    └── test_analysis.py            # Unit tests for analysis modules
```

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python -c "from database.connection import init_db; init_db()"
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## MVP Roadmap

1. ✅ Project setup and structure
2. Citizen report submission form
3. Database and data models
4. Data cleaning and validation
5. Duplicate/related report detection
6. Basic hotspot detection
7. Trend analysis
8. Priority scoring
9. Authority routing
10. Status tracking
11. Intelligence dashboard
12. Community intelligence reports
13. Advanced ML features

## Design Principles

- **Transform, Don't Just Collect**: The system aggregates reports into intelligence, not just a complaint repository
- **Explainable**: All scores and recommendations must be transparent and justified
- **Evidence-Based**: Every claim is backed by actual data and clear methodology
- **Mobile-First**: Simple, accessible interface for citizen reporting
- **Accountability-Focused**: Track outcomes and verify whether interventions work
- **Nigerian Context**: Designed specifically for Nigerian civic challenges

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Geospatial**: Geopy, Folium
- **Visualization**: Plotly, Matplotlib
- **Database**: SQLite (extensible to PostgreSQL)

## License

MIT License - See LICENSE file for details
