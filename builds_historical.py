import csv
import os

OUTPUT_FOLDER = r"C:\Users\james\OneDrive\Roller Coasters\Roller Coaster Lineup Ranking\Site Test\output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HISTORICAL_FILE = r"C:\Users\james\OneDrive\Roller Coasters\Roller Coaster Lineup Ranking\Site Test\park history.csv"

# Read CSV and preserve the original row order from A2 downward.
# The checkbox list and the chart datasets must stay in the same sequence.
parks = []
months = []
ordered_rows = []

with open(HISTORICAL_FILE, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    raw_months = reader.fieldnames[1:] if reader.fieldnames else []
    months = [m.strip() for m in raw_months]

    for row in reader:
        park_name = row["PARK"].strip()
        scores = [float(row[m].strip()) if row.get(m, "").strip() != "" else 0 for m in months]
        ordered_rows.append((park_name, scores))

parks = [park_name for park_name, _ in ordered_rows]
data_by_park = {park_name: scores for park_name, scores in ordered_rows}

# Generate HTML page
historical_html = f"""<!DOCTYPE html>
<html>
<head>
<title>Historical Park Scores</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{
    background-color: #121212;
    color: #fff;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    margin: 40px;
}}
h1 {{ color: #1E90FF; text-align: center; }}
#controls {{
    text-align: center;
    margin-top: 20px;
}}
label {{
    display: inline-block;
    width: 180px;
}}
button {{
    margin: 10px;
    padding: 8px 15px;
    background-color: #1E90FF;
    border: none;
    color: #fff;
    border-radius: 5px;
    cursor: pointer;
}}
button:hover {{ background-color: #0F75D8; }}
a.back-link {{
    display: block;
    text-align: center;
    margin-top: 30px;
    padding: 10px 20px;
    border: 1px solid #1E90FF;
    border-radius: 5px;
    width: 150px;
    margin-left:auto;
    margin-right:auto;
    text-decoration:none;
    color:#1E90FF;
}}
a.back-link:hover {{ background-color:#1E90FF; color:#fff; }}
</style>
</head>
<body>

<h1>Historical Park Scores</h1>

<a href="/index.html" class="back-link">Back to Rankings</a>

<canvas id="historicalChart" width="1000" height="500"></canvas>

<div id="controls">
<button onclick="clearSelection()">Clear Selection</button>
<button onclick="selectTop20()">Select Top 20</button>
<br><br>
<form id="parkForm">
"""

# Add checkboxes in the same A2-down order read from the CSV.
for park in parks:
    historical_html += f'<input type="checkbox" name="park" value="{park}"> {park}<br>\n'

historical_html += """
</form>
</div>

<script>
const months = """ + str(months) + """;
const parkData = [
"""

# Add park data JS array
colors = [
'#1E90FF','#FF4500','#FFA500','#32CD32','#8A2BE2','#FF69B4','#00CED1','#FFD700','#ADFF2F','#FF7F50',
'#7FFF00','#DC143C','#00BFFF','#FF1493','#20B2AA','#FF6347','#BA55D3','#40E0D0','#FF8C00','#7B68EE'
]

for i, park in enumerate(parks):
    scores = data_by_park[park]
    color = colors[i % len(colors)]
    historical_html += f"""{{ label: "{park}", data: {scores}, borderColor: "{color}", hidden:true }},\n"""

historical_html += """
];

// Create Chart
const ctx = document.getElementById('historicalChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: months,
        datasets: parkData
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'right',
                onClick: null,
                labels: {
                    color: '#FFFFFF',
                    generateLabels: function(chart) {
                        return chart.data.datasets
                            .filter(d => !d.hidden)   // only datasets that are visible
                            .map(d => ({
                                text: d.label,
                                fillStyle: d.borderColor,
                                hidden: d.hidden,
                                datasetIndex: chart.data.datasets.indexOf(d),
                                fontColor: '#FFFFFF'
                            }));
                    }
                }
            }
        },
        scales: {
            y: { title: { display: true, text: 'Score' } },
            x: { title: { display: true, text: 'Month' }, reverse: true }
        }
    }
});

// Handle checkbox selection
document.getElementById('parkForm').addEventListener('change', function() {
    const checked = Array.from(document.querySelectorAll('input[name="park"]:checked')).map(i=>i.value);
    parkData.forEach(d => d.hidden = !checked.includes(d.label));
    chart.update();
});

function clearSelection(){
    document.querySelectorAll('input[name="park"]').forEach(cb=>cb.checked=false);
    parkData.forEach(d=>d.hidden=true);
    chart.update();
}

function selectTop20(){
    clearSelection();
    document.querySelectorAll('input[name="park"]').forEach((cb,i)=>{
        if(i<20){ cb.checked=true; parkData[i].hidden=false; }
    });
    chart.update();
}
</script>
</body>
</html>
"""

# Write to file
with open(os.path.join(OUTPUT_FOLDER, "historical.html"), "w", encoding="utf-8") as f:
    f.write(historical_html)

print("Historical data page generated!")