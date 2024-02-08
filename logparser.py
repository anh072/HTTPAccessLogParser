from abc import ABC, abstractclassmethod
from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappop, heappush
import re
from pathlib import Path
from typing import List, TypeAlias


IP: TypeAlias = str
URL: TypeAlias = str


@dataclass
class IHTTPAccessLogParser(ABC):
  regexPattern: str = r"^(\S*).*\[(.*)\]\s\"(\S*)\s(\S*)\s([^\"]*)\"\s(\S*)\s(\S*)\s\"([^\"]*)\"\s\"([^\"]*)\".*$"

  @abstractclassmethod
  def parse(self, filePath: Path):
    pass


@dataclass
class HTTPAccessLogParserWithHeap(IHTTPAccessLogParser):
  ips: defaultdict[int] = field(default_factory=lambda: defaultdict(int))
  urls: defaultdict[int] = field(default_factory=lambda: defaultdict(int))

  def parse(self, filePath: Path) -> None:
    with open(filePath, "r") as file:
      for line in file:
        result = re.match(self.regexPattern, line)
        ip = result.group(1)
        url = result.group(4)
        self.ips[ip] += 1
        self.urls[url] += 1
  
  def getTopKMostActiveIPs(self, k: int) -> List[IP]:
    heap = []
    for ip, numOccurences in self.ips.items():
      heappush(heap, (numOccurences, ip))
      if len(heap) > k:
        heappop(heap)
    res = []
    for i in range(k):
      if len(heap):
        _, ip = heappop(heap)
        res.append(ip)
    return res
  
  def getTopKVisitedUrls(self, k: int) -> List[URL]:
    heap = []
    for url, numOccurences in self.urls.items():
      heappush(heap, (numOccurences, url))
      if len(heap) > k:
        heappop(heap)
    res = []
    for i in range(k):
      if len(heap):
        _, url = heappop(heap)
        res.append(url)
    return res

  def getNumOfUniqueIPs(self) -> int:
    return len(self.ips)
