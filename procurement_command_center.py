import os
import pandas as pd

REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)

# =====================================================
# Helper
# =====================================================

def write_report(filename, html):

    with open(
        os.path.join(REPORT_DIR, filename),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print("Created:", filename)


# =====================================================
# Supplier Report
# =====================================================

def generate_supplier_report():

    df = pd.read_csv(
        "supplier_scorecard.csv"
    )

    html = """
    <html>
    <head>
        <title>Supplier Scorecard</title>
    </head>
    <body>

    <h1>Strategic Supplier Scorecard</h1>

    <table border="1" cellpadding="5">

    <tr>
        <th>Supplier</th>
        <th>Unit Cost</th>
        <th>Lead Time</th>
        <th>Reliability</th>
        <th>Quality</th>
        <th>On-Time Delivery</th>
    </tr>
    """

    for _, row in df.iterrows():

        html += """
        <tr>
            <td>{}</td>
            <td>${:.2f}</td>
            <td>{}</td>
            <td>{}%</td>
            <td>{}%</td>
            <td>{}%</td>
        </tr>
        """.format(
            row["Supplier"],
            row["UnitCost"],
            row["LeadTimeDays"],
            row["ReliabilityScore"],
            row["QualityScore"],
            row["OnTimeDelivery"]
        )

    html += """
    </table>

    </body>
    </html>
    """

    write_report(
        "supplier_scorecard_report.html",
        html
    )


# =====================================================
# Inventory Report
# =====================================================

def generate_inventory_report():

    df = pd.read_csv(
        "inventory_advanced.csv"
    )

    html = """
    <html>
    <head>
        <title>Inventory Planning</title>
    </head>
    <body>

    <h1>Inventory Planning Dashboard</h1>

    <table border="1" cellpadding="5">

    <tr>
        <th>Material</th>
        <th>On Hand</th>
        <th>Daily Usage</th>
        <th>Lead Time</th>
        <th>Safety Stock</th>
    </tr>
    """

    for _, row in df.iterrows():

        html += """
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        """.format(
            row["Material"],
            row["OnHandQty"],
            row["DailyUsage"],
            row["LeadTimeDays"],
            row["SafetyStock"]
        )

    html += """
    </table>

    </body>
    </html>
    """

    write_report(
        "inventory_planning_report.html",
        html
    )


# =====================================================
# Market Report
# =====================================================

def generate_market_report():

    df = pd.read_csv(
        "market_data.csv"
    )

    html = """
    <html>
    <head>
        <title>Market Intelligence</title>
    </head>
    <body>

    <h1>Market Intelligence Dashboard</h1>

    <table border="1" cellpadding="5">

    <tr>
        <th>Date</th>
        <th>Diesel</th>
        <th>Freight</th>
        <th>Resin</th>
        <th>Copper</th>
    </tr>
    """

    for _, row in df.iterrows():

        html += """
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        """.format(
            row["Date"],
            row["DieselIndex"],
            row["OceanFreight"],
            row["ResinPrice"],
            row["CopperPrice"]
        )

    html += """
    </table>

    </body>
    </html>
    """

    write_report(
        "market_intelligence_report.html",
        html
    )


# =====================================================
# Home Page
# =====================================================

def generate_index():

    html = """
    <html>
    <head>
        <title>Procurement Command Center</title>
    </head>

    <body>

    <h1>Procurement Command Center</h1>

    <h2>Available Reports</h2>

    <ul>

        <li>
            supplier_scorecard_report.html
                Supplier Scorecard
            </a>
        </li>

        <li>
            inventory_planning_report.html
                Inventory Planning
            </a>
        </li>

        <li>
            market_intelligence_report.html
                Market Intelligence
            </a>
        </li>

    </ul>

    </body>
    </html>
    """

    write_report(
        "index.html",
        html
    )


# =====================================================
# MAIN
# =====================================================

print("\nGenerating Reports...\n")

generate_supplier_report()
generate_inventory_report()
generate_market_report()
generate_index()

print("\nOpen reports\\index.html")
print("\nSUCCESS")