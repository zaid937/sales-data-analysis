import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Load Data ──────────────────────────────────────────
df = pd.read_csv('train.csv', encoding='latin-1')
print("Dataset loaded! Shape:", df.shape)
print(df.head())

# ── Clean Data ─────────────────────────────────────────
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Month'] = df['Order Date'].dt.strftime('%b %Y')
df['Year'] = df['Order Date'].dt.year

# ── 1. TOP 10 PRODUCTS BY SALES ────────────────────────
top_products = df.groupby('Product Name')['Sales'].sum()\
                 .sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
top_products.plot(kind='barh', color='steelblue')
plt.title('Top 10 Products by Sales', fontsize=16)
plt.xlabel('Total Sales ($)')
plt.tight_layout()
plt.savefig('top_products.png')
plt.show()
print("✅ Chart 1 saved!")

# ── 2. MONTHLY SALES TREND ─────────────────────────────
monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Sales']\
            .sum().reset_index()
monthly['Order Date'] = monthly['Order Date'].astype(str)

plt.figure(figsize=(14, 5))
plt.plot(monthly['Order Date'], monthly['Sales'],
         marker='o', color='green', linewidth=2)
plt.title('Monthly Sales Trend', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('monthly_sales.png')
plt.show()
print("✅ Chart 2 saved!")

# ── 3. TOP REGIONS BY REVENUE ──────────────────────────
region_sales = df.groupby('Region')['Sales'].sum()\
                 .sort_values(ascending=False)

plt.figure(figsize=(8, 5))
region_sales.plot(kind='bar', color=['#2196F3','#4CAF50','#FF9800','#E91E63'])
plt.title('Sales by Region', fontsize=16)
plt.xlabel('Region')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('region_sales.png')
plt.show()
print("✅ Chart 3 saved!")

# ── 4. PROFIT BY CATEGORY ──────────────────────────────
category_profit = df.groupby('Category')['Profit'].sum()

plt.figure(figsize=(7, 7))
plt.pie(category_profit, labels=category_profit.index,
        autopct='%1.1f%%', colors=['#42A5F5','#66BB6A','#FFA726'],
        startangle=140)
plt.title('Profit Share by Category', fontsize=16)
plt.tight_layout()
plt.savefig('category_profit.png')
plt.show()
print("✅ Chart 4 saved!")

# ── 5. SUMMARY STATS ───────────────────────────────────
print("\n===== PROJECT SUMMARY =====")
print(f"Total Sales:  ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Total Orders: {df['Order ID'].nunique()}")
print(f"Top Region:   {region_sales.idxmax()}")
print(f"Top Category: {df.groupby('Category')['Sales'].sum().idxmax()}")