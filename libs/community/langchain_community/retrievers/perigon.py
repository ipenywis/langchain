from typing import Any, List
from langchain_core.callbacks import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_community.utilities.perigon import (
    PerigonVectorAPIWrapper,
    PerigonVectorConfig,
    DEFAULT_PERIGON_CONFIG,
)
from typing import Any, List, Optional


class PerigonRetriever(BaseRetriever, PerigonVectorAPIWrapper):
    """Perigon Vector API retriever."""

    def _get_relevant_documents(
        self,
        query: str,
        run_manager: CallbackManagerForRetrieverRun,
        perigon_config: PerigonVectorConfig = None,
    ) -> List[Document]:
        selected_config = perigon_config if perigon_config is not None else self.config
        return self.results(query, config=selected_config)

    async def _aget_relevant_documents(
        self,
        query: str,
        run_manager: AsyncCallbackManagerForRetrieverRun,
        config: Optional[PerigonVectorConfig] = None,
    ) -> List[Document]:
        selected_config = config if config is not None else self.config

        results = await self.results_async(query, config=selected_config)
        return results
