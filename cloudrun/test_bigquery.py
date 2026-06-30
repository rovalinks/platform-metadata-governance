from google.cloud import bigquery


PROJECT_ID = "platform-metadata-demo"
DATASET_ID = "cpe_tagging"


client = bigquery.Client(project=PROJECT_ID)

dataset = client.get_dataset(f"{PROJECT_ID}.{DATASET_ID}")

existing = dict(dataset.labels or {})

existing.update(
    {
        "application": "cpe-tagging-validation",
        "environment": "sandbox",
    }
)

dataset.labels = existing

client.update_dataset(
    dataset,
    ["labels"],
)

print("Labels updated successfully.")