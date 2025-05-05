from datetime import datetime, timezone

def get_utc_now():
    return datetime.now(timezone.utc)

def get_utc_now_str(fmt="iso"):
    now = datetime.now(timezone.utc)
    if fmt == "iso":
        return now.isoformat()
    elif fmt == "file":
        return now.strftime("%Y-%m-%d_%H-%M-%S")
    elif fmt == "today":
        return now.strftime("%Y-%m-%d")
    else:
        raise ValueError("Unsupported format. Use 'iso' or 'file'.")
    

def parse_utc_from_string(time_str):
    dt = datetime.strptime(time_str, "%Y-%m-%d_%H-%M-%S")
    return dt.replace(tzinfo=timezone.utc)