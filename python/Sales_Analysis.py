import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

#---- Analyze Data -----------
df = pd.read_excel(r"F:\Data analytics\Portfolio\Sales_Analysis\Dataset\Sales_Analysis_Dataset.xlsx", sheet_name='Sales_Table')
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


# 1. تحميل البيانات (افترضنا أن الملف هو excel أو csv)
# df = pd.read_excel('sales_data.xlsx')
# للتجربة، سنقوم بإنشاء بيانات وهمية تشبه بياناتك


# --- الحسابات المطلوبة ---

# 1. Total Records (إجمالي عدد الأسطر - الـ 1200 سطر)
total_records = df.shape[0]

# 2. Total Sales (إجمالي المبيعات)
total_sales = df['Sales'].sum()

# 3. Monthly Sales (المبيعات الشهرية)
monthly_sales = df.resample('ME', on='Order Date')['Sales'].sum()

# 4. MoM % (نسبة النمو الشهري)
mom_growth = monthly_sales.pct_change() * 100

# 5. YoY % (نسبة النمو السنوي)
# نحتاج لتجميع البيانات سنوياً أولاً
yearly_sales = df.resample('YE', on='Order Date')['Sales'].sum()
yoy_growth = yearly_sales.pct_change() * 100

# --- طباعة النتائج ---
print(f"Total Records: {total_records}")
print(f"Total Sales: {total_sales}")
print("\nMonthly Sales:\n", monthly_sales)
print("\nMonth-over-Month Growth (%):\n", mom_growth)
print("\nYear-over-Year Growth (%):\n", yoy_growth)


#---- Decision Making -----------
decisions = {
    "High Discounts": "Limit discount to max 20%",
    "Loss Products": "Stop or reprice loss-making products",
    "Top Categories": "Increase inventory for high profit categories",
    "Seasonality": "Increase marketing during high sales months"
}
for k, v in decisions.items():
    print(k, "->", v)


pdf = FPDF()
pdf.add_page()

import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

# 1. إعداد التقرير وحفظ الرسوم البيانية كصور مؤقتة
def save_plots():
    # رسم تحليل الأصناف
    plt.figure(figsize=(10, 5))
    category_analysis['Sales'].plot(kind='bar', color='skyblue')
    plt.title("Total Sales by Category")
    plt.tight_layout()
    plt.savefig("cat_sales.png")
    plt.close()

    # رسم تحليل القطاعات
    plt.figure(figsize=(10, 5))
    segment_analysis['Profit'].plot(kind='bar', color='salmon')
    plt.title("Total Profit by Segment")
    plt.tight_layout()
    plt.savefig("seg_profit.png")
    plt.close()

# 2. إنشاء كلاس الـ PDF وتنسيقه
class AnalysisReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Sales & Business Analysis Report', 0, 1, 'C')
        self.ln(5)

    def add_section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', fill=True)
        self.ln(4)

    def add_text_line(self, label, value):
        self.set_font('Arial', 'B', 10)
        self.write(10, f"{label}: ")
        self.set_font('Arial', '', 10)
        self.write(10, f"{value}\n")

# 3. تنفيذ استخراج البيانات وتوليد الملف
save_plots()
pdf = AnalysisReport()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# --- القسم الأول: المؤشرات الرئيسية (KPIs) ---
pdf.add_section_title("1. Executive Summary (KPIs)")
pdf.add_text_line("Total Records (CountRows)", f"{total_records}")
pdf.add_text_line("Total Sales", f"${total_sales:,.2f}")
pdf.add_text_line("Total Profit", f"${total_Profit:,.2f}")
pdf.add_text_line("Profit Margin", f"{profit_margin:.2%}")
pdf.add_text_line("Average Discount", f"{avg_discount:.2%}")
pdf.ln(10)

# --- القسم الثاني: الرسوم البيانية ---
pdf.add_section_title("2. Visual Analysis")
pdf.image("cat_sales.png", x=10, w=180)
pdf.ln(5)
pdf.image("seg_profit.png", x=10, w=180)

# --- صفحة جديدة للنمو والقرارات ---
pdf.add_page()
pdf.add_section_title("3. Growth Metrics (MoM & YoY)")
# تحويل نتائج النمو لنص
mom_text = f"Latest Month-over-Month Growth: {mom_growth.iloc[-1]:.2f}%"
yoy_text = f"Year-over-Year Growth: {yoy_growth.iloc[-1]:.2f}%" if not pd.isna(yoy_growth.iloc[-1]) else "YoY: N/A"
pdf.add_text_line("MoM %", mom_text)
pdf.add_text_line("YoY %", yoy_text)
pdf.ln(10)

# --- القسم الرابع: القرارات الاستراتيجية ---
pdf.add_section_title("4. Strategic Decisions & Insights")
for k, v in decisions.items():
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, f"* {k}:", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, v)
    pdf.ln(2)

# حفظ الملف
pdf.output("Business_Analysis_Report.pdf")

# تنظيف الصور المؤقتة
os.remove("cat_sales.png")
os.remove("seg_profit.png")

print(" Done! Your professional PDF report is ready: Business_Analysis_Report.pdf")
