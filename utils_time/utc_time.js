export function get_utc_now() {
    return new Date();
}

export function get_utc_now_str(fmt = "iso") {
    const now = new Date();
    if (fmt === "iso") {
        return now.toISOString();
    } else if (fmt === "file") {
        const pad = n => n.toString().padStart(2, '0');
        return `${now.getUTCFullYear()}-${pad(now.getUTCMonth() + 1)}-${pad(now.getUTCDate())}_` +
                `${pad(now.getUTCHours())}-${pad(now.getUTCMinutes())}-${pad(now.getUTCSeconds())}`;
    } else if (fmt === "today"){
        const startOfDay = new Date(Date.UTC(
            now.getUTCFullYear(),
            now.getUTCMonth(),
            now.getUTCDate()
        ));
        return startOfDay.toISOString();
    } else {
        throw new Error("Unsupported format. Use 'iso' or 'file'.");
    }
}

export function parse_utc_from_string(timeStr) {
    const [datePart, timePart] = timeStr.split("_");
    const [year, month, day] = datePart.split("-").map(Number);
    const [hour, minute, second] = timePart.split("-").map(Number);
  
    return new Date(Date.UTC(year, month - 1, day, hour, minute, second));
}


export function extractTimeFromFilename(filename) {
    const match = filename.match(/_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json/);
    return match ? match[1] : null;
}

