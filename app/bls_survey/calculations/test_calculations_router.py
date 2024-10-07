from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from app.main import app  
from app.bls_survey.calculations.calculation_dto import CalculationDTO

client = TestClient(app)


# Test for GET /calculations with mocked repository and db
@patch("app.bls_survey.calculations.calculations_router.CalculationsRepository")
def test_get_all_calculations_success(mock_repo):
    # Mock the get_db dependency to avoid needing a real database connection
    mock_db = MagicMock()

    # Mock the repository to return a sample list of calculations
    mock_repo_instance = mock_repo.return_value
    mock_repo_instance.get_all_calculations.return_value = [
        CalculationDTO(pct_changes={"2023": "0.5%"}, net_changes={"2023": "10"}).model_dump(),
    ]

    # Call the GET /calculations route
    response = client.get("/calculations")

    # Assert the response is successful and contains the expected data
    assert response.status_code == 200
    assert response.json() == [
        {"pct_changes": {"2023": "0.5%"}, "net_changes": {"2023": "10"}}
    ]


@patch("app.bls_survey.calculations.calculations_router.CalculationsRepository")
def test_get_all_calculations_no_data(mock_repo):
    # Mock the repository to return an empty list
    mock_repo_instance = mock_repo.return_value
    mock_repo_instance.get_all_calculations.return_value = []

    # Call the GET /calculations route
    response = client.get("/calculations")

    # Assert the response returns 404 when no calculations are found
    assert response.status_code == 404
    assert response.json() == {"detail": "No calculations data found"}


@patch("app.bls_survey.calculations.calculations_router.CalculationsRepository")
def test_get_all_calculations_server_error(mock_repo):
    # Mock the repository to raise an exception
    mock_repo_instance = mock_repo.return_value
    mock_repo_instance.get_all_calculations.side_effect = Exception("Database error")

    # Call the GET /calculations route
    response = client.get("/calculations")

    # Assert the response returns 500 for server errors
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}