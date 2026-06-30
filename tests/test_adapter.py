from services.adapter import AdapterService


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


def test_storage_adapter_not_supported():

    adapter = AdapterService()

    client = adapter.client_for(
        "storage.googleapis.com/Bucket"
    )

    assert client is None
