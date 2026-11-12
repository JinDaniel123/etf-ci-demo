import numpy as np
import pandas as pd
from etf_pipeline import clean_prices, quality_report, make_demo_prices
from app import app
 
 
def test_quality_report_counts_missing():
    df = pd.DataFrame({"A": [1.0, np.nan, np.nan, 4.0]})
    report = quality_report(df)
    assert report.loc["A", "missing"] == 2
    assert report.loc["A", "longest_gap_days"] == 2
 
 
def test_clean_fills_short_gaps_only():
    df = pd.DataFrame({"A": [1.0, np.nan, np.nan, np.nan, np.nan, 6.0]})
    cleaned = clean_prices(df, max_gap=3)
    assert cleaned["A"].isna().sum() == 1  # 4-day gap: only 3 filled
 
 
def test_demo_data_has_gaps():
    assert make_demo_prices().isna().sum().sum() > 0
 
 
def test_health_endpoint():
    client = app.test_client()
    assert client.get("/health").get_json() == {"status": "ok"}
