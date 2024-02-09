from pathlib import Path
from typing import List
import unittest

from parser import IP, URL, HTTPAccessLogParserWithHeap


p = Path(__file__).resolve().parent


class HTTPAccessLogParserWithHeapTest(unittest.TestCase):
    def setUp(self) -> None:
        file = p / "access.log"
        self.parser = HTTPAccessLogParserWithHeap()
        self.parser.parse(file)

    def test_get_num_unique_ips(self) -> None:
        self.assertEqual(self.parser.getNumOfUniqueIPs(), 11)

    def test_get_most_active_ips(self) -> None:
        expectedResult: List[IP] = ["168.41.191.40", "72.44.32.10", "50.112.00.11"]
        actualResult = self.parser.getTopKMostActiveIPs(3)
        self.assertListEqual(actualResult, expectedResult)

    def test_get_most_visited_urls(self) -> None:
        expectedResult: List[URL] = [
            "/docs/manage-websites/",
            "http://example.net/faq/",
            "http://example.net/blog/category/meta/",
        ]
        actualResult = self.parser.getTopKVisitedUrls(3)
        self.assertListEqual(actualResult, expectedResult)


class HTTPAccessLogParserWithHeapEmptyDataTest(unittest.TestCase):
    def setUp(self) -> None:
        file = p / "empty.access.log"
        self.parser = HTTPAccessLogParserWithHeap()
        self.parser.parse(file)

    def test_get_num_unique_ips(self) -> None:
        self.assertEqual(self.parser.getNumOfUniqueIPs(), 0)

    def test_get_most_active_ips(self) -> None:
        expectedResult: List[IP] = []
        actualResult = self.parser.getTopKMostActiveIPs(3)
        self.assertListEqual(actualResult, expectedResult)

    def test_get_most_visited_urls(self) -> None:
        expectedResult: List[URL] = []
        actualResult = self.parser.getTopKVisitedUrls(3)
        self.assertListEqual(actualResult, expectedResult)


class HTTPAccessLogParserWithHeapLessThanKTest(unittest.TestCase):
    def setUp(self) -> None:
        file = p / "less_than_three.access.log"
        self.parser = HTTPAccessLogParserWithHeap()
        self.parser.parse(file)

    def test_get_num_unique_ips(self) -> None:
        self.assertEqual(self.parser.getNumOfUniqueIPs(), 2)

    def test_get_most_active_ips(self) -> None:
        expectedResult: List[IP] = ["177.71.128.21", "168.41.191.40"]
        actualResult = self.parser.getTopKMostActiveIPs(3)
        self.assertListEqual(actualResult, expectedResult)

    def test_get_most_visited_urls(self) -> None:
        expectedResult: List[URL] = ["http://example.net/faq/", "/intranet-analytics/"]
        actualResult = self.parser.getTopKVisitedUrls(3)
        self.assertListEqual(actualResult, expectedResult)
