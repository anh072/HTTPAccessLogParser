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
        self.assertEqual(self.parser.get_number_of_unique_ips(), 11)

    def test_get_most_active_ips(self) -> None:
        expected_result: List[IP] = ["168.41.191.40", "72.44.32.10", "50.112.00.11"]
        actual_result = self.parser.get_top_k_most_active_ips(3)
        self.assertListEqual(actual_result, expected_result)

    def test_get_most_visited_urls(self) -> None:
        expected_result: List[URL] = [
            "/docs/manage-websites/",
            "http://example.net/faq/",
            "http://example.net/blog/category/meta/",
        ]
        actual_result = self.parser.get_top_k_visited_urls(3)
        self.assertListEqual(actual_result, expected_result)


class HTTPAccessLogParserWithHeapEmptyDataTest(unittest.TestCase):
    def setUp(self) -> None:
        file = p / "empty.access.log"
        self.parser = HTTPAccessLogParserWithHeap()
        self.parser.parse(file)

    def test_get_num_unique_ips(self) -> None:
        self.assertEqual(self.parser.get_number_of_unique_ips(), 0)

    def test_get_most_active_ips(self) -> None:
        expected_result: List[IP] = []
        actual_result = self.parser.get_top_k_most_active_ips(3)
        self.assertListEqual(actual_result, expected_result)

    def test_get_most_visited_urls(self) -> None:
        expected_result: List[URL] = []
        actual_result = self.parser.get_top_k_visited_urls(3)
        self.assertListEqual(actual_result, expected_result)


class HTTPAccessLogParserWithHeapLessThanThreeTest(unittest.TestCase):
    def setUp(self) -> None:
        file = p / "less_than_three.access.log"
        self.parser = HTTPAccessLogParserWithHeap()
        self.parser.parse(file)
        self.k = 3

    def test_get_num_unique_ips(self) -> None:
        self.assertEqual(self.parser.get_number_of_unique_ips(), 2)

    def test_get_most_active_ips(self) -> None:
        expected_result: List[IP] = ["177.71.128.21", "168.41.191.40"]
        actual_result = self.parser.get_top_k_most_active_ips(self.k)
        self.assertListEqual(actual_result, expected_result)

    def test_get_most_visited_urls(self) -> None:
        expected_result: List[URL] = ["http://example.net/faq/", "/intranet-analytics/"]
        actual_result = self.parser.get_top_k_visited_urls(self.k)
        self.assertListEqual(actual_result, expected_result)
