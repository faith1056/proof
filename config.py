"""Configuration and constants for FixNaija Intelligence."""

import os
from enum import Enum
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "database"
UPLOADS_DIR = DATA_DIR / "uploads"

# Ensure directories exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Database
DATABASE_PATH = DB_DIR / "fixnaija.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Problem Categories
class ProblemCategory(Enum):
    """Types of civic problems that can be reported."""
    FLOODING = "Flooding"
    DRAINAGE = "Blocked Drainage"
    WASTE = "Waste Accumulation"
    POTHOLE = "Potholes/Road Damage"
    STREETLIGHT = "Broken Streetlights"
    WATER = "Water Problems"
    ENVIRONMENTAL = "Environmental Hazards"
    INFRASTRUCTURE = "Damaged Public Infrastructure"
    SECURITY = "Security Concerns"
    SANITATION = "Sanitation Issues"
    OTHER = "Other"

# Severity Levels
class SeverityLevel(Enum):
    """Severity classification for problems."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

# Report Status
class ReportStatus(Enum):
    """Status of a citizen report."""
    SUBMITTED = "Submitted"
    PROCESSED = "Processed"
    DUPLICATE_IDENTIFIED = "Duplicate Identified"
    ASSIGNED_TO_CASE = "Assigned to Case"

# Case Status (for grouped incidents)
class CaseStatus(Enum):
    """Status of a community case (grouped reports)."""
    SUBMITTED = "Submitted"
    ROUTED = "Routed"
    SENT = "Sent to Authority"
    ACKNOWLEDGED = "Acknowledged by Authority"
    UNDER_REVIEW = "Under Review"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    VERIFIED = "Verified"
    UNRESOLVED = "Unresolved"
    ESCALATED = "Escalated"

# Authority Types
class AuthorityType(Enum):
    """Types of government authorities."""
    LOCAL_GOVERNMENT = "Local Government"
    STATE_AUTHORITY = "State Authority"
    FEDERAL_AUTHORITY = "Federal Authority"
    ENVIRONMENTAL_AGENCY = "Environmental Agency"
    WASTE_MANAGEMENT = "Waste Management Authority"
    INFRASTRUCTURE = "Road/Infrastructure Authority"
    ELECTRICITY = "Electricity Authority"
    WATER = "Water Authority"
    TRANSPORT = "Transport Authority"

# Analysis Parameters
DUPLICATE_DETECTION_DISTANCE_KM = 0.5  # Reports within 500m may be duplicates
DUPLICATE_SIMILARITY_THRESHOLD = 0.7  # Text similarity threshold (0-1)
HOTSPOT_RADIUS_KM = 1.0  # Radius for hotspot clustering
HOTSPOT_MIN_REPORTS = 5  # Minimum reports to identify a hotspot
TREND_ANALYSIS_DAYS = 90  # Days to consider for trend analysis
RECURRENCE_TIME_WINDOW_DAYS = 14  # Days before problem can be classified as recurring
PRIORITY_SCORE_MAX = 100

# Priority Score Weights
PRIORITY_WEIGHTS = {
    "frequency": 0.25,
    "severity": 0.20,
    "recency": 0.20,
    "independent_reporters": 0.15,
    "geographic_concentration": 0.10,
    "trend": 0.10,
}

# File Upload Constraints
MAX_FILE_SIZE_MB = 10
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png", "gif"]
ALLOWED_VIDEO_TYPES = ["mp4", "mov", "avi", "mkv"]

# Coordinates for Nigeria (approximate center)
NIGERIA_CENTER = (9.0820, 8.6753)
NIGERIA_BOUNDS = {  # approximate
    "north": 13.8,
    "south": 4.2,
    "east": 14.7,
    "west": 2.7,
}

# Escalation Configuration
ESCALATION_DAYS = 7  # Days before escalation reminder
MAX_ESCALATIONS = 3  # Maximum escalation attempts before marking unresolved
