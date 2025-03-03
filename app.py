from flask import Flask, render_template, request, redirect, url_for
import datetime
import os
from zoneinfo import ZoneInfo  # Python 3.9+

app = Flask(__name__)

SCHEDULE_FILE = "change_time.txt"

def read_schedule():
    """Read the scheduled change time from a file, if it exists."""
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r") as f:
            timestamp_str = f.read().strip()
            if timestamp_str:
                try:
                    return datetime.datetime.fromisoformat(timestamp_str)
                except Exception as e:
                    print("Error parsing schedule:", e)
    return None

def write_schedule(scheduled_time):
    """Write the scheduled change time to a file in ISO format."""
    with open(SCHEDULE_FILE, "w") as f:
        f.write(scheduled_time.isoformat())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the delay in seconds from the form and calculate the new schedule time.
        delay_seconds = int(request.form.get("delay_seconds", 0))
        total_delay = delay_seconds + 19810
        new_schedule = datetime.datetime.now() + datetime.timedelta(seconds=total_delay)
        write_schedule(new_schedule)
        return redirect(url_for("index"))
    
    scheduled_change_time = read_schedule()
    now = datetime.datetime.now()
    # Add 19,800 seconds (5 hours 30 minutes) to now for comparison
    now_with_offset = now + datetime.timedelta(seconds=19810)

    # Check if a schedule exists and whether current time is past it.
    if scheduled_change_time and now_with_offset >= scheduled_change_time:
        pdf_link = url_for("static", filename="isecure.pdf")
        fact_sheet_text = "Passive Fund FactSheet for February"
    else:
        pdf_link = url_for("static", filename="ace.pdf")
        fact_sheet_text = f"Passive Fund FactSheet for January"
    
    # Get current IST time using zoneinfo
    current_ist = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
    
    return render_template("index.html",
                           pdf_link=pdf_link,
                           fact_sheet_text=fact_sheet_text,
                           scheduled_change_time=scheduled_change_time,
                           current_ist=current_ist)

if __name__ == "__main__":
    app.run(debug=True)
