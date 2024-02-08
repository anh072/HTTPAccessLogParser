from pathlib import Path
from logparser import HTTPAccessLogParserWithHeap


if __name__ == "__main__":
  parser = HTTPAccessLogParserWithHeap()
  parser.parse(Path("access.log"))
  print(parser.getTopKMostActiveIPs(3))
  print(parser.getTopKVisitedUrls(3))
  print(parser.getNumOfUniqueIPs())