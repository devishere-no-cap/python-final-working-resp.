

# def get_page_html(form_data=None):
#     from pyhtml import get_results_from_query

#     # Form input defaults or actual user input
#     state = form_data.get('state', ['VIC'])[0] if form_data else 'VIC'
#     lat_start = form_data.get('lat_start', ['-38'])[0] if form_data else '-38'
#     lat_end = form_data.get('lat_end', ['-36'])[0] if form_data else '-36'
#     metric = form_data.get('metric', ['MaxTemp'])[0] if form_data else 'MaxTemp'
#     sort_by = form_data.get('sort_by', ['Region'])[0] if form_data else 'Region'

#     error_msg = ""
#     results = []

#     try:
#         # Input sanitization
#         state_escaped = state.replace("'", "''")
#         lat_start_float = float(lat_start)
#         lat_end_float = float(lat_end)

#         valid_metrics = ['MaxTemp', 'MinTemp', 'Rainfall']
#         valid_sort_by = ['Region', 'Number_Weather_Stations', 'Average_Metric']

#         if metric not in valid_metrics:
#             metric = 'MaxTemp'
#         if sort_by not in valid_sort_by:
#             sort_by = 'Region'

#         query = f"""
#             SELECT 
#                 s.Region, 
#                 COUNT(*) AS Number_Weather_Stations, 
#                 ROUND(AVG(w.{metric}), 2) AS Average_Metric
#             FROM WeatherData w
#             JOIN Sites s ON w.Location = s.SiteID
#             WHERE s.State = '{state_escaped}'
#               AND s.Latitude BETWEEN {lat_start_float} AND {lat_end_float}
#             GROUP BY s.Region
#             ORDER BY {sort_by} ASC
#         """
#         print(query)

#         results = get_results_from_query("weatherdata.db", query)

#     except ValueError:
#         error_msg = "Latitude inputs must be valid numbers."
#     except Exception as e:
#         error_msg = f"Error running query: {e}"

#     # Build result rows
#     rows_html = ""
#     if results:
#         for region, num_stations, avg_metric in results:
#             rows_html += f"<tr><td>{region}</td><td>{num_stations}</td><td>{avg_metric}</td></tr>"
#     else:
#         rows_html = "<tr><td colspan='3'>No results found.</td></tr>"

#     # Return page with form and results
#     html = f"""
#     <html>
#     <head>
#         <title>State Query Page</title>
#     </head>
#     <body>
#         <h1>Weather Station Summary</h1>
#         <form method="get" action="/page2a">
#             <label>State:
#                 <select name="state" required>
#                     <option value="VIC" {"selected" if state=="VIC" else ""}>VIC</option>
#                     <option value="NSW" {"selected" if state=="NSW" else ""}>NSW</option>
#                     <option value="QLD" {"selected" if state=="QLD" else ""}>QLD</option>
#                     <option value="WA" {"selected" if state=="WA" else ""}>WA</option>
#                     <option value="SA" {"selected" if state=="SA" else ""}>SA</option>
#                     <option value="TAS" {"selected" if state=="TAS" else ""}>TAS</option>
#                     <option value="NT" {"selected" if state=="NT" else ""}>NT</option>
#                     <option value="ACT" {"selected" if state=="ACT" else ""}>ACT</option>
#                 </select>
#             </label><br><br>

#             <label>Start Latitude:
#                 <input type="text" name="lat_start" value="{lat_start}" required />
#             </label><br><br>

#             <label>End Latitude:
#                 <input type="text" name="lat_end" value="{lat_end}" required />
#             </label><br><br>

#             <label>Metric:
#                 <select name="metric">
#                     <option value="MaxTemp" {"selected" if metric=="MaxTemp" else ""}>MaxTemp</option>
#                     <option value="MinTemp" {"selected" if metric=="MinTemp" else ""}>MinTemp</option>
#                     <option value="Rainfall" {"selected" if metric=="Rainfall" else ""}>Rainfall</option>
#                 </select>
#             </label><br><br>

#             <label>Sort By:
#                 <select name="sort_by">
#                     <option value="Region" {"selected" if sort_by=="Region" else ""}>Region</option>
#                     <option value="Number_Weather_Stations" {"selected" if sort_by=="Number_Weather_Stations" else ""}>Number of Stations</option>
#                     <option value="Average_Metric" {"selected" if sort_by=="Average_Metric" else ""}>Average Metric</option>
#                 </select>
#             </label><br><br>

#             <button type="submit">Submit</button>
#         </form>

#         <p style="color:red;">{error_msg}</p>

#         <h2>Results</h2>
#         <table border="1" cellpadding="5" cellspacing="0">
#             <thead>
#                 <tr>
#                     <th>Region</th>
#                     <th>Number of Stations</th>
#                     <th>Average Metric</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 {rows_html}
#             </tbody>
#         </table>
#     </body>
#     </html>
#     """

#     return html
# import pyhtml
# import re

# def is_valid_number(s):
#     # This regex matches optional leading +/-, digits, optional decimal part
#     # It will NOT match just '-' or empty strings
#     pattern = r'^[-+]?\d*\.?\d+$'
#     return bool(re.match(pattern, s.strip()))

# def get_page_html(form_data=None):
#     print("About to return State View page")

#     state = form_data.get('state', [''])[0] if form_data else ''
#     lat_start = form_data.get('lat_start', [''])[0] if form_data else ''
#     lat_end = form_data.get('lat_end', [''])[0] if form_data else ''
#     metric = form_data.get('metric', ['MaxTemp'])[0] if form_data else 'MaxTemp'
#     sort_by = form_data.get('sort_by', ['Region'])[0] if form_data else 'Region'

#     table1_results, table2_results = [], []
#     error_msg = ""

#     if form_data and lat_start.strip() != '' and lat_end.strip() != '':
#         # Use the is_valid_number function to validate input before float conversion
#         if not is_valid_number(lat_start) or not is_valid_number(lat_end):
#             error_msg = f"Latitude values must be valid numbers. Got: '{lat_start}' and '{lat_end}'"
#         else:
#             try:
#                 lat_start_val = float(lat_start)
#                 lat_end_val = float(lat_end)

#                 if not (-90 <= lat_start_val <= 90 and -90 <= lat_end_val <= 90):
#                     error_msg = "Latitude values must be between -90 and 90."
#                 elif lat_start_val > lat_end_val:
#                     error_msg = "Start latitude must be less than or equal to end latitude."
#                 elif not state:
#                     error_msg = "Please select a state."
#                 else:
#                     state_escaped = state.replace("'", "''")
#                     valid_metrics = ['MaxTemp', 'MinTemp', 'Rainfall']
#                     valid_sort_by = ['Region', 'Number_Weather_Stations', 'Average_Metric']

#                     if metric not in valid_metrics:
#                         metric = 'MaxTemp'
#                     if sort_by not in valid_sort_by:
#                         sort_by = 'Region'

#                     query1 = f"""
#                         SELECT s.Name, s.Region, s.Latitude
#                         FROM Sites s
#                         WHERE s.State = '{state_escaped}'
#                           AND s.Latitude BETWEEN {lat_start_val} AND {lat_end_val}
#                         ORDER BY s.Region;
#                     """

#                     query2 = f"""
#                         SELECT s.Region,
#                                COUNT(*) AS Number_Weather_Stations,
#                                ROUND(AVG(w.{metric}), 2) AS Average_Metric
#                         FROM WeatherData w
#                         JOIN Sites s ON w.Location = s.SiteID
#                         WHERE s.State = '{state_escaped}'
#                           AND s.Latitude BETWEEN {lat_start_val} AND {lat_end_val}
#                         GROUP BY s.Region
#                         ORDER BY {sort_by};
#                     """

#                     table1_results = pyhtml.get_results_from_query("weatherdata.db", query1)
#                     table2_results = pyhtml.get_results_from_query("weatherdata.db", query2)

#             except Exception as e:
#                 error_msg = f"Unexpected error: {e}"
#     else:
#         # On initial load or missing inputs: no error message
#         error_msg = ""

#     table1_html = "".join([
#         f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
#         for r in table1_results
#     ]) or "<tr><td colspan='3'>No results found.</td></tr>"

#     table2_html = "".join([
#         f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
#         for r in table2_results
#     ]) or "<tr><td colspan='3'>No summary data found.</td></tr>"

#     return f"""
#     <html>
#     <head><title>Climate Summary</title></head>
#     <body>
#         <h1>Explore Weather Stations</h1>
#         <form method='GET' action='/page2a'>
#             <label>State: <select name='state' required>
#                 <option value=''>--Select--</option>
#                 {''.join([f"<option value='{s}' {'selected' if s == state else ''}>{s}</option>" for s in ['VIC','NSW','QLD','WA','SA','TAS','NT','ACT']])}
#             </select></label>
#             <label>Start Latitude: <input name='lat_start' type='number' step='0.01' value='{lat_start}' required></label>
#             <label>End Latitude: <input name='lat_end' type='number' step='0.01' value='{lat_end}' required></label>
#             <label>Metric:
#                 <select name='metric'>
#                     <option value='MaxTemp' {'selected' if metric == 'MaxTemp' else ''}>MaxTemp</option>
#                     <option value='MinTemp' {'selected' if metric == 'MinTemp' else ''}>MinTemp</option>
#                     <option value='Rainfall' {'selected' if metric == 'Rainfall' else ''}>Rainfall</option>
#                 </select>
#             </label>
#             <label>Sort By:
#                 <select name='sort_by'>
#                     <option value='Region' {'selected' if sort_by == 'Region' else ''}>Region</option>
#                     <option value='Number_Weather_Stations' {'selected' if sort_by == 'Number_Weather_Stations' else ''}># Stations</option>
#                     <option value='Average_Metric' {'selected' if sort_by == 'Average_Metric' else ''}>Avg Metric</option>
#                 </select>
#             </label>
#             <button type='submit'>Submit</button>
#         </form>
#         <p style='color:red;'>{error_msg}</p>

#         <h2>📍 Weather Stations in Selected State</h2>
#         <table border='1'><tr><th>Site Name</th><th>Region</th><th>Latitude</th></tr>{table1_html}</table>

#         <h2>📊 Regional Climate Summary</h2>
#         <table border='1'><tr><th>Region</th><th>Number Weather Stations</th><th>Average {metric}</th></tr>{table2_html}</table>
#     </body>
#     </html>
#     """

import pyhtml

def get_first(form_data, key, default=''):
    val = form_data.get(key, default)
    if isinstance(val, list):
        return val[0]
    return val

def get_page_html(form_data=None):
    print("About to return State View page")
    print(f"Raw form_data: {form_data}")

    # Get values safely
    state = get_first(form_data, 'state', '')
    metric = get_first(form_data, 'metric', 'MaxTemp')
    sort_by = get_first(form_data, 'sort_by', 'Region')

    print(f"Parsed inputs -> state: {state}, metric: {metric}, sort_by: {sort_by}")

    lat_start_val = -90.0
    lat_end_val = 90.0

    table1_results, table2_results = [], []
    error_msg = ""

    try:
        if not state:
            error_msg = "Please select a state."
        else:
            state_escaped = state.replace("'", "''")

            valid_metrics = ['MaxTemp', 'MinTemp', 'Rainfall']
            valid_sort_by = ['Region', 'Number_Weather_Stations', 'Average_Metric']

            if metric not in valid_metrics:
                metric = 'MaxTemp'
            if sort_by not in valid_sort_by:
                sort_by = 'Region'

            query1 = f"""
                SELECT s.Name, s.Region, s.Latitude
                FROM Sites s
                WHERE s.State = '{state_escaped}'
                  AND s.Latitude BETWEEN {lat_start_val} AND {lat_end_val}
                ORDER BY s.Region;
            """

            query2 = f"""
                SELECT s.Region,
                       COUNT(*) AS Number_Weather_Stations,
                       ROUND(AVG(w.{metric}), 2) AS Average_Metric
                FROM WeatherData w
                JOIN Sites s ON w.Location = s.SiteID
                WHERE s.State = '{state_escaped}'
                  AND s.Latitude BETWEEN {lat_start_val} AND {lat_end_val}
                GROUP BY s.Region
                ORDER BY {sort_by};
            """

            table1_results = pyhtml.get_results_from_query("weatherdata.db", query1)
            table2_results = pyhtml.get_results_from_query("weatherdata.db", query2)

    except Exception as e:
        error_msg = f"Error: {e}"

    table1_html = "".join([
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        for r in table1_results
    ]) or "<tr><td colspan='3'>No results found.</td></tr>"

    table2_html = "".join([
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>"
        for r in table2_results
    ]) or "<tr><td colspan='3'>No summary data found.</td></tr>"

    state_options = ""
    for s in ['VIC','N.S.W.','QLD','W.A.','S.A.','TAS','N.T.','ACT']:
        selected_attr = "selected" if s == state else ""
        state_options += f"<option value='{s}' {selected_attr}>{s}</option>"

    return f"""
<html>
<head>
  <title>Climate Summary</title>
  <link rel="stylesheet" href="/style.css" />
</head>
<body>
  <header class="site-header">
    <h1>Explore Weather Stations</h1> <h1>Australia Climate Watch</h1>
    <nav class="nav-bar">
        <a href="/" class="active">Home</a>
        <a href="/page2a">State View</a>
        <a href="/page3a">Compare Regions</a>
    </nav>
  </header>

  <main class="state-view-main">
    <form method='GET' action='/page2a' class="filter-search">
      <label>State:
        <select name='state' required>
          <option value=''>--Select--</option>
          {state_options}
        </select>
      </label>
      <p>Latitude range is fixed for testing: from {lat_start_val} to {lat_end_val}</p>

      <label>Metric:
        <select name='metric'>
          <option value='MaxTemp' {'selected' if metric == 'MaxTemp' else ''}>MaxTemp</option>
          <option value='MinTemp' {'selected' if metric == 'MinTemp' else ''}>MinTemp</option>
          <option value='Rainfall' {'selected' if metric == 'Rainfall' else ''}>Rainfall</option>
        </select>
      </label>

      <label>Sort By:
        <select name='sort_by'>
          <option value='Region' {'selected' if sort_by == 'Region' else ''}>Region</option>
          <option value='Number_Weather_Stations' {'selected' if sort_by == 'Number_Weather_Stations' else ''}># Stations</option>
          <option value='Average_Metric' {'selected' if sort_by == 'Average_Metric' else ''}>Avg Metric</option>
        </select>
      </label>

      <button type='submit' class="cta-button">Submit</button>
    </form>

    <p style='color:red;'>{error_msg}</p>

    <section class="station-info">
      <h2> Weather Stations in Selected State</h2>
      <table class="data-table" border='1'>
        <thead>
          <tr><th>Site Name</th><th>Region</th><th>Latitude</th></tr>
        </thead>
        <tbody>
          {table1_html}
        </tbody>
      </table>
    </section>

    <section class="station-detail">
      <h2>Regional Climate Summary</h2>
      <table class="data-table" border='1'>
        <thead>
          <tr><th>Region</th><th>Number Weather Stations</th><th>Average {metric}</th></tr>
        </thead>
        <tbody>
          {table2_html}
        </tbody>
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
</html>
"""
