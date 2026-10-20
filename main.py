import pandas as pd
import numpy as np
import webbrowser
import os

np.random.seed(42)

manufacturers = [
    "Tesla", "Tata Motors", "BYD", "Hyundai",
    "MG Motor", "Mahindra", "Kia", "BMW"
]

categories = ["SUV", "Sedan", "Hatchback", "Two-Wheeler"]
batteries = ["LFP", "NMC", "NCA", "Solid-State"]

data = {
    "Manufacturer": np.random.choice(manufacturers, 100),
    "Category": np.random.choice(categories, 100),
    "Battery_Technology": np.random.choice(batteries, 100),
    "Battery_Capacity_kWh": np.random.randint(20, 110, 100),
    "Driving_Range_km": np.random.randint(150, 650, 100),
    "Annual_Sales": np.random.randint(500, 25000, 100),
    "Price_INR_Lakh": np.random.randint(5, 100, 100),
    "Customer_Rating": np.round(np.random.uniform(3.0, 5.0, 100), 1),
    "Manufacturing_Country": np.random.choice(
        ["India", "USA", "China", "Germany", "South Korea"], 100
    )
}

df = pd.DataFrame(data)

df.to_csv("ev_market_data.csv", index=False)

total_sales = df["Annual_Sales"].sum()
average_range = df["Driving_Range_km"].mean()
average_rating = df["Customer_Rating"].mean()
average_price = df["Price_INR_Lakh"].mean()

manufacturer_sales = (
    df.groupby("Manufacturer")["Annual_Sales"]
    .sum()
    .sort_values(ascending=False)
)

category_sales = (
    df.groupby("Category")["Annual_Sales"]
    .sum()
    .sort_values(ascending=False)
)

battery_count = df["Battery_Technology"].value_counts()
country_count = df["Manufacturing_Country"].value_counts()

print("=" * 50)
print(" ELECTRIC VEHICLE MARKET PERFORMANCE & INSIGHTS")
print("=" * 50)

print("\nMARKET OVERVIEW")
print("-" * 30)
print(f"Total recorded sales: {total_sales:,}")
print(f"Average driving range: {average_range:.2f} km")
print(f"Average customer rating: {average_rating:.2f}/5")
print(f"Average vehicle price: Rs. {average_price:.2f} lakh")

print("\nSALES BY MANUFACTURER")
print(manufacturer_sales.to_string())

print("\nSALES BY VEHICLE CATEGORY")
print(category_sales.to_string())

print("\nBATTERY TECHNOLOGY DISTRIBUTION")
print(battery_count.to_string())

print("\nMANUFACTURING COUNTRY DISTRIBUTION")
print(country_count.to_string())

print("\nTOP 5 VEHICLES BY DRIVING RANGE")
print(
    df.nlargest(5, "Driving_Range_km")[
        ["Manufacturer", "Category", "Driving_Range_km"]
    ].to_string(index=False)
)

def make_bars(series, color="#16a085"):
    maximum = max(series.max(), 1)
    html = ""

    for name, value in series.items():
        width = value / maximum * 100
        html += f"""
        <div class="bar-row">
            <div class="bar-label">{name}</div>
            <div class="bar-bg">
                <div class="bar" style="width:{width:.1f}%;
                background:{color}"></div>
            </div>
            <div class="bar-value">{value:,.0f}</div>
        </div>
        """
    return html


manufacturer_bars = make_bars(manufacturer_sales)
category_bars = make_bars(category_sales, "#3498db")
battery_bars = make_bars(battery_count, "#8e44ad")
country_bars = make_bars(country_count, "#e67e22")

top_vehicles = df.nlargest(10, "Driving_Range_km")

table_rows = ""
for _, row in top_vehicles.iterrows():
    table_rows += f"""
    <tr>
        <td>{row['Manufacturer']}</td>
        <td>{row['Category']}</td>
        <td>{row['Driving_Range_km']} km</td>
        <td>{row['Battery_Capacity_kWh']} kWh</td>
        <td>{row['Customer_Rating']}/5</td>
    </tr>
    """

dashboard = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>EV Market Insights Dashboard</title>
<style>
body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f3f6f8;
    color: #263238;
}}
header {{
    background: #173f35;
    color: white;
    padding: 28px;
    text-align: center;
}}
header p {{ color: #d1e8df; }}
.container {{ padding: 22px; max-width: 1200px; margin: auto; }}
.cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}}
.card, .panel {{
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px #00000010;
    margin-bottom: 18px;
}}
.card h3 {{ color: #61736d; font-size: 14px; }}
.metric {{ font-size: 26px; font-weight: bold; color: #167653; }}
.charts {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 18px;
}}
.bar-row {{
    display: grid;
    grid-template-columns: 105px 1fr 65px;
    gap: 8px;
    align-items: center;
    margin: 14px 0;
    font-size: 12px;
}}
.bar-bg {{ background: #e8eeee; height: 15px; border-radius: 4px; }}
.bar {{ height: 15px; border-radius: 4px; }}
.bar-value {{ text-align: right; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th, td {{ padding: 12px 8px; border-bottom: 1px solid #ddd; text-align: left; }}
th {{ background: #eaf2ef; }}
.note {{ color: #687780; font-size: 12px; }}
</style>
</head>
<body>

<header>
<h1>Electric Vehicle Market Performance & Insights</h1>
<p>Market analysis | Manufacturer performance | Battery technologies</p>
</header>

<div class="container">

<div class="cards">
    <div class="card">
        <h3>Total Recorded Sales</h3>
        <div class="metric">{total_sales:,}</div>
    </div>
    <div class="card">
        <h3>Average Driving Range</h3>
        <div class="metric">{average_range:.0f} km</div>
    </div>
    <div class="card">
        <h3>Average Customer Rating</h3>
        <div class="metric">{average_rating:.2f}/5</div>
    </div>
    <div class="card">
        <h3>Average Vehicle Price</h3>
        <div class="metric">Rs. {average_price:.2f} lakh</div>
    </div>
</div>

<div class="charts">
    <div class="panel">
        <h2>Sales by Manufacturer</h2>
        {manufacturer_bars}
    </div>
    <div class="panel">
        <h2>Sales by Vehicle Category</h2>
        {category_bars}
    </div>
    <div class="panel">
        <h2>Battery Technology Distribution</h2>
        {battery_bars}
    </div>
    <div class="panel">
        <h2>Manufacturing Countries</h2>
        {country_bars}
    </div>
</div>

<div class="panel">
<h2>Top 10 Vehicles by Driving Range</h2>
<table>
<thead>
<tr>
<th>Manufacturer</th>
<th>Category</th>
<th>Driving Range</th>
<th>Battery Capacity</th>
<th>Customer Rating</th>
</tr>
</thead>
<tbody>
{table_rows}
</tbody>
</table>
</div>

<div class="panel">
<h2>Key Insights</h2>
<ul>
<li>The manufacturer with the highest recorded sales is
<b>{manufacturer_sales.index[0]}</b>.</li>
<li>The leading vehicle category by recorded sales is
<b>{category_sales.index[0]}</b>.</li>
<li>The most frequently represented battery technology is
<b>{battery_count.index[0]}</b>.</li>
<li>The most represented manufacturing country is
<b>{country_count.index[0]}</b>.</li>
</ul>
<p class="note">
Note: This project uses randomly generated sample data for demonstration.
Sales figures are not verified real-world market statistics.
</p>
</div>

</div>
</body>
</html>
"""

with open("ev_dashboard.html", "w", encoding="utf-8") as file:
    file.write(dashboard)

print("\nDataset saved as ev_market_data.csv")
print("Dashboard saved as ev_dashboard.html")

webbrowser.open("file://" + os.path.abspath("ev_dashboard.html"))

print("\nProject completed successfully!")
