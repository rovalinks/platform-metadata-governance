from services.adapter import AdapterService
from clients.storage import StorageClient

def test_compute_adapter():

    adapter = AdapterService()

    client = adapter.client_for(
        "compute.googleapis.com/Instance"
    )

    assert client is not None


def test_bigquery_adapter():

    adapter = AdapterService()

    client = adapter.client_for(
        "bigquery.googleapis.com/Dataset"
    )

    assert client is not None


def test_storage_adapter_supported():

    adapter = AdapterService()

    client = adapter.client_for(
        "storage.googleapis.com/Bucket"
    )

    assert isinstance(
        client,
        StorageClient,
    )