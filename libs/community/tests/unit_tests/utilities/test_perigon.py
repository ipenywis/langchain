from typing import Any, Dict, List, Optional, Union
from unittest.mock import AsyncMock, patch

import pytest
import responses
from langchain_core.documents import Document

TEST_ENDPOINT = "https://api.goperigon.com/v1/vector/news/all"


# Mock you.com response for testing
# Sample response for query: "Who won the recent F1 race?"
MOCK_RESULTS_JSON: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {
    "status": 200,
    "results": [
        {
            "score": 0.6573221,
            "data": {
                "articleId": "9f91577d118a4d0b80655ffa00b51a98",
                "clusterId": "f4312c03ce6e4e5199bf165c6256e849",
                "url": "https://www.sportskeeda.com/f1/ranked-no-races-since-f1-drivers-2024-grid-won-last-race",
                "imageUrl": "https://staticg.sportskeeda.com/editor/2024/08/4fa29-17237042334270-1920.jpg",
                "pubDate": "2024-08-15T08:18:59+00:00",
                "addDate": "2024-08-15T08:36:39.950816+00:00",
                "language": "en",
                "source": {"domain": "sportskeeda.com", "location": "null"},
                "country": "us",
                "reprint": "false",
                "reprintGroupId": "557cb35bc83944c5bce08f712f29b5e1",
                "title": "Ranked: No. of races since F1 drivers on the 2024 grid won their last race",
                "translatedTitle": "",
                "summary": "The number of races since current F1 drivers last won a race has been ranked at number one. Lewis Hamilton won the 2024 F1 Belgian GP, which was the last race before the summer break, but his teammate, George Russell, was disqualified due to underweight. Oscar Piastri, another McLaren driver, won his first race in Hungary earlier this year. However, his last official race win was in Austria where Max Verstappen won despite a collision with Lando Norris. Charles Leclerc's last win was six races ago, and Valtteri Bottas' last was in Turkey. Sergio Perez has not won a single race in the 2024 season, and Daniel Ricci's last victory was in 2021.",
                "translatedSummary": "",
                "labels": [],
                "topics": [{"name": "Motorsports"}, {"name": "Formula 1"}],
                "categories": [{"name": "Sports"}],
                "entities": [
                    {"data": "F1", "type": "ORG", "mentions": 4},
                    {"data": "McLaren", "type": "ORG", "mentions": 6},
                    {"data": "Red Bull", "type": "ORG", "mentions": 3},
                    {"data": "Ferrari", "type": "ORG", "mentions": 2},
                    {"data": "Mercedes", "type": "ORG", "mentions": 3},
                    {"data": "Alfa Romeo", "type": "ORG", "mentions": 1},
                    {"data": "Kick Sauber", "type": "ORG", "mentions": 1},
                    {"data": "Lewis Hamilton", "type": "PERSON", "mentions": 6},
                    {"data": "George Russell", "type": "PERSON", "mentions": 3},
                    {"data": "Oscar Piastri", "type": "PERSON", "mentions": 2},
                    {"data": "Lando Norris", "type": "PERSON", "mentions": 9},
                    {"data": "Verstappen", "type": "PERSON", "mentions": 8},
                    {"data": "Charles Leclerc", "type": "PERSON", "mentions": 1},
                    {"data": "Monegasque", "type": "PERSON", "mentions": 1},
                    {"data": "Carlos Sainz", "type": "PERSON", "mentions": 2},
                    {"data": "Oliver Bearman", "type": "PERSON", "mentions": 1},
                    {"data": "Sergio Perez", "type": "PERSON", "mentions": 2},
                    {"data": "Valtteri Bottas'", "type": "PERSON", "mentions": 2},
                    {"data": "Daniel Ricciardo's", "type": "PERSON", "mentions": 3},
                    {"data": "Esteban Ocon", "type": "PERSON", "mentions": 4},
                    {"data": "Alonso", "type": "PERSON", "mentions": 2},
                    {"data": "Pierre Gasly", "type": "PERSON", "mentions": 2},
                    {"data": "Sebastian Vettel", "type": "PERSON", "mentions": 1},
                    {"data": "Nico Rosberg", "type": "PERSON", "mentions": 1},
                    {"data": "Belgian GP", "type": "EVENT", "mentions": 6},
                    {"data": "the Grand Prix", "type": "EVENT", "mentions": 5},
                    {"data": "the Monaco GP", "type": "EVENT", "mentions": 1},
                    {"data": "the Miami GP", "type": "EVENT", "mentions": 1},
                    {"data": "Several hours", "type": "TIME", "mentions": 1},
                    {"data": "Hungary", "type": "GPE", "mentions": 2},
                    {"data": "Austria", "type": "GPE", "mentions": 1},
                    {"data": "Spain", "type": "GPE", "mentions": 1},
                    {"data": "Saudi Arabia", "type": "GPE", "mentions": 1},
                    {"data": "Azerbaijan", "type": "GPE", "mentions": 1},
                    {"data": "Turkey", "type": "GPE", "mentions": 1},
                    {"data": "Australian", "type": "NORP", "mentions": 3},
                    {"data": "British", "type": "NORP", "mentions": 1},
                    {"data": "Finnish", "type": "NORP", "mentions": 1},
                    {"data": "Alpine", "type": "NORP", "mentions": 1},
                    {"data": "Frenchman", "type": "NORP", "mentions": 1},
                    {"data": "Italian", "type": "NORP", "mentions": 1},
                ],
                "companies": [
                    {
                        "id": "a041be921af54bf485787b01c3697806",
                        "name": "Ferrari N.V.",
                        "domains": ["ferrari.com"],
                        "symbols": ["2FE.DE", "RACE", "RACE.MI", "RACE.SW"],
                    },
                    {
                        "id": "caf0d3c2e71045468fd2ffe727051ef7",
                        "name": "Alfa Romeo Automobiles S.p.A.",
                        "domains": ["alfaromeo.com"],
                        "symbols": [],
                    },
                    {
                        "id": "44ef16cef287460ea21356507428f1dc",
                        "name": "Mercedes-Benz Mexico",
                        "domains": ["mercedes-benz.com.mx"],
                        "symbols": [],
                    },
                    {
                        "id": "606ccb60d66849a18306f1fc5e0f0ef1",
                        "name": "McLaren",
                        "domains": ["mclaren.com"],
                        "symbols": [],
                    },
                    {
                        "id": "4643432b14444fb090c01fd58222d594",
                        "name": "Hotel F1",
                        "domains": ["hotelf1.accor.com"],
                        "symbols": [],
                    },
                ],
                "people": [
                    {"wikidataId": "Q28741262", "name": "Oscar Piastri"},
                    {"wikidataId": "Q138745", "name": "Valtteri Bottas"},
                    {"wikidataId": "Q15074165", "name": "Esteban Ocon"},
                    {"wikidataId": "Q211204", "name": "Carlos Sainz"},
                    {"wikidataId": "Q82805", "name": "Sergio Pérez"},
                    {"wikidataId": "Q17541912", "name": "Charles Leclerc"},
                    {"wikidataId": "Q82816", "name": "Daniel Ricciardo"},
                    {"wikidataId": "Q11816647", "name": "Pierre Gasly"},
                    {"wikidataId": "Q10514", "name": "Fernando Alonso"},
                    {"wikidataId": "Q107023292", "name": "Oliver Bearman"},
                    {"wikidataId": "Q42311", "name": "Sebastian Vettel"},
                    {"wikidataId": "Q75820", "name": "Nico Rosberg"},
                    {"wikidataId": "Q9673", "name": "Lewis Hamilton"},
                    {"wikidataId": "Q2239218", "name": "Max Verstappen"},
                    {"wikidataId": "Q22007193", "name": "Lando Norris"},
                    {"wikidataId": "Q17319645", "name": "George Russell"},
                ],
                "locations": [],
                "places": [],
            },
        },
        {
            "score": 0.6089887,
            "data": {
                "articleId": "e50df677689343148b986dce01357e0a",
                "clusterId": "f4312c03ce6e4e5199bf165c6256e849",
                "url": "https://www.sportskeeda.com/f1/ranked-no-f1-podiums-took-drivers-2024-grid-win-first-race",
                "imageUrl": "https://staticg.sportskeeda.com/editor/2024/08/bdae3-17237030648394-1920.jpg",
                "pubDate": "2024-08-15T08:04:00+00:00",
                "addDate": "2024-08-15T08:21:30.641014+00:00",
                "language": "en",
                "source": {"domain": "sportskeeda.com", "location": "null"},
                "country": "us",
                "reprint": "false",
                "reprintGroupId": "05fcf6ad37274fb496a83734b1aecc38",
                "title": "Ranked: No. of F1 podiums it took for drivers on the 2024 grid to win their first race",
                "translatedTitle": "",
                "summary": "Currently, there are only 13 drivers currently on the F1 grid that have won their first race. The list includes Max Verstappen, the youngest race winner in the sport at 18, and Esteban Ocon, the current Alpine F1 driver, who won his first race at the Hungarian GP in 2021. Other drivers included Daniel Ricciardo, Fernando Alonso, and Oscar Piastri, who have previously taken podiums in Japan and Qatar in 2023, Austria, and Monaco this year. Lewis Hamilton and Lewis Rosberg were the standout drivers in F1 history during the 2007 season. George Russell had a remarkable debut season with a win in the German Grand Prix, which he followed up with a podium win in Indianapolis.",
                "translatedSummary": "",
                "labels": [],
                "topics": [{"name": "Motorsports"}, {"name": "Formula 1"}],
                "categories": [{"name": "Sports"}],
                "entities": [
                    {"data": "F1", "type": "ORG", "mentions": 5},
                    {"data": "Toro Rosso", "type": "ORG", "mentions": 1},
                    {"data": "Red Bull", "type": "ORG", "mentions": 3},
                    {"data": "Mercedes", "type": "ORG", "mentions": 3},
                    {"data": "Alpine", "type": "ORG", "mentions": 1},
                    {"data": "AlphaTauri", "type": "ORG", "mentions": 1},
                    {"data": "Renault", "type": "ORG", "mentions": 1},
                    {"data": "Ferrari", "type": "ORG", "mentions": 2},
                    {"data": "McLaren", "type": "ORG", "mentions": 2},
                    {"data": "Williams", "type": "ORG", "mentions": 1},
                    {"data": "Max Verstappen's", "type": "PERSON", "mentions": 4},
                    {"data": "Daniil Kvyat", "type": "PERSON", "mentions": 1},
                    {"data": "Lewis Hamilton", "type": "PERSON", "mentions": 4},
                    {"data": "Nico Rosberg", "type": "PERSON", "mentions": 2},
                    {"data": "Esteban Ocon", "type": "PERSON", "mentions": 3},
                    {"data": "Sebastian Vettel", "type": "PERSON", "mentions": 3},
                    {"data": "Pierre Gasly", "type": "PERSON", "mentions": 2},
                    {"data": "Carlos Sainz", "type": "PERSON", "mentions": 2},
                    {"data": "Daniel Ricciardo", "type": "PERSON", "mentions": 1},
                    {"data": "Sergio Perez", "type": "PERSON", "mentions": 2},
                    {"data": "Felipe Massa", "type": "PERSON", "mentions": 1},
                    {"data": "Fernando Alonso", "type": "PERSON", "mentions": 1},
                    {"data": "Jenson Button", "type": "PERSON", "mentions": 1},
                    {"data": "Oscar Piastri", "type": "PERSON", "mentions": 2},
                    {"data": "Lando Norris", "type": "PERSON", "mentions": 5},
                    {"data": "Charles Leclerc", "type": "PERSON", "mentions": 2},
                    {"data": "Anthoine Hubert", "type": "PERSON", "mentions": 1},
                    {"data": "George Russell", "type": "PERSON", "mentions": 1},
                    {"data": "Dutch", "type": "NORP", "mentions": 1},
                    {"data": "Austrian", "type": "NORP", "mentions": 1},
                    {"data": "Frenchman", "type": "NORP", "mentions": 3},
                    {"data": "Italian", "type": "NORP", "mentions": 2},
                    {"data": "Aussie", "type": "NORP", "mentions": 1},
                    {"data": "German", "type": "NORP", "mentions": 1},
                    {"data": "Mexican", "type": "NORP", "mentions": 1},
                    {"data": "Finnish", "type": "NORP", "mentions": 1},
                    {"data": "the Hungarian GP", "type": "EVENT", "mentions": 6},
                    {"data": "Brazilian GP", "type": "EVENT", "mentions": 1},
                    {"data": "Canadian GP", "type": "EVENT", "mentions": 1},
                    {"data": "Turn 1", "type": "FAC", "mentions": 2},
                    {"data": "the Hungaroring", "type": "FAC", "mentions": 1},
                    {"data": "Spa", "type": "FAC", "mentions": 1},
                    {"data": "Interlagos", "type": "FAC", "mentions": 1},
                    {"data": "Miami", "type": "FAC", "mentions": 1},
                    {"data": "Australia", "type": "GPE", "mentions": 3},
                    {"data": "Spain", "type": "GPE", "mentions": 2},
                    {"data": "Monaco", "type": "GPE", "mentions": 2},
                    {"data": "Montreal", "type": "GPE", "mentions": 2},
                    {"data": "Malaysia", "type": "GPE", "mentions": 1},
                    {"data": "Brazil", "type": "GPE", "mentions": 1},
                    {"data": "Japan", "type": "GPE", "mentions": 1},
                    {"data": "Qatar", "type": "GPE", "mentions": 1},
                    {"data": "Bahrain", "type": "GPE", "mentions": 1},
                    {"data": "France", "type": "GPE", "mentions": 1},
                    {"data": "Silverstone", "type": "GPE", "mentions": 1},
                    {"data": "Canada", "type": "GPE", "mentions": 1},
                    {"data": "Indianapolis", "type": "GPE", "mentions": 1},
                    {"data": "F1", "type": "PRODUCT", "mentions": 5},
                ],
                "companies": [
                    {
                        "id": "606ccb60d66849a18306f1fc5e0f0ef1",
                        "name": "McLaren",
                        "domains": ["mclaren.com"],
                        "symbols": [],
                    },
                    {
                        "id": "a041be921af54bf485787b01c3697806",
                        "name": "Ferrari N.V.",
                        "domains": ["ferrari.com"],
                        "symbols": ["2FE.DE", "RACE", "RACE.MI", "RACE.SW"],
                    },
                    {
                        "id": "b40dc389506141a4bcd5ba94f64592f6",
                        "name": "Red Bull",
                        "domains": ["redbullracing.com"],
                        "symbols": [],
                    },
                    {
                        "id": "6326b2384b024b06978390920ff06048",
                        "name": "Mercedes AMG High Performance Powertrains",
                        "domains": ["mercedes-amg-hpp.com"],
                        "symbols": [],
                    },
                    {
                        "id": "44ef16cef287460ea21356507428f1dc",
                        "name": "Mercedes-Benz Mexico",
                        "domains": ["mercedes-benz.com.mx"],
                        "symbols": [],
                    },
                ],
                "people": [
                    {"wikidataId": "Q11816647", "name": "Pierre Gasly"},
                    {"wikidataId": "Q2239218", "name": "Max Verstappen"},
                    {"wikidataId": "Q211204", "name": "Carlos Sainz"},
                    {"wikidataId": "Q17541912", "name": "Charles Leclerc"},
                    {"wikidataId": "Q82816", "name": "Daniel Ricciardo"},
                    {"wikidataId": "Q17319645", "name": "George Russell"},
                    {"wikidataId": "Q42311", "name": "Sebastian Vettel"},
                    {"wikidataId": "Q10514", "name": "Fernando Alonso"},
                    {"wikidataId": "Q10510", "name": "Jenson Button"},
                    {"wikidataId": "Q16529407", "name": "Anthoine Hubert"},
                    {"wikidataId": "Q15074165", "name": "Esteban Ocon"},
                    {"wikidataId": "Q82652", "name": "Felipe Massa"},
                    {"wikidataId": "Q28741262", "name": "Oscar Piastri"},
                    {"wikidataId": "Q22007193", "name": "Lando Norris"},
                    {"wikidataId": "Q9673", "name": "Lewis Hamilton"},
                    {"wikidataId": "Q979668", "name": "Daniil Kvyat"},
                    {"wikidataId": "Q82805", "name": "Sergio Pérez"},
                    {"wikidataId": "Q75820", "name": "Nico Rosberg"},
                ],
                "locations": [],
                "places": [],
            },
        },
    ],
}


def generate_parsed_metadata(num: Optional[int] = 0) -> Dict[Any, Any]:
    """generate metadata for testing"""
    if num is None:
        num = 0
    result: Dict[str, Union[str, List[str]]] = MOCK_RESULTS_JSON["results"][num].get(
        "data", {}
    )
    return {
        "title": result.get("title"),
        "url": result.get("url"),
        "source": result.get("source"),
        "published_date": result.get("publishedDate"),
        "add_date": result.get("addDate"),
        "language": result.get("language"),
        "imageUrl": result.get("imageUrl"),
        "entities": ", ".join(
            [entity["data"] for entity in result.get("entities", [])]
        ),
        "categories": ", ".join(
            [category["name"] for category in result.get("categories", [])]
        ),
        "topics": ", ".join([topic["name"] for topic in result.get("topics", [])]),
        "companies": ", ".join(
            [company["name"] for company in result.get("companies", [])]
        ),
        "people": ", ".join([person["name"] for person in result.get("people", [])]),
    }


def generate_parsed_output(num: Optional[int] = 0) -> List[Document]:
    """generate parsed output for testing"""
    if num is None:
        num = 0
    results: Dict[str, Union[str, List[str]]] = MOCK_RESULTS_JSON["results"][num]
    article_data = results.get("data", {})
    document = Document(
        page_content=article_data.get("summary", ""),
        metadata=generate_parsed_metadata(num),
    )
    return [document]


# # Mock results after parsing
MOCK_DOCUMENTS_OUTPUT = generate_parsed_output()
print("MOCK_DOCUMENTS_OUTPUT: ", MOCK_DOCUMENTS_OUTPUT)
MOCK_DOCUMENTS_OUTPUT.extend(generate_parsed_output(1))
# # Single-snippet
# LIMITED_PARSED_OUTPUT = []
# LIMITED_PARSED_OUTPUT.append(generate_parsed_output()[0])
# LIMITED_PARSED_OUTPUT.append(generate_parsed_output(1)[0])

# # copied from you api docs
# NEWS_RESPONSE_RAW = {
#     "news": {
#         "results": [
#             {
#                 "age": "18 hours ago",
#                 "breaking": True,
#                 "description": "Search on YDC for the news",
#                 "meta_url": {
#                     "hostname": "www.reuters.com",
#                     "netloc": "reuters.com",
#                     "path": "› 2023  › 10  › 18  › politics  › inflation  › index.html",
#                     "scheme": "https",
#                 },
#                 "page_age": "2 days",
#                 "page_fetched": "2023-10-12T23:00:00Z",
#                 "thumbnail": {"original": "https://reuters.com/news.jpg"},
#                 "title": "Breaking News about the World's Greatest Search Engine!",
#                 "type": "news",
#                 "url": "https://news.you.com",
#             }
#         ]
#     }
# }

# NEWS_RESPONSE_PARSED = [
#     Document(page_content=str(result["description"]), metadata=result)
#     for result in NEWS_RESPONSE_RAW["news"]["results"]
# ]


# @responses.activate
# def test_raw_results() -> None:
#     responses.add(
#         responses.GET, f"{TEST_ENDPOINT}/search", json=MOCK_RESPONSE_RAW, status=200
#     )

#     query = "Test query text"
#     # ensure default endpoint_type
#     you_wrapper = YouSearchAPIWrapper(endpoint_type="snippet", ydc_api_key="test")
#     raw_results = you_wrapper.raw_results(query)
#     expected_result = MOCK_RESPONSE_RAW
#     assert raw_results == expected_result


# @responses.activate
# def test_raw_results_defaults() -> None:
#     responses.add(
#         responses.GET, f"{TEST_ENDPOINT}/search", json=MOCK_RESPONSE_RAW, status=200
#     )

#     query = "Test query text"
#     # ensure limit on number of docs returned
#     you_wrapper = YouSearchAPIWrapper(ydc_api_key="test")
#     raw_results = you_wrapper.raw_results(query)
#     expected_result = MOCK_RESPONSE_RAW
#     assert raw_results == expected_result


# @responses.activate
# def test_raw_results_news() -> None:
#     responses.add(
#         responses.GET, f"{TEST_ENDPOINT}/news", json=NEWS_RESPONSE_RAW, status=200
#     )

#     query = "Test news text"
#     # ensure limit on number of docs returned
#     you_wrapper = YouSearchAPIWrapper(endpoint_type="news", ydc_api_key="test")
#     raw_results = you_wrapper.raw_results(query)
#     expected_result = NEWS_RESPONSE_RAW
#     assert raw_results == expected_result


# @responses.activate
# def test_results() -> None:
#     responses.add(
#         responses.GET, f"{TEST_ENDPOINT}/search", json=MOCK_RESPONSE_RAW, status=200
#     )

#     query = "Test query text"
#     you_wrapper = YouSearchAPIWrapper(ydc_api_key="test")
#     results = you_wrapper.results(query)
#     expected_result = MOCK_PARSED_OUTPUT
#     assert results == expected_result


# @responses.activate
# def test_results_max_docs() -> None:
#     responses.add(
#         responses.GET, f"{TEST_ENDPOINT}/search", json=MOCK_RESPONSE_RAW, status=200
#     )

#     query = "Test query text"
#     you_wrapper = YouSearchAPIWrapper(k=2, ydc_api_key="test")
#     results = you_wrapper.results(query)
#     expected_result = generate_parsed_output()
#     assert results == expected_result


# @responses.activate
# def test_results_limit_snippets() -> None:
#     responses.add(
#         responses.GET, f"{TEST_ENDPOINT}/search", json=MOCK_RESPONSE_RAW, status=200
#     )

#     query = "Test query text"
#     you_wrapper = YouSearchAPIWrapper(n_snippets_per_hit=1, ydc_api_key="test")
#     results = you_wrapper.results(query)
#     expected_result = LIMITED_PARSED_OUTPUT
#     assert results == expected_result


# @responses.activate
# def test_results_news() -> None:
#     responses.add(
#         responses.GET, f"{TEST_ENDPOINT}/news", json=NEWS_RESPONSE_RAW, status=200
#     )

#     query = "Test news text"
#     # ensure limit on number of docs returned
#     you_wrapper = YouSearchAPIWrapper(endpoint_type="news", ydc_api_key="test")
#     raw_results = you_wrapper.results(query)
#     expected_result = NEWS_RESPONSE_PARSED
#     assert raw_results == expected_result


# @pytest.mark.asyncio
# async def test_raw_results_async() -> None:
#     instance = YouSearchAPIWrapper(ydc_api_key="test_api_key")

#     # Mock response object to simulate aiohttp response
#     mock_response = AsyncMock()
#     mock_response.__aenter__.return_value = (
#         mock_response  # Make the context manager return itself
#     )
#     mock_response.__aexit__.return_value = None  # No value needed for exit
#     mock_response.status = 200
#     mock_response.json = AsyncMock(return_value=MOCK_RESPONSE_RAW)

#     # Patch the aiohttp.ClientSession object
#     with patch("aiohttp.ClientSession.get", return_value=mock_response):
#         results = await instance.raw_results_async("test query")
#         assert results == MOCK_RESPONSE_RAW


# @pytest.mark.asyncio
# async def test_results_async() -> None:
#     instance = YouSearchAPIWrapper(ydc_api_key="test_api_key")

#     # Mock response object to simulate aiohttp response
#     mock_response = AsyncMock()
#     mock_response.__aenter__.return_value = (
#         mock_response  # Make the context manager return itself
#     )
#     mock_response.__aexit__.return_value = None  # No value needed for exit
#     mock_response.status = 200
#     mock_response.json = AsyncMock(return_value=MOCK_RESPONSE_RAW)

#     # Patch the aiohttp.ClientSession object
#     with patch("aiohttp.ClientSession.get", return_value=mock_response):
#         results = await instance.results_async("test query")
#         assert results == MOCK_PARSED_OUTPUT


# @pytest.mark.asyncio
# async def test_results_news_async() -> None:
#     instance = YouSearchAPIWrapper(endpoint_type="news", ydc_api_key="test_api_key")

#     # Mock response object to simulate aiohttp response
#     mock_response = AsyncMock()
#     mock_response.__aenter__.return_value = (
#         mock_response  # Make the context manager return itself
#     )
#     mock_response.__aexit__.return_value = None  # No value needed for exit
#     mock_response.status = 200
#     mock_response.json = AsyncMock(return_value=NEWS_RESPONSE_RAW)

#     # Patch the aiohttp.ClientSession object
#     with patch("aiohttp.ClientSession.get", return_value=mock_response):
#         results = await instance.results_async("test query")
#         assert results == NEWS_RESPONSE_PARSED
