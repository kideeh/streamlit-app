import pandas as pd
import random
from datetime import datetime, timedelta

# Number of rows
N = 100

# Sample data
titles = [
    "Impact of COVID-19 on Health",
    "New Vaccine Development for COVID-19",
    "COVID-19 Variants and Transmission",
    "Social Distancing Effects",
    "Economic Impacts of COVID-19",
    "Mental Health during Pandemic",
    "Treatment Options for COVID-19",
    "COVID-19 and Education",
    "Public Policy Responses",
    "Long-term Effects of COVID-19"
]

journals = [
    "Journal of Health", "Vaccine Research", "Virology Today",
    "Public Health Reports", "Medical Science", "Global Health Journal"
]

authors = [
    "Smith J; Doe A", "Lee K; Wong M", "Brown C; Green D",
    "Patel R; Singh A", "Garcia M; Lopez P"
]

sources = ["PMC", "ArXiv", "bioRxiv", "medRxiv"]

# Generate random data
data = []
for i in range(N):
    uid = f"id{i:03d}"
    title = random.choice(titles)
    abstract = f"This is a sample abstract about {title.lower()}."
    pub_date = datetime(2020,1,1) + timedelta(days=random.randint(0, 1000))
    journal = random.choice(journals)
    author = random.choice(authors)
    source = random.choice(sources)
    data.append([uid, title, abstract, pub_date.strftime("%Y-%m-%d"), journal, author, source])

# Create DataFrame
df = pd.DataFrame(data, columns=["cord_uid","title","abstract","publish_time","journal","authors","source"])

# Save CSV
df.to_csv("metadata.csv", index=False)
print("Sample metadata.csv created with 100 rows!")
