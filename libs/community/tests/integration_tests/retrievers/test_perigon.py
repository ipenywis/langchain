import os

from langchain_community.retrievers.perigon import PerigonRetriever


class TestPerigonRetriever:
    @classmethod
    def setup_class(cls) -> None:
        if not os.getenv("PERIGON_API_KEY"):
            raise ValueError("PERIGON_API_KEY environment variable is not set")

    def test_invoke(self) -> None:
        retriever = PerigonRetriever()
        actual = retriever.invoke("Who won the recent F1 race?")

        assert len(actual) > 0
