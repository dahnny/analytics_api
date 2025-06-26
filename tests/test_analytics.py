import pytest

def test_get_financial_summary(authorized_client, test_sales, test_expenses):
    response = authorized_client.get("api/v1/analytics/summary/")
    assert response.status_code == 200
    summary = response.json()
    assert isinstance(summary["datasets"], list)
    assert all(isinstance(item, dict) for item in summary["datasets"])
    assert all("label" in item and "data" in item for item in summary["datasets"])


def test_get_monthly_summary(authorized_client, test_sales, test_expenses):
    # Test for a specific year
    year = 2023
    response = authorized_client.get(f"api/v1/analytics/monthly-summary?year={year}")
    assert response.status_code == 200
    summary = response.json()
    assert isinstance(summary["labels"], list)
    assert len(summary["labels"]) == 12
    assert all(isinstance(item, str) for item in summary["labels"])
    assert "datasets" in summary
    assert isinstance(summary["datasets"], list)
    assert all(isinstance(item, dict) for item in summary["datasets"])
    assert all("label" in item and "data" in item for item in summary["datasets"])
    
def test_unauthorized_financial_summary(client):
    response = client.get("api/v1/analytics/summary/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

@pytest.mark.parametrize(
    "start_date, end_date",
    [
        ("2023-01-01", "2023-01-31"),
        ("2023-02-01", "2023-02-28"),
        ("2023-03-01", "2023-03-31"),
    ]
)
def test_get_summary_with_date_range(authorized_client, start_date, end_date, test_sales, test_expenses):
    response = authorized_client.get(
        f"api/v1/analytics/summary?start_date={start_date}&end_date={end_date}"
    )
    assert response.status_code == 200
    summary = response.json()
    assert isinstance(summary["datasets"], list)
    assert all(isinstance(item, dict) for item in summary["datasets"])
    assert all("label" in item and "data" in item for item in summary["datasets"])
    
def test_get_summary_with_invalid_date_range(authorized_client):
    response = authorized_client.get(
        "api/v1/analytics/summary?start_date=invalid&end_date=invalid"
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format. Use ISO format (YYYY-MM-DD)."}
    
def test_get_weekly_summary(authorized_client, test_sales, test_expenses):
    response = authorized_client.get("api/v1/analytics/weekly-summary?start_date=2023-10-01&end_date=2023-10-07")
    assert response.status_code == 200
    summary = response.json()
    assert isinstance(summary["labels"], list)
    assert len(summary["labels"]) > 0
    assert "datasets" in summary
    assert isinstance(summary["datasets"], list)
    assert all(isinstance(item, dict) for item in summary["datasets"])
    assert all("label" in item and "data" in item for item in summary["datasets"])
    
def test_get_weekly_summary_without_dates(authorized_client):
    response = authorized_client.get("api/v1/analytics/weekly-summary")
    assert response.status_code == 400
    assert response.json() == {"detail": "Start date is required."}
    
def test_get_expense_breakdown(authorized_client, test_expenses):
    response = authorized_client.get("api/v1/analytics/expense-breakdown?start_date=2023-10-01&end_date=2023-10-31")
    assert response.status_code == 200
    breakdown = response.json()['datasets']
    assert isinstance(breakdown, list)
    assert all(isinstance(item, dict) for item in breakdown)
    assert all("label" in item and "data" in item for item in breakdown)
    
def test_get_expense_breakdown_without_dates(authorized_client):
    response = authorized_client.get("api/v1/analytics/expense-breakdown")
    assert response.status_code == 200
    breakdown = response.json()['datasets']
    assert isinstance(breakdown, list)
    assert all(isinstance(item, dict) for item in breakdown)
    assert all("label" in item and "data" in item for item in breakdown)
    
def test_get_expense_breakdown_with_invalid_dates(authorized_client):
    response = authorized_client.get("api/v1/analytics/expense-breakdown?start_date=invalid&end_date=invalid")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format. Use ISO format (YYYY-MM-DD)."}
    