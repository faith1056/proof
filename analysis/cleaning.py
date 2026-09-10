"""Data cleaning and validation for reports."""

import re
from typing import Dict, Tuple, Optional
from datetime import datetime
import numpy as np


def clean_text(text: str) -> str:
    """Clean and normalize text data.
    
    Args:
        text: Raw text to clean
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower().strip()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters except punctuation
    text = re.sub(r'[^a-z0-9\s.,!?-]', '', text)
    
    return text


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """Validate geographic coordinates.
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return False, "Coordinates must be numeric"
    
    if not (-90 <= latitude <= 90):
        return False, f"Latitude must be between -90 and 90, got {latitude}"
    
    if not (-180 <= longitude <= 180):
        return False, f"Longitude must be between -180 and 180, got {longitude}"
    
    # Check if within reasonable bounds for Nigeria
    if not (4.2 <= latitude <= 13.8 and 2.7 <= longitude <= 14.7):
        return False, "Coordinates appear to be outside Nigeria"
    
    return True, ""


def validate_date(date_value: datetime) -> Tuple[bool, str]:
    """Validate report date.
    
    Args:
        date_value: Date to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(date_value, datetime):
        return False, "Date must be a datetime object"
    
    if date_value > datetime.now():
        return False, "Report date cannot be in the future"
    
    # Check if not too old (more than 1 year)
    days_old = (datetime.now() - date_value).days
    if days_old > 365:
        return False, "Report is more than 1 year old"
    
    return True, ""


def normalize_phone(phone: str) -> Optional[str]:
    """Normalize Nigerian phone numbers.
    
    Args:
        phone: Raw phone number
    
    Returns:
        Normalized phone number or None if invalid
    """
    if not phone:
        return None
    
    # Remove non-digits
    digits = re.sub(r'\D', '', phone)
    
    # Check length
    if len(digits) < 10:
        return None
    
    # Nigerian numbers are 11 digits starting with 0, or 12 digits starting with +234
    if len(digits) == 11 and digits.startswith('0'):
        return digits
    elif len(digits) == 12 and digits.startswith('234'):
        return '0' + digits[3:]
    
    return None


def validate_email(email: str) -> bool:
    """Validate email address.
    
    Args:
        email: Email to validate
    
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) if email else False


def clean_report_data(report_dict: Dict) -> Tuple[Dict, list]:
    """Clean an entire report dictionary.
    
    Args:
        report_dict: Raw report data
    
    Returns:
        Tuple of (cleaned_data, list_of_errors)
    """
    errors = []
    cleaned = report_dict.copy()
    
    # Clean text fields
    for field in ['description', 'location_description']:
        if field in cleaned:
            cleaned[field] = clean_text(cleaned[field])
            if not cleaned[field]:
                errors.append(f"{field} cannot be empty")
    
    # Validate coordinates
    if 'latitude' in cleaned and 'longitude' in cleaned:
        is_valid, error = validate_coordinates(cleaned['latitude'], cleaned['longitude'])
        if not is_valid:
            errors.append(error)
    
    # Validate date
    if 'report_date' in cleaned:
        is_valid, error = validate_date(cleaned['report_date'])
        if not is_valid:
            errors.append(error)
    
    # Normalize phone
    if 'phone' in cleaned and cleaned['phone']:
        normalized = normalize_phone(cleaned['phone'])
        if normalized:
            cleaned['phone'] = normalized
        else:
            errors.append("Invalid phone number format")
    
    # Validate email
    if 'email' in cleaned and cleaned['email']:
        if not validate_email(cleaned['email']):
            errors.append("Invalid email format")
    
    return cleaned, errors
