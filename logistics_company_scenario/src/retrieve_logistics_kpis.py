import os
from dotenv import load_dotenv
# Import functions

from qualifying_data import qualify_logistics_company_data
from visualising_data import bar_chart, line_chart, heatmap_chart, scatter_graph
# Load environment variables
load_dotenv()

CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")

data = qualify_logistics_company_data(CSV_FILE_PATH)

KPIS = data['kpis']
dataframe = data['df']

print(KPIS['service_summary'])
# Visualise the data

bar_chart(x_axis = "service_type", y_axis = "late_rate", title = "Late Rate by Service Type", x_lable = "Service Type", y_lable = "Late Rate", data =KPIS['service_summary'])

line_chart(x_axis ="month", y_axis="late_rate", title = "Monthly Late Rate Trend", x_lable = "Month", y_lable = "Late Rate",  data=KPIS['monthly_summary'], marker = 'o')

heatmap_chart(df = dataframe, title = "Late Rate by Region and Service Type")

scatter_graph(x_axis = "delivery_time_minutes", y_axis = "customer_rating", title = "Delivery Time vs Customer Rating", hue = "service_type", data=dataframe)
