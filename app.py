from flask import Flask, render_template, url_for
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    # Initially, show the January PDF (ace.pdf)
    pdf_link = url_for('static', filename='ace.pdf')
    fact_sheet_text = "Passive Fund FactSheet for January"
    return render_template("index.html", pdf_link=pdf_link, fact_sheet_text=fact_sheet_text)

if __name__ == "__main__":
    app.run(debug=True)
