from unittest.mock import AsyncMock, patch

import pytest
import responses

from langchain_community.retrievers.perigon import PerigonRetriever

from ..utilities.test_perigon import (
    TEST_ENDPOINT,
    MOCK_RESULTS_JSON,
    MOCK_DOCUMENTS_OUTPUT,
)


class TestPerigonRetriever:
    @responses.activate
    def test_invoke(self) -> None:
        responses.add(responses.POST, TEST_ENDPOINT, json=MOCK_RESULTS_JSON, status=200)
        query = "Who won the recent F1 race?"
        perigon_retriever = PerigonRetriever(
            perigon_api_key="api_key", config={"size": 2}
        )
        results = perigon_retriever.invoke(query)
        expected_result = MOCK_DOCUMENTS_OUTPUT
        assert results == expected_result

    @responses.activate
    def test_invoke_max_size(self) -> None:
        responses.add(responses.POST, TEST_ENDPOINT, json=MOCK_RESULTS_JSON, status=200)
        query = "Who won the recent F1 race?"
        perigon_retriever = PerigonRetriever(config={"size": 2})
        results = perigon_retriever.invoke(query)
        expected_result = [MOCK_DOCUMENTS_OUTPUT[0], MOCK_DOCUMENTS_OUTPUT[1]]
        assert results == expected_result

    @pytest.mark.asyncio
    async def test_ainvoke(self) -> None:
        instance = PerigonRetriever(config={"size": 2})

        # Mock response object to simulate aiohttp response
        mock_response = AsyncMock()
        mock_response.__aenter__.return_value = (
            mock_response  # Make the context manager return itself
        )
        mock_response.__aexit__.return_value = None  # No value needed for exit
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=MOCK_RESULTS_JSON)

        # Patch the aiohttp.ClientSession object
        with patch("aiohttp.ClientSession.post", return_value=mock_response):
            results = await instance.ainvoke("Who won the recent F1 race?")
            expected_result = MOCK_DOCUMENTS_OUTPUT
            assert results == expected_result
