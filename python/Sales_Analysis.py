import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

#---- Analyze Data -----------
df = pd.read_excel(r"F:\Data analytics\Business Case\Dataset\Sales_Analysis_Dataset.xlsx", sheet_name='Sales_Table')
print(df.head())
print(df.info())

#---- Cleaning Data -----------
df['Order Date'] = pd.to_datetime(df['Order Date'])
print(df.isnull().sum())
df = df[df['Quantity'] > 0]
df = df[df['Sales'] >= 0]

#---- Create KPIs -----------
Total_Sales = df['Sales'].sum()
total_Profit = df['Profit'].sum()
total_Orders = df['Order ID'].unique()
avg_discount = df['Discount'].mean()
profit_margin = (total_Profit / Total_Sales)

print("Total Sales :" , Total_Sales)
print("Total Profit :" , total_Profit)
print("Total Orders :" , total_Orders)
print("Average Discount : " , avg_discount)
print("Profit Margin :" , profit_margin)

#---- Category Analysis -----------
category_analysis = (
    df.groupby('Category')[['Sales' , 'Profit']]
    .sum()
    .sort_values(by='Sales' , ascending= False)
)
print(category_analysis)

category_analysis['Sales'].plot(kind='bar')
plt.title("Total Sales by Category")
plt.show()

category_analysis['Profit'].plot(kind = 'bar')
plt.title("Total Profit by Category")
plt.show()

#---- Discount vs. Profit Analysis -----------
discount_profit = df.groupby('Discount')['Profit'].mean()
print(discount_profit)

discount_profit.plot(kind = 'line' , marker = 'o')
plt.title("Average Profit by Discount Level")
plt.xlabel("Discount")
plt.ylabel("Average Profit")
plt.show()

#---- Time Series Analysis -----------
df['Month'] = df['Order Date'].dt.to_period('M')

monthly_sales = df.groupby('Month')['Sales'].sum()
monthly_profit = df.groupby('Month')['Profit'].sum()

monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.show()

monthly_sales.plot()
plt.title("Monthly Profit Trend")
plt.show()

#---- Top & Loss Products -----------
top_products = (
    df.groupby('Product')['Profit']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_products)

loss_products = (
    df.groupby('Product')['Profit']
    .sum()
    .sort_values()
    .head(10)
)
print(loss_products)

#---- Customer Segment Analysis ---------
segment_analysis = (
    df.groupby('Customer Segment')[['Sales', 'Profit']]
    .sum()
)

print(segment_analysis)

segment_analysis.plot(kind='bar')
plt.title("Sales & Profit by Customer Segment")
plt.show()


#---- Decision Making -----------
decisions = {
    "High Discounts": "Limit discount to max 20%",
    "Loss Products": "Stop or reprice loss-making products",
    "Top Categories": "Increase inventory for high profit categories",
    "Seasonality": "Increase marketing during high sales months"
}
for k, v in decisions.items():
    print(k, "->", v)
