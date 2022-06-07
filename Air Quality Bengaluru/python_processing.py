import json
import pandas as pd

data = json.load(open('Air Quality Bengaluru/data/data.json'))
df = pd.DataFrame(data['graphData']['chartSeries']['data'])
print(df)
