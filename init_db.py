import sqlite3
import pandas as pd
import numpy as np

def init_database():
    print("Initializing SQLite Database...")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create Customers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        CustomerName TEXT,
        PreferedOrderCat TEXT,
        Tenure REAL,
        SatisfactionScore REAL,
        OrderCount REAL,
        CashbackAmount REAL,
        Complain INTEGER,
        DaySinceLastOrder REAL,
        Feedback TEXT,
        Sentiment TEXT,
        Prediction TEXT,
        Confidence REAL,
        Churn INTEGER,
        -- Storing the rest of the features needed for ML
        PreferredLoginDevice INTEGER,
        CityTier INTEGER,
        WarehouseToHome REAL,
        PreferredPaymentMode INTEGER,
        Gender INTEGER,
        HourSpendOnApp REAL,
        NumberOfDeviceRegistered INTEGER,
        MaritalStatus INTEGER,
        NumberOfAddress INTEGER,
        OrderAmountHikeFromlastYear REAL,
        CouponUsed REAL
    )
    ''')
    
    # Load data from CSV
    print("Loading data from ecommerce_clean.csv...")
    df = pd.read_csv('ecommerce_clean.csv')
    
    # Generate some dummy names (User 50001, User 50002, etc.) to simulate a real database
    df['CustomerName'] = df['CustomerID'].apply(lambda x: f"User {x}")
    df['Feedback'] = None
    df['Sentiment'] = None
    df['Prediction'] = None
    df['Confidence'] = None
    
    # Select columns to match the SQLite table
    cols = [
        'CustomerID', 'CustomerName', 'PreferedOrderCat', 'Tenure', 'SatisfactionScore', 
        'OrderCount', 'CashbackAmount', 'Complain', 'DaySinceLastOrder', 'Feedback', 
        'Sentiment', 'Prediction', 'Confidence', 'Churn', 'PreferredLoginDevice', 'CityTier', 
        'WarehouseToHome', 'PreferredPaymentMode', 'Gender', 'HourSpendOnApp', 
        'NumberOfDeviceRegistered', 'MaritalStatus', 'NumberOfAddress', 
        'OrderAmountHikeFromlastYear', 'CouponUsed'
    ]
    
    # Ensure all columns exist in df
    for col in cols:
        if col not in df.columns:
            print(f"Missing {col}")
            
    df_to_sql = df[cols]
    
    # Insert data into SQLite
    print("Inserting data into database.db...")
    df_to_sql.to_sql('Customers', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    print("Database initialization complete! Saved to database.db")

if __name__ == "__main__":
    init_database()
