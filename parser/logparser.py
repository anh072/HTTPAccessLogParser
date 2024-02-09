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
    regexPattern: str = (
        r"^(\S*).*\[(.*)\]\s\"(\S*)\s(\S*)\s([^\"]*)\"\s(\S*)\s(\S*)\s\"([^\"]*)\"\s\"([^\"]*)\".*$"
    )

    @abstractmethod
    def parse(self, filePath: Path) -> None:
        pass

    @abstractmethod
    def getTopKMostActiveIPs(self, k: int) -> List[IP]:
        pass

    @abstractmethod
    def getTopKVisitedUrls(self, k: int) -> List[URL]:
        pass


@dataclass
class HTTPAccessLogParserWithHeap(IHTTPAccessLogParser):
    ips: DefaultDict[IP, int] = field(default_factory=lambda: defaultdict(int))
    urls: DefaultDict[URL, int] = field(default_factory=lambda: defaultdict(int))

    def parse(self, filePath: Path) -> None:
        try:
            with filePath.open(mode="r", encoding="utf-8") as file:
                for line in file:
                    result = re.match(self.regexPattern, line)
                    if result:
                        ip = result.group(1)
                        url = result.group(4)
                        self.ips[ip] += 1
                        self.urls[url] += 1
        except FileNotFoundError as e:
            print(f"File {filePath.name} is not found")
        except:
            print(f"Cannot open file {filePath.name}")

    def getTopKMostActiveIPs(self, k: int) -> List[IP]:
        heap: List[tuple[int, IP]] = []
        for ip, numOccurences in self.ips.items():
            heappush(heap, (numOccurences, ip))
            if len(heap) > k:
                heappop(heap)
        res = []
        for _ in range(k):
            if len(heap):
                _, ip = heappop(heap)
                res.append(ip)
        res.reverse()
        return res

    def getTopKVisitedUrls(self, k: int) -> List[URL]:
        heap: List[tuple[int, URL]] = []
        for url, numOccurences in self.urls.items():
            heappush(heap, (numOccurences, url))
            if len(heap) > k:
                heappop(heap)
        res = []
        for _ in range(k):
            if len(heap):
                _, url = heappop(heap)
                res.append(url)
        res.reverse()
        return res

    def getNumOfUniqueIPs(self) -> int:
        return len(self.ips)
