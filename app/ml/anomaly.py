import pandas as pd
from sklearn.ensemble import IsolationForest

from app.database.queries import get_transactions


def detect_transaction_anomalies(contamination=0.10):
    """
    Transactions tablosundaki islemleri analiz eder
    ve anormal olabilecek islemleri tespit eder.
    """

    transactions = get_transactions()

    if not transactions:
        return []

    df = pd.DataFrame(transactions)

    if len(df) < 5:
        return []

    features = df[["amount"]].copy()

    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    model.fit(features)

    df["anomaly_score"] = model.decision_function(features)
    df["is_anomaly"] = model.predict(features)

    anomalies = df[df["is_anomaly"] == -1].copy()

    return anomalies.to_dict(orient="records")


def get_anomaly_summary():
    """
    Anomali tespitinin ozet bilgisini dondurur.
    """

    transactions = get_transactions()

    if not transactions:
        return {
            "total_transactions": 0,
            "anomaly_count": 0,
            "normal_count": 0,
            "anomalies": []
        }

    anomalies = detect_transaction_anomalies()

    total_transactions = len(transactions)
    anomaly_count = len(anomalies)
    normal_count = total_transactions - anomaly_count

    return {
        "total_transactions": total_transactions,
        "anomaly_count": anomaly_count,
        "normal_count": normal_count,
        "anomalies": anomalies
    }