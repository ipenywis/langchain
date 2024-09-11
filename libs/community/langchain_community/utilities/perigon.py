"""Util that calls Perigon Vector API.

In order to set this up, follow instructions at:

"""

from typing import Any, Dict, List, Optional, TypedDict, Union

import aiohttp
import requests
from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain_core.utils import get_from_dict_or_env

PERIGON_VECTOR_API_URL = "https://api.goperigon.com/v1/vector/news/all"


class PerigonCoordinates(TypedDict, total=False):
    """Coordinates for the Perigon Vector API."""

    lat: float
    lon: float
    radius: float


class PerigonVectorFilter(TypedDict, total=False):
    """Filter for the Perigon Vector API.

    See https://docs.goperigon.com/api/vector/search/
    """

    articleId: Optional[Union[str, List[str]]]
    clusterId: Optional[Union[str, List[str]]]
    source: Optional[Union[str, List[str]]]
    sourceGroup: Optional[Union[str, List[str]]]
    language: Optional[Union[str, List[str]]]
    label: Optional[Union[str, List[str]]]
    category: Optional[Union[str, List[str]]]
    topic: Optional[Union[str, List[str]]]
    country: Optional[Union[str, List[str]]]
    locationsCountry: Optional[Union[str, List[str]]]
    state: Optional[Union[str, List[str]]]
    county: Optional[Union[str, List[str]]]
    city: Optional[Union[str, List[str]]]
    coordinates: Optional[PerigonCoordinates]
    sourceCountry: Optional[Union[str, List[str]]]
    sourceState: Optional[Union[str, List[str]]]
    sourceCounty: Optional[Union[str, List[str]]]
    sourceCity: Optional[Union[str, List[str]]]
    sourceCoordinates: Optional[PerigonCoordinates]
    companyId: Optional[Union[str, List[str]]]
    companyDomain: Optional[Union[str, List[str]]]
    companySymbol: Optional[Union[str, List[str]]]
    companyName: Optional[Union[str, List[str]]]
    personWikidataId: Optional[Union[str, List[str]]]
    personName: Optional[Union[str, List[str]]]
    AND: Optional[List["PerigonVectorFilter"]]
    OR: Optional[List["PerigonVectorFilter"]]
    NOT: Optional[Union["PerigonVectorFilter", List["PerigonVectorFilter"]]]


class PerigonVectorConfig(TypedDict, total=False):
    """Options for the Perigon Vector API."""

    pubDateFrom: Optional[str]
    pubDateTo: Optional[str]
    size: Optional[int]
    showReprints: Optional[bool]
    filter: Optional[PerigonVectorFilter]


DEFAULT_PERIGON_CONFIG = PerigonVectorConfig(
    size=10,
    showReprints=True,
    filter=None,
)


class PerigonVectorAPIWrapper(BaseModel):
    """Wrapper for Perigon Vector API."""

    perigon_api_key: Optional[str] = None
    """API key for accessing the Perigon Vector API.

    This attribute stores the API key required for authenticating requests to the Perigon Vector API.
    It is an optional string that can be set directly or through environment variables.

    If not provided during initialization, the wrapper will attempt to retrieve it from
    the PERIGON_API_KEY environment variable.
    
    Please note you must either set this or set the PERIGON_API_KEY environment variable. The environment variable is recommended for production use.

    Attributes:
        perigon_api_key (Optional[str]): The API key for Perigon Vector API authentication.
    """
    config: Optional[Dict] = DEFAULT_PERIGON_CONFIG
    """Configuration options for the Perigon Vector API.

    This attribute stores the configuration settings for the Perigon Vector API.
    It is an optional dictionary that defaults to DEFAULT_PERIGON_CONFIG.

    The configuration can include the following options:
    - pubDateFrom (Optional[str], default=None): Start date for publication date range filter.
    - pubDateTo (Optional[str], default=None): End date for publication date range filter.
    - size (Optional[int], default=10): Number of results to return.
    - showReprints (Optional[bool], default=True): Whether to include reprinted articles.
    - filter (Optional[PerigonVectorFilter], default=None): Additional filtering options.

    If not provided, it uses the default configuration defined in DEFAULT_PERIGON_CONFIG.
    Can be overridden by passing a config to the retriever invoke method.
    """

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        perigon_api_key = get_from_dict_or_env(
            values, "perigon_api_key", "PERIGON_API_KEY"
        )
        values["perigon_api_key"] = perigon_api_key
        return values

    def _generate_params(
        self, query: str, **kwargs: PerigonVectorConfig
    ) -> PerigonVectorConfig:
        """Generate parameters for Perigon API."""
        body = {
            "prompt": query,
            **kwargs,
        }
        if "filter" in kwargs and kwargs["filter"] is not None:
            body["filter"] = PerigonVectorFilter(**kwargs["filter"])
        return {k: v for k, v in body.items() if v is not None}

    def _parse_results(self, raw_results: Dict) -> List[Document]:
        """Parse results from Perigon API."""
        documents = []
        for article in raw_results.get("results", []):
            data = article.get("data", {})
            documents.append(
                Document(
                    page_content=data.get("summary", ""),
                    metadata={
                        "title": data.get("title"),
                        "url": data.get("url"),
                        "source": data.get("source"),
                        "published_date": data.get("publishedDate"),
                        "add_date": data.get("addDate"),
                        "language": data.get("language"),
                        "imageUrl": data.get("imageUrl"),
                        "entities": ", ".join(
                            [entity["data"] for entity in data.get("entities", [])]
                        ),
                        "categories": ", ".join(
                            [
                                category["name"]
                                for category in data.get("categories", [])
                            ]
                        ),
                        "topics": ", ".join(
                            [topic["name"] for topic in data.get("topics", [])]
                        ),
                        "companies": ", ".join(
                            [company["name"] for company in data.get("companies", [])]
                        ),
                        "people": ", ".join(
                            [person["name"] for person in data.get("people", [])]
                        ),
                    },
                )
            )
        return documents

    def results(
        self, query: str, config: Optional[PerigonVectorConfig] = None
    ) -> List[Document]:
        """Run query through Perigon Vector API and parse results."""
        headers = {"x-api-key": self.perigon_api_key}
        params = self._generate_params(query, **config)

        response = requests.post(
            PERIGON_VECTOR_API_URL,
            json=params,
            headers=headers,
        )
        response.raise_for_status()

        return self._parse_results(response.json())

    async def results_async(
        self, query: str, config: Optional[PerigonVectorConfig] = None
    ) -> List[Document]:
        """Get results from Perigon Vector API asynchronously."""
        headers = {"x-api-key": self.perigon_api_key}
        params = self._generate_params(query, **config)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                PERIGON_VECTOR_API_URL,
                json=params,
                headers=headers,
            ) as response:
                if response.status == 200:
                    results = await response.json()
                    return self._parse_results(results)
                else:
                    raise Exception(f"Error {response.status}: {response.reason}")
