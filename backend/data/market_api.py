import json

def fetch_market_data(quarter: str, year: str) -> dict:
    """
    Mocks fetching financial data for the given quarter and year.
    In the future, this will connect to Alpha Vantage or a database.
    """
    # Mock data for demonstration purposes
    return {
        "msci_acwi_return": "10.6%",
        "sp500_return": "12.4%",
        "ytd_gains": "15.2%",
        "record_highs": 21,
        "macro_drivers": [
            "Easing inflation allowed central banks to cut rates.",
            "Strong corporate earnings driven by the technology sector.",
            "Stable geopolitical environment fostering investor confidence."
        ]
    }
