import sqlite3
import pandas as pd
import numpy as np

# Connect to SQLite database
db_name = 'sap_logistics_analysis.db'
conn = sqlite3.connect(db_name)

# Load shipping data into a DataFrame
query = "SELECT * FROM LIKP_Shipping_Logistics"
df = pd.read_sql(query, conn)

print(f"Loaded {len(df)} records from '{db_name}' for anomaly analysis.")

# Statistical Anomaly Detection using Z-Score & IQR on LeadTimeVariance
mean_var = df['LeadTimeVariance'].mean()
std_var = df['LeadTimeVariance'].std()

# Calculate Z-score for lead time variance
df['ZScore'] = (df['LeadTimeVariance'] - mean_var) / std_var

# Flag anomalies where Z-score > 2.0 (approx. top 5% outliers) or variance > 4 days
df['IsAnomaly'] = np.where((abs(df['ZScore']) > 2.0) | (df['LeadTimeVariance'] > 4.0), 1, 0)

# Filter and save flagged anomalies to a dedicated table and CSV report
df_anomalies = df[df['IsAnomaly'] == 1]
df_anomalies.to_sql('logistics_anomalies', conn, if_exists='replace', index=False)
df_anomalies.to_csv('anomaly_audit_report.csv', index=False)

conn.close()

print(f"Anomaly detection complete! Flagged {len(df_anomalies)} shipping anomalies.")
print(f"Saved audit report to 'anomaly_audit_report.csv' and updated database '{db_name}'.")
print("\nSample Flagged Anomalies:")
print(df_anomalies[['DeliveryID', 'Carrier', 'ShippingRoute', 'PlannedLeadTimeDays', 'ActualLeadTimeDays', 'LeadTimeVariance']].head())