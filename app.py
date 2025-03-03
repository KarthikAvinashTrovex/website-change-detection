from flask import Flask, render_template, request, redirect, url_for
import datetime
import os
import pytz

app = Flask(__name__)

SCHEDULE_FILE = "change_time.txt"
IST = pytz.timezone("Asia/Kolkata")

def read_schedule():
    """Read the scheduled change time from a file, if it exists."""
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r") as f:
            timestamp_str = f.read().strip()
            if timestamp_str:
                try:
                    # Parse the ISO format string (which includes the offset)
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
        # Use IST for calculating new scheduled change time.
        now_ist = datetime.datetime.now(IST)
        delay_seconds = int(request.form.get("delay_seconds", 0))
        new_schedule = now_ist + datetime.timedelta(seconds=delay_seconds)
        write_schedule(new_schedule)
        return redirect(url_for("index"))
    
    scheduled_change_time = read_schedule()
    # Get the current IST time.
    now_ist = datetime.datetime.now(IST)
    
    # Compare scheduled change time (assumed in IST) with current IST time.
    if scheduled_change_time and now_ist >= scheduled_change_time:
        pdf_link = url_for("static", filename="isecure.pdf")
        fact_sheet_text = "Passive Fund FactSheet for February"
    else:
        pdf_link = url_for("static", filename="ace.pdf")
        fact_sheet_text = "Passive Fund FactSheet for January"
    
    return render_template("index.html",
                           pdf_link=pdf_link,
                           fact_sheet_text=fact_sheet_text,
                           scheduled_change_time=scheduled_change_time,
                           current_ist=now_ist)

if __name__ == "__main__":
    app.run(debug=True)
