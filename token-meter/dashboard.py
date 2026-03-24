import json
import pandas as pd
import plotly.express as px
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
db = client["token_meter"]
collection = db["data"]

data = list(collection.find({}, {"_id": 0}))

df = pd.DataFrame(data)

fig = px.bar(df, x="model", y="Total Tokens Used", color="sbu")

fig.show()