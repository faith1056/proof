"""Duplicate and related report detection."""

from typing import List, Dict, Tuple
import math
from difflib import SequenceMatcher
from config import (
    DUPLICATE_DETECTION_DISTANCE_KM,
    DUPLICATE_SIMILARITY_THRESHOLD
)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers.
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
    
    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts (0-1).
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    matcher = SequenceMatcher(None, text1.lower(), text2.lower())
    return matcher.ratio()


def are_likely_duplicates(report1: Dict, report2: Dict) -> Tuple[bool, Dict]:
    """Determine if two reports are likely duplicates.
    
    Args:
        report1: First report
        report2: Second report
    
    Returns:
        Tuple of (is_duplicate, reasoning)
    """
    reasoning = {
        "distance_km": 0,
        "same_category": False,
        "text_similarity": 0,
        "time_difference_hours": 0,
        "is_duplicate": False,
        "reason": ""
    }
    
    # Check geographic distance
    distance = haversine_distance(
        report1['latitude'], report1['longitude'],
        report2['latitude'], report2['longitude']
    )
    reasoning["distance_km"] = round(distance, 3)
    
    if distance > DUPLICATE_DETECTION_DISTANCE_KM:
        reasoning["reason"] = "Too far apart"
        return False, reasoning
    
    # Check category
    same_category = report1['category'] == report2['category']
    reasoning["same_category"] = same_category
    
    if not same_category:
        reasoning["reason"] = "Different categories"
        return False, reasoning
    
    # Check text similarity
    similarity = text_similarity(
        report1.get('description', ''),
        report2.get('description', '')
    )
    reasoning["text_similarity"] = round(similarity, 3)
    
    if similarity < DUPLICATE_SIMILARITY_THRESHOLD:
        reasoning["reason"] = f"Low text similarity ({similarity:.2%})"
        return False, reasoning
    
    # If we get here, likely a duplicate
    reasoning["is_duplicate"] = True
    reasoning["reason"] = "Geographic proximity, same category, and text similarity"
    
    return True, reasoning


def find_related_reports(new_report: Dict, existing_reports: List[Dict]) -> List[Dict]:
    """Find reports related to a new report.
    
    Args:
        new_report: New report to compare
        existing_reports: List of existing reports
    
    Returns:
        List of related reports with duplicate reasoning
    """
    related = []
    
    for existing_report in existing_reports:
        is_dup, reasoning = are_likely_duplicates(new_report, existing_report)
        if is_dup:
            reasoning['report_id'] = existing_report.get('report_id')
            reasoning['citizen_id'] = existing_report.get('citizen_id')
            related.append(reasoning)
    
    return related
