from flask import Flask, jsonify

from etf_pipeline import make_demo_prices, quality_report

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/quality")
def quality():
    report = quality_report(make_demo_prices())
    return jsonify(report.reset_index(names="ticker").to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
