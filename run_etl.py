
import pandas as pd

deliveries = pd.read_csv('/content/germany-scip/data/sample_deliveries.csv')
deliveries['planned_arrival'] = pd.to_datetime(deliveries['planned_arrival'])
deliveries['actual_arrival'] = pd.to_datetime(deliveries['actual_arrival'])
deliveries['lead_time_hours'] = (deliveries['actual_arrival'] - deliveries['planned_arrival']).dt.total_seconds()/3600
deliveries['date'] = pd.to_datetime(deliveries['date']).dt.date
deliveries.to_csv('/content/germany-scip/data/deliveries_curated.csv', index=False)
print("ETL completed. Curated file created.")
