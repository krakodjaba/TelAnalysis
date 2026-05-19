import json
import jmespath
from datetime import datetime
from collections import Counter, defaultdict
from typing import List, Dict, Any
from . import utils


def parse_timestamp(timestamp: int) -> datetime:
    """
    Parse Unix timestamp to datetime object.
    """
    try:
        return datetime.fromtimestamp(timestamp)
    except (TypeError, ValueError):
        return None


def analyze_activity_by_hour(messages: List[Dict]) -> Dict[str, int]:
    """
    Analyze message activity by hour of day (0-23).
    """
    hour_activity = defaultdict(int)
    
    for msg in messages:
        timestamp = msg.get('date')
        if timestamp:
            dt = parse_timestamp(timestamp)
            if dt:
                hour_activity[dt.hour] += 1
    
    # Fill missing hours with 0
    for hour in range(24):
        if hour not in hour_activity:
            hour_activity[hour] = 0
    
    return dict(sorted(hour_activity.items()))


def analyze_activity_by_day(messages: List[Dict]) -> Dict[str, int]:
    """
    Analyze message activity by day of week.
    """
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_activity = defaultdict(int)
    
    for msg in messages:
        timestamp = msg.get('date')
        if timestamp:
            dt = parse_timestamp(timestamp)
            if dt:
                day_activity[day_names[dt.weekday()]] += 1
    
    # Fill missing days with 0
    for day in day_names:
        if day not in day_activity:
            day_activity[day] = 0
    
    return dict(sorted(day_activity.items(), key=lambda x: day_names.index(x[0])))


def analyze_activity_by_month(messages: List[Dict]) -> Dict[str, int]:
    """
    Analyze message activity by month.
    """
    month_activity = defaultdict(int)
    
    for msg in messages:
        timestamp = msg.get('date')
        if timestamp:
            dt = parse_timestamp(timestamp)
            if dt:
                month_key = dt.strftime('%Y-%m')
                month_activity[month_key] += 1
    
    return dict(sorted(month_activity.items()))


def calculate_message_frequency(messages: List[Dict]) -> Dict[str, Any]:
    """
    Calculate message frequency statistics.
    """
    if not messages:
        return {"error": "No messages for frequency analysis"}
    
    timestamps = []
    for msg in messages:
        timestamp = msg.get('date')
        if timestamp:
            dt = parse_timestamp(timestamp)
            if dt:
                timestamps.append(dt)
    
    if not timestamps:
        return {"error": "No valid timestamps found"}
    
    timestamps.sort()
    
    # Calculate time span
    time_span = (timestamps[-1] - timestamps[0]).days
    
    if time_span == 0:
        time_span = 1  # Avoid division by zero
    
    # Calculate messages per day
    messages_per_day = len(timestamps) / time_span
    
    # Calculate average time between messages
    time_intervals = []
    for i in range(1, len(timestamps)):
        interval = (timestamps[i] - timestamps[i-1]).total_seconds() / 60  # in minutes
        time_intervals.append(interval)
    
    avg_interval = sum(time_intervals) / len(time_intervals) if time_intervals else 0
    
    return {
        "total_messages": len(timestamps),
        "time_span_days": time_span,
        "messages_per_day": round(messages_per_day, 2),
        "average_interval_minutes": round(avg_interval, 2),
        "first_message": timestamps[0].strftime('%Y-%m-%d %H:%M:%S'),
        "last_message": timestamps[-1].strftime('%Y-%m-%d %H:%M:%S')
    }


def analyze_peak_activity_times(messages: List[Dict]) -> Dict[str, Any]:
    """
    Identify peak activity times.
    """
    hour_activity = analyze_activity_by_hour(messages)
    day_activity = analyze_activity_by_day(messages)
    
    # Find peak hour
    peak_hour = max(hour_activity.items(), key=lambda x: x[1])
    
    # Find peak day
    peak_day = max(day_activity.items(), key=lambda x: x[1])
    
    return {
        "peak_hour": {"hour": peak_hour[0], "message_count": peak_hour[1]},
        "peak_day": {"day": peak_day[0], "message_count": peak_day[1]},
        "hourly_distribution": hour_activity,
        "daily_distribution": day_activity
    }


def analyze_user_activity_over_time(messages: List[Dict]) -> Dict[str, Any]:
    """
    Analyze user activity patterns over time.
    """
    user_activity = defaultdict(lambda: defaultdict(int))
    
    for msg in messages:
        user_id = msg.get('from_id')
        timestamp = msg.get('date')
        if user_id and timestamp:
            dt = parse_timestamp(timestamp)
            if dt:
                month_key = dt.strftime('%Y-%m')
                user_activity[user_id][month_key] += 1
    
    # Convert to regular dict
    result = {}
    for user_id, activity in user_activity.items():
        result[str(user_id)] = dict(sorted(activity.items()))
    
    return result


def temporal_analysis_from_file(filepath: str) -> Dict[str, Any]:
    """
    Perform temporal analysis on a Telegram export file.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    
    messages = jmespath.search('messages[*]', data) or []
    
    if not messages:
        return {"error": "No messages found for temporal analysis"}
    
    # Perform various temporal analyses
    frequency_stats = calculate_message_frequency(messages)
    peak_activity = analyze_peak_activity_times(messages)
    user_activity = analyze_user_activity_over_time(messages)
    
    return {
        "frequency": frequency_stats,
        "peak_activity": peak_activity,
        "user_activity_over_time": user_activity,
        "total_messages_analyzed": len(messages)
    }
