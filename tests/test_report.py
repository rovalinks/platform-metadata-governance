from services.report import ReportService


def test_report(mocker):

    mock_discovery = mocker.Mock()

    mock_discovery.discover.return_value = [1, 2, 3]

    mock_compliance = mocker.Mock()

    mock_compliance.evaluate.return_value = [
        mocker.Mock(compliant=True),
        mocker.Mock(compliant=False),
        mocker.Mock(compliant=True),
    ]

    mock_enforcement = mocker.Mock()

    mock_enforcement.plan.return_value = [
        {"resource": "vm"}
    ]

    service = ReportService(mock_discovery)

    service.compliance = mock_compliance
    service.enforcement = mock_enforcement

    report = service.report(
        "platform-metadata-demo"
    )

    assert report.total_resources == 3
    assert report.supported_resources == 3
    assert report.compliant_resources == 2
    assert report.non_compliant_resources == 1
    assert report.enforcement_candidates == 1