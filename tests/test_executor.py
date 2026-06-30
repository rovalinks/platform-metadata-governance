from services.executor import ExecutorService


def test_executor_success(mocker):

    mock_client = mocker.Mock()

    mock_adapter = mocker.Mock()
    mock_adapter.client_for.return_value = mock_client

    service = ExecutorService()

    service.adapters = mock_adapter

    actions = [
        {
            "resource": "//compute.googleapis.com/projects/demo/zones/europe-west2-a/instances/vm-01",
            "asset_type": "compute.googleapis.com/Instance",
            "labels": {
                "application": "demo"
            }
        }
    ]

    results = service.execute(actions)

    mock_client.apply_labels.assert_called_once()

    assert results[0]["status"] == "updated"
