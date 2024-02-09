from parser import HTTPAccessLogParserWithHeap


if __name__ == "__main__":
    parser = HTTPAccessLogParserWithHeap()
    parser.parse("tests/access.log")
    print(parser.getTopKMostActiveIPs(3))
    print(parser.getTopKVisitedUrls(3))
    print(parser.getNumOfUniqueIPs())
