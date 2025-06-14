
import pyhtml

def get_page_html(form_data=None):
    print("About to return page home page...")

    # --- SQL Queries ---
    try:
        # 1. Avg Max Temp (last 7 days)
        avg_temp = pyhtml.get_results_from_query(
            "weatherdata.db",
            "SELECT ROUND(AVG(MaxTemp),1) FROM DailyWeather_AAT WHERE MaxTemp IS NOT NULL AND DMY >= DATE('now', '-7 days');"
        )[0][0] or "N/A"

        # 2. Year Range Data (modified)
        year_data = pyhtml.get_results_from_query(
            "weatherdata.db",
            """
                SELECT 
                    MIN(CAST(substr(DMY, length(DMY) - 3, 4) AS INTEGER)),
                    MAX(CAST(substr(DMY, length(DMY) - 3, 4) AS INTEGER))
                FROM WeatherData 
                WHERE length(DMY) >= 8 
                AND substr(DMY, length(DMY) - 3, 4) GLOB '[1-2][0-9][0-9][0-9]';
            """
        )

        print("DEBUG: year_data =", year_data)  # Debug print

        try:
            if year_data and year_data[0] and year_data[0][0] is not None and year_data[0][1] is not None:
                year_range = f"{year_data[0][0]}-{year_data[0][1]}"
            else:
                year_range = "No data available"
        except Exception as e:
            print("DEBUG: Error parsing year_data:", e)
            year_range = "Error loading"

        # 3. Active Fire Alerts in NSW
        active_alerts = pyhtml.get_results_from_query(
            "weatherdata.db",
            """
            SELECT Region, COUNT(*) AS number_of_stations 
            FROM Sites 
            GROUP BY Region 
            HAVING Region IS NOT NULL 
            ORDER BY number_of_stations DESC;
            """
        )[0][0] or 0

        # 4. Latest Station Data (for spotlight)
        station_data = pyhtml.get_results_from_query(
            "weatherdata.db",
            """
            SELECT s.Name, w.MaxTemp, w.Humid09 
            FROM WeatherData w
            JOIN Sites s ON w.Location = s.SiteID
            ORDER BY w.DMY DESC LIMIT 1;
            """
        )[0]
        station_name = station_data[0]
        station_temp = station_data[1]
        station_humidity = station_data[2]

    except Exception as e:
        print(f"Error: {e}")
        avg_temp = "?"
        year_range = "?"
        active_alerts = "?"
        station_name = "Unknown"
        station_temp = "?"
        station_humidity = "?"

    # --- HTML with dynamic values ---
    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Australia Climate Watch - Home</title>
    <link rel="stylesheet" href="/style.css" />
</head>
<body>
    <header class="site-header">
        <h1>Australia Climate Watch</h1>
        <nav class="nav-bar">
            <a href="/" class="active">Home</a>
            <a href="/page2a">State View</a>
            <a href="/page3a">Compare Regions</a>
        </nav>
    </header>

    <section class="alert-banner">
        <h2>🔥 Heatwave Warning in Regional NSW</h2>
        <p><a href="#">CLICK FOR INFO</a></p>
    </section>

    <main class="landing-main">
        <h2 class="section-title">QUICK GLANCE</h2>

        <div class="quick-glance-grid">
            <div class="glance-card">
                <h3>🌡️ Temperature Trend</h3>
                <p>Avg. Max Temp this week: <strong>{avg_temp}°C</strong></p>
            </div>

            <div class="glance-card">
                <h3>📅 Data Coverage</h3>
                <p>Available data from: <strong>{year_range}</strong></p>
            </div>

            <div class="glance-card">
                <h3>⚠️ Alert Summary</h3>
                <p>"Heat & Fire Warnings" <strong>{active_alerts} active alerts in NSW</strong></p>
            </div>

            <div class="glance-card">
                <h3>📍 BOM Station Spotlight</h3>
                <p>Nearby Station Update</p>
                <p><strong>{station_name}: {station_temp}°C, {station_humidity}% humidity</strong></p>
            </div>
        </div>

        <section class="cta">
            <a href="/page2a" class="cta-button">Check My State's Weather →</a>
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
</html>
""" 
    print("Rendering page with:")
    print("Avg Temp:", avg_temp)
    print("Year Range:", year_range)
    print("Active Alerts:", active_alerts)
    print("Station Data:", station_name, station_temp, station_humidity)
    print("DEBUG: HTML being returned:\n", page_html)



    return page_html
