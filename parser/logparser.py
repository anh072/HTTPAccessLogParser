from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappop, heappush
from pathlib import Path
import re
from typing import DefaultDict, List, TypeAlias


IP: TypeAlias = str
URL: TypeAlias = str


@dataclass
class IHTTPAccessLogParser(ABC):
    regex_pattern: str = (
        r"^(\S*).*\[(.*)\]\s\"(\S*)\s(\S*)\s([^\"]*)\"\s(\S*)\s(\S*)\s\"([^\"]*)\"\s\"([^\"]*)\".*$"
    )

    @abstractmethod
    def parse(self, file_path: Path) -> None:
        pass

    @abstractmethod
    def get_top_k_most_active_ips(self, k: int) -> List[IP]:
        pass

    @abstractmethod
    def get_top_k_visited_urls(self, k: int) -> List[URL]:
        pass

    @abstractmethod
    def get_number_of_unique_ips(self) -> int:
        pass


@dataclass
class HTTPAccessLogParserWithHeap(IHTTPAccessLogParser):
    ips: DefaultDict[IP, int] = field(default_factory=lambda: defaultdict(int))
    urls: DefaultDict[URL, int] = field(default_factory=lambda: defaultdict(int))

    def parse(self, file_path: Path) -> None:
        try:
            with file_path.open(mode="r", encoding="utf-8") as file:
                for line in file:
                    result = re.match(self.regex_pattern, line)
                    if result:
                        ip = result.group(1)
                        url = result.group(4)
                        self.ips[ip] += 1
                        self.urls[url] += 1
        except FileNotFoundError as e:
            print(f"File {file_path.name} is not found")
        except:
            print(f"Cannot open file {file_path.name}")

    def get_top_k_most_active_ips(self, k: int) -> List[IP]:
        heap: List[tuple[int, IP]] = []
        for ip, num_occurences in self.ips.items():
            heappush(heap, (num_occurences, ip))
            if len(heap) > k:
                heappop(heap)
        res = []
        for _ in range(k):
            if len(heap):
                _, ip = heappop(heap)
                res.append(ip)
        res.reverse()
        return res

    def get_top_k_visited_urls(self, k: int) -> List[URL]:
        heap: List[tuple[int, URL]] = []
        for url, num_occurences in self.urls.items():
            heappush(heap, (num_occurences, url))
            if len(heap) > k:
                heappop(heap)
        res = []
        for _ in range(k):
            if len(heap):
                _, url = heappop(heap)
                res.append(url)
        res.reverse()
        return res

    def get_number_of_unique_ips(self) -> int:
        return len(self.ips)
