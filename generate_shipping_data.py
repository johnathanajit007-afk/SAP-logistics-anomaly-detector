import sqlite3
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Parameters for synthetic SAP logistics dataset
n_records = 1500

delivery_ids = [f"800{str(i).zfill(5)}" for i in range(1, n_records + 1)]
customers = [f"CUST_{str(np.random.randint(100, 150))}" for _ in range(n_records)]
plants = ['PLT_North', 'PLT_South', 'PLT_East', 'PLT_West', 'PLT_Central']
shipping_routes = ['RT_Express_A', 'RT_Standard_B', 'RT_Freight_C', 'RT_Overland_D']
carriers = ['DHL_Freight', 'Kuehne_Nagel', 'FedEx_Supply', 'DB_Schenker']

# Generate baseline planned lead times (in days)
planned_lead_times = np.random.choice([2, 3, 5, 7, 10], size=n_records, p=[0.2, 0.4, 0.25, 0.1, 0.05])

# Generate actual lead times with normal variance plus injected anomalies
actual_lead_times = []
for planned in planned_lead_times:
    if np.random.rand() > 0.15:
        variance = np.random.normal(loc=0.2, scale=0.5)
        actual = max(1, round(planned + variance, 1))
    else:
        spike = np.random.uniform(4.0, 12.0)
        actual = round(planned + spike, 1)
    actual_lead_times.append(actual)

# Create DataFrame
df_shipping = pd.DataFrame({
    'DeliveryID': delivery_ids,
    'CustomerID': customers,
    'Plant': np.random.choice(plants, size=n_records),
    'ShippingRoute': np.random.choice(shipping_routes, size=n_records),
    'Carrier': np.random.choice(carriers, size=n_records),
    'PlannedLeadTimeDays': planned_lead_times,
    'ActualLeadTimeDays': actual_lead_times
})

# Calculate variance / delay delta
df_shipping['LeadTimeVariance'] = df_shipping['ActualLeadTimeDays'] - df_shipping['PlannedLeadTimeDays']

# Save to local SQLite Database
db_name = 'sap_logistics_analysis.db'
conn = sqlite3.connect(db_name)
df_shipping.to_sql('LIKP_Shipping_Logistics', conn, if_exists='replace', index=False)
conn.close()

print(f"Successfully generated {n_records} SAP shipping records and saved to relational database '{db_name}'.")
print(df_shipping.head())