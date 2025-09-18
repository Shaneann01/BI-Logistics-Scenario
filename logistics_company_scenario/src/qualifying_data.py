import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")

def extract_company_data(csv_file_path, summary=False):
    """
    Extracts data from a CSV file and returns it as a pandas DataFrame.
    """
# Extract the data from the CSV file into a DataFrame
    df = pd.read_csv( rf'{csv_file_path}')

    if summary:
        print(df.info())
        print(df.describe())
        print(df.head())

    return df

def data_cleaning(df):
    """
    Cleans the DataFrame by handling missing values and ensuring correct data types.
    """
                
    # clean duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df['customer_rating'] = df['customer_rating'].fillna(df['customer_rating'].mean())
    
    # Standardise text
    df['region'] = df['region'].str.title().str.strip()
    df['service_type'] = df['service_type'].str.title().str.strip()

    print(f"LATEST DF: {df}")

    return df

def transform_data(df):

     # Convert 'delivery_date' to standard datetime format
    df['delivery_date'] = pd.to_datetime(df['delivery_date'], format='%d/%m/%Y', errors='coerce')

    # Add extra columns to help KPIS
    df['is_late'] = (df['promised_time_minutes'] < df['delivery_time_minutes']).astype(int)

    # Seasonal (by month)
    df['month'] = df['delivery_date'].dt.month

    # Group by service type
    service_summary = df.groupby('service_type').agg(
        total_deliveries=('order_id','count'),
        late_deliveries=('is_late','sum'),
        avg_rating=('customer_rating','mean'),
        avg_duration=('delivery_time_minutes','mean')
    ).reset_index()

    service_summary['late_rate'] = service_summary['late_deliveries'] / service_summary['total_deliveries']
    print(service_summary)

    # Group by region
    region_summary = df.groupby('region').agg(
        total_deliveries=('order_id','count'),
        late_rate=('is_late','mean'),
        avg_rating=('customer_rating','mean')
    ).reset_index()
    print(region_summary)

    

    monthly_summary = df.groupby('month').agg(
        total_deliveries=('order_id','count'),
        late_rate=('is_late','mean'),
        avg_rating=('customer_rating','mean')
    ).reset_index()
    print(monthly_summary)

    # Promotion vs non-promotion
    promo_summary = df.groupby('promotional_campaign_id').agg(
        total_deliveries=('order_id','count'),
        late_rate=('is_late','mean'),
        avg_rating=('customer_rating','mean')
    ).reset_index()
    print(promo_summary)

    # Repeat customers (count how many >1 order)
    repeat = df.groupby('customer_id').size().reset_index(name='orders')
    repeat_summary = repeat.sort_values(by='orders', ascending = False)
    print(repeat_summary)

    return {
        'service_summary': service_summary,
        'region_summary': region_summary,
        'monthly_summary': monthly_summary,
        'promo_summary': promo_summary,
        'repeat_summary': repeat_summary
    }

def qualify_logistics_company_data(csv_file_path):

    # Extract the company data - returns the dataframe
    df = extract_company_data(csv_file_path, summary=False)

    # Cleans the data - removes duplicates, handles missing data and standardise format - returns the dataframe
    df = data_cleaning(df)

    KPIS = transform_data(df)

    return {
        'kpis': KPIS,
        'df': df
    }




