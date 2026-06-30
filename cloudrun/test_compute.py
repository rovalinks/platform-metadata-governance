from clients.compute import ComputeClient
from models.resource import Resource

client = ComputeClient()

resource = Resource(
    asset_type="compute.googleapis.com/Instance",
    name="//compute.googleapis.com/projects/platform-metadata-demo/zones/europe-west2-a/instances/small-vm-01",
    project="platform-metadata-demo",
)

labels = {
    "application": "cpe-tagging-validation",
    "environment": "sandbox",
}

client.apply_labels(resource, labels)

print("Labels applied successfully.")