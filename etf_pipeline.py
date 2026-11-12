"""Mock ETF price pipeline: load, clean, check quality, plot.
 
Run with --demo to use synthetic prices (no network needed).
"""
import argparse
import numpy as np
import pandas as pd
 
 
def make_demo_prices(seed=42, days=120):
    """Synthetic daily closing prices with deliberate gaps, for demonstration only."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2026-01-01", periods=days)
    data = {}
    for ticker, start in {"AAA": 100.0, "BBB": 50.0, "CCC": 200.0}.items():
        data[ticker] = start * np.exp(np.cumsum(rng.normal(0, 0.01, days)))
    df = pd.DataFrame(data, index=dates)
    df.iloc[[10, 11, 40], 0] = np.nan   # gaps in AAA
    df.iloc[25, 1] = np.nan             # gap in BBB
    df.iloc[60:70, 2] = np.nan          # long gap in CCC
    return df
 
 
def load_prices(tickers, start, end):
    """Download adjusted close prices with yfinance (needs network)."""
    import yfinance as yf
    return yf.download(tickers, start=start, end=end)["Close"]
 
 
def quality_report(df):
    """Return a table of missing-value counts and share per ticker."""
    missing = df.isna().sum()
    report = pd.DataFrame({
        "rows": len(df),
        "missing": missing,
        "missing_pct": (missing / len(df) * 100).round(1),
        "longest_gap_days": [_longest_gap(df[c]) for c in df.columns],
    })
    return report
 
 
def _longest_gap(series):
    longest = current = 0
    for is_missing in series.isna():
        current = current + 1 if is_missing else 0
        longest = max(longest, current)
    return longest
 
 
def clean_prices(df, max_gap=3):
    """Forward-fill gaps up to max_gap days; leave longer gaps missing."""
    return df.ffill(limit=max_gap)
 
 
def plot_prices(df, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ax = (df / df.bfill().iloc[0] * 100).plot(figsize=(7, 3.4))
    ax.set_title("Cleaned prices, rebased to 100 (synthetic demo data)")
    ax.set_ylabel("Index")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="use synthetic data")
    parser.add_argument("--out", default="prices.png")
    args = parser.parse_args()
    raw = make_demo_prices() if args.demo else load_prices(["SPY", "QQQ"], "2025-01-01", "2025-12-31")
    print("DATA QUALITY REPORT (before cleaning)")
    print(quality_report(raw).to_string())
    cleaned = clean_prices(raw)
    print("\nDATA QUALITY REPORT (after cleaning, gaps up to 3 days filled)")
    print(quality_report(cleaned).to_string())
    plot_prices(cleaned, args.out)
    print(f"\nChart saved to {args.out}")
 
 
if __name__ == "__main__":
    main()
