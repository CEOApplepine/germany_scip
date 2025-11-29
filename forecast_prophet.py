
import pandas as pd
from prophet import Prophet

df = pd.read_csv('/content/germany-scip/data/deliveries_curated.csv')
df = df.groupby('date')['quantity'].sum().reset_index()
df.columns = ['ds','y']

model = Prophet()
model.fit(df)

future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

forecast[['ds','yhat','yhat_lower','yhat_upper']].to_csv('/content/germany-scip/data/forecast.csv', index=False)
print("Forecast saved to forecast.csv")
