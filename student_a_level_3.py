
import pyhtml

def get_page_html(form_data=None):
    print("Returning Level 3 Page (Dynamic Similarity Finder)")

    # Default values
    station_name = "Melbourne Airport"
    metric = "MaxTemp"
    period1_start = "2005-01-01"
    period1_end = "2009-12-31"
    period2_start = "2010-01-01"
    period2_end = "2015-12-31"
    top_n = 3

    if form_data:
        station_name = form_data.get("station", station_name)
        metric = form_data.get("metric", metric)
        period1_start = form_data.get("p1_start", period1_start)
        period1_end = form_data.get("p1_end", period1_end)
        period2_start = form_data.get("p2_start", period2_start)
        period2_end = form_data.get("p2_end", period2_end)
        try:
            top_n = int(form_data.get("top_n", top_n))
        except ValueError:
            top_n = 3

   
import pyhtml  

def get_page_html(form_data=None):
    print("Returning Level 3 Page (Dynamic Similarity Finder)")

    # Default values
    station_name = "Melbourne Airport"
    metric = "MaxTemp"
    period1_start = "2005-01-01"
    period1_end = "2009-12-31"
    period2_start = "2010-01-01"
    period2_end = "2015-12-31"
    top_n = 3

    if form_data:
        station_name = form_data.get("station", station_name)
        metric = form_data.get("metric", metric)
        period1_start = form_data.get("p1_start", period1_start)
        period1_end = form_data.get("p1_end", period1_end)
        period2_start = form_data.get("p2_start", period2_start)
        period2_end = form_data.get("p2_end", period2_end)
        try:
            top_n = int(form_data.get("top_n", top_n))
        except ValueError:
            top_n = 3

    def convert_dmy(col_name):
        return (
            f"date(printf('%04d-%02d-%02d', "
            f"CAST(substr({col_name}, instr({col_name}, '/') + 4, 4) AS INTEGER), "
            f"CAST(substr({col_name}, instr({col_name}, '/') + 1, 2) AS INTEGER), "
            f"CAST(substr({col_name}, 1, instr({col_name}, '/') - 1) AS INTEGER)))"
        )

    try:
        query = f"""
        WITH
        RefStation AS (
            SELECT 
                Location,
                ROUND(AVG(CASE 
                    WHEN {convert_dmy('DMY')} BETWEEN '{period1_start}' AND '{period1_end}' THEN {metric}
                END), 2) AS avg1,
                ROUND(AVG(CASE 
                    WHEN {convert_dmy('DMY')} BETWEEN '{period2_start}' AND '{period2_end}' THEN {metric}
                END), 2) AS avg2
            FROM WeatherData
            WHERE Location = (SELECT SiteID FROM Sites WHERE Name = '{station_name}')
        ),
        AllStations AS (
            SELECT 
                w.Location,
                s.Name AS StationName,
                ROUND(AVG(CASE 
                    WHEN {convert_dmy('w.DMY')} BETWEEN '{period1_start}' AND '{period1_end}' THEN w.{metric}
                END), 2) AS avg1,
                ROUND(AVG(CASE 
                    WHEN {convert_dmy('w.DMY')} BETWEEN '{period2_start}' AND '{period2_end}' THEN w.{metric}
                END), 2) AS avg2
            FROM WeatherData w
            JOIN Sites s ON w.Location = s.SiteID
            GROUP BY w.Location
        ),
        WithChange AS (
            SELECT 
                a.StationName,
                a.avg1 AS Period1_Avg,
                a.avg2 AS Period2_Avg,
                ROUND(((a.avg2 - a.avg1) / a.avg1) * 100, 2) AS PercentChange,
                ROUND(
                    ABS(
                        ((a.avg2 - a.avg1) / a.avg1) - 
                        ((r.avg2 - r.avg1) / r.avg1)
                    ) * 100, 2
                ) AS SimilarityScore
            FROM AllStations a, RefStation r
            WHERE a.avg1 IS NOT NULL AND a.avg2 IS NOT NULL
        )
        SELECT * FROM WithChange
        ORDER BY SimilarityScore ASC
        LIMIT {top_n};
        """

        # Run the query on your DB
        results = pyhtml.get_results_from_query("weatherdata.db", query)

    except Exception as e:
        print("SQL Error:", e)
        results = []

    # Prepare table rows for the results
    table_rows = ""
    for row in results:
        table_rows += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}%</td>
            <td>{row[4]}%</td>
        </tr>"""

    # HTML output with linked CSS (your CSS should be saved as 'style.css' in your web root)
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Climate Watch – Similar Station Finder</title>
    <link rel="stylesheet" href="/style.css" />
</head>
<body>
    <header class="site-header">
        <h1>Australia Climate Watch</h1>
        <nav class="nav-bar">
            <a href="/">Home</a>
            <a href="/page2a">State View</a>
            <a href="/page3a" class="active">Compare Regions</a>
        </nav>
    </header>

    <main class="state-view-main">
        <section class="user-form">
            <h2>Find Similar Weather Stations</h2>
            <form method="GET">
                <label>Reference Station:
                    <input type="text" name="station" value="{station_name}" required>
                </label><br>
                <label>Metric:
                    <select name="metric">
                        <option value="MaxTemp" {"selected" if metric=="MaxTemp" else ""}>MaxTemp</option>
                        <option value="MinTemp" {"selected" if metric=="MinTemp" else ""}>MinTemp</option>
                        <option value="Rainfall" {"selected" if metric=="Rainfall" else ""}>Rainfall</option>
                    </select>
                </label><br><br>
                <fieldset>
                    <legend>Period 1:</legend>
                    Start: <input type="date" name="p1_start" value="{period1_start}" required>
                    End: <input type="date" name="p1_end" value="{period1_end}" required>
                </fieldset>
                <fieldset>
                    <legend>Period 2:</legend>
                    Start: <input type="date" name="p2_start" value="{period2_start}" required>
                    End: <input type="date" name="p2_end" value="{period2_end}" required>
                </fieldset><br>
                <label>Number of Similar Stations:
                    <input type="number" name="top_n" value="{top_n}" min="1" max="10">
                </label><br><br>
                <button type="submit">Compare</button>
            </form>
        </section>

        <section class="results-section">
            <h3>Comparison Results</h3>
            <table class="data-table">
                <tr>
                    <th>Station</th>
                    <th>Avg ({period1_start}–{period1_end})</th>
                    <th>Avg ({period2_start}–{period2_end})</th>
                    <th>% Change</th>
                    <th>Similarity Score</th>
                </tr>
                {table_rows if table_rows else "<tr><td colspan='5'>No results found</td></tr>"}
            </table>
        </section>
    </main>

    <footer class="site-footer">
        <div class="footer-icons">ⓘ ♿ 🎧</div>
        <div class="footer-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Contact</a>
            <a href="#">About</a>
        </div>
    </footer>
</body>
</html>"""

    return page_html
