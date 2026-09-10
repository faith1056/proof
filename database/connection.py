"""Database connection and initialization."""

import sqlite3
from pathlib import Path
from config import DATABASE_PATH, DB_DIR


def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with all required tables."""
    # Ensure database directory exists
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users/Citizens table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS citizens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        citizen_id TEXT UNIQUE NOT NULL,
        name TEXT,
        email TEXT,
        phone TEXT,
        location_state TEXT,
        location_lga TEXT,
        anonymous BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id TEXT UNIQUE NOT NULL,
        citizen_id TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        location_description TEXT,
        state TEXT,
        lga TEXT,
        report_date TIMESTAMP NOT NULL,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'SUBMITTED',
        case_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (citizen_id) REFERENCES citizens(citizen_id),
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )
    """)
    
    # Evidence/Media table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_name TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (report_id) REFERENCES reports(report_id)
    )
    """)
    
    # Cases table (grouped/related reports)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'SUBMITTED',
        priority_score REAL DEFAULT 0,
        priority_reasoning TEXT,
        latitude REAL,
        longitude REAL,
        location_description TEXT,
        state TEXT,
        lga TEXT,
        independent_reporters INTEGER DEFAULT 1,
        total_reports INTEGER DEFAULT 1,
        total_media INTEGER DEFAULT 0,
        first_report_date TIMESTAMP,
        latest_report_date TIMESTAMP,
        routed_to_authority INTEGER,
        resolved_date TIMESTAMP,
        resolution_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (routed_to_authority) REFERENCES authorities(id)
    )
    """)
    
    # Authorities table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authorities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        authority_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        state TEXT,
        lga TEXT,
        email TEXT,
        phone TEXT,
        website TEXT,
        contact_person TEXT,
        jurisdiction_scope TEXT,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Authority Alerts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authority_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT UNIQUE NOT NULL,
        case_id INTEGER NOT NULL,
        authority_id INTEGER NOT NULL,
        sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        acknowledged_date TIMESTAMP,
        status TEXT DEFAULT 'SENT',
        escalation_count INTEGER DEFAULT 0,
        last_escalation_date TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id),
        FOREIGN KEY (authority_id) REFERENCES authorities(id)
    )
    """)
    
    # Status Updates/Audit Trail
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS status_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        from_status TEXT,
        to_status TEXT NOT NULL,
        changed_by TEXT,
        change_reason TEXT,
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id)
    )
    """)
    
    # Resolution Verification
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resolution_verifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        citizen_id TEXT NOT NULL,
        verified BOOLEAN NOT NULL,
        feedback TEXT,
        follow_up_required BOOLEAN DEFAULT 0,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id),
        FOREIGN KEY (citizen_id) REFERENCES citizens(citizen_id)
    )
    """)
    
    # Analysis Results (for caching analysis)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_type TEXT NOT NULL,
        result_data TEXT NOT NULL,
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {DATABASE_PATH}")
