from fastapi import FastAPI, File, UploadFile
import pandas as pd
import io
from datetime import datetime

app = FastAPI()

def calculate_gross_margin(df):
    df['Gross Margin'] = (df['Selling price'] - df['Buying price']) * df['Quantity sold']
    df['den'] = df['Buying price']*df['Quantity sold']
    overall_margin = df['Gross Margin'].sum() / df['den'].sum()
    return overall_margin

def most_profitable_vendor(df):
    vendor_profit = df.groupby('Firm bought from')['Gross Margin'].sum()
    most_profitable_vendor = vendor_profit.idxmax()
    return most_profitable_vendor

def least_profitable_customer(df):
    customer_profit = df.groupby('Customer')['Gross Margin'].sum()
    least_profitable_customer = customer_profit.idxmin()
    return least_profitable_customer

def most_profitable_day(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%y/%m/%d')
    df['Day of Week'] = df['Date'].dt.day_name()
    day_profit = df.groupby('Day of Week')['Gross Margin'].sum()
    most_profitable_day = day_profit.idxmax()
    return most_profitable_day

@app.post("/process_csv/")
async def process_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

    # Calculate overall gross margin
    overall_margin = calculate_gross_margin(df)

    # Find the most profitable vendor
    most_profitable_vendor_name = most_profitable_vendor(df)

    # Find the least profitable customer
    least_profitable_customer_name = least_profitable_customer(df)

    # Find the most profitable day
    most_profitable_day_name = most_profitable_day(df)

    result = {
        "overall_gross_margin": overall_margin,
        "most_profitable_vendor": most_profitable_vendor_name,
        "least_profitable_customer": least_profitable_customer_name,
        "most_profitable_day": most_profitable_day_name
    }

    return result
