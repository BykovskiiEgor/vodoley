import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_elasticsearch_search():
    with patch("services.items_service.ItemDocument") as mock_doc:
        mock_search = MagicMock()
        mock_search.to_queryset.return_value = []
        mock_doc.search.return_value = mock_search
        yield
