from services.governance import GovernanceService


def test_expected_labels(mocker):

    mocker.patch(
        "registry.reader.RegistryReader.load_all",
        return_value=[
            {
                "product": "cpe-tagging-validation",
                "team": "cloud-platform-engineering",
                "owner": "camlong@ritchiebros.com",
                "budgetOwner": "pfernandez@ritchiebros.com",
                "organization": "rba",
                "department": "cloud-platform-engineering",
                "costCenter": "PLACEHOLDER",
                "bindings": {
                    "gcp": [
                        {
                            "projectId": "platform-metadata-demo",
                            "environment": "sandbox",
                            "businessCriticality": "low",
                        }
                    ]
                },
            }
        ],
    )

    service = GovernanceService()

    labels = service.expected_labels(
        "platform-metadata-demo"
    )

    assert labels["application"] == "cpe-tagging-validation"
    assert labels["team"] == "cloud-platform-engineering"
    assert labels["environment"] == "sandbox"
    assert labels["businesscriticality"] == "low"
