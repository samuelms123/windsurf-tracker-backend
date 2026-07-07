from app.schemas.activities import Summary

def safe_min(current: float | None, new: float | None) -> float:
    if new is None:
        return current
    
    if current is None:
        return new
    
    return min(current, new)

def calculate_summary(activities: list[dict]) -> Summary:
    summary = Summary(
        total_distance=0,
        time_spent=0,
        time_spent_planing=0,
        total_session_count=0,
        top_speed=0,
        fastest_100=None,
        fastest_500=None,
        fastest_1000=None

    )

    for activity in activities:
        summary.total_distance += activity.get('total_distance')
        summary.time_spent += activity.get('elapsed_time')
        summary.time_spent_planing += activity.get('speed_zones').get('planing')
        summary.total_session_count += 1
        summary.top_speed = max(summary.top_speed, activity.get('max_speed'))
        summary.fastest_100 = safe_min(summary.fastest_100, activity.get('fastest_100'))
        summary.fastest_500 = safe_min(summary.fastest_500, activity.get('fastest_500'))
        summary.fastest_1000 = safe_min(summary.fastest_1000, activity.get('fastest_1000'))

    return summary