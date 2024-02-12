from pathlib import Path
from parser import HTTPAccessLogParserWithHeap


if __name__ == "__main__":
    parser = HTTPAccessLogParserWithHeap()
    parser.parse(Path("tests/access.log"))
    print(parser.get_top_k_most_active_ips(3))
    print(parser.get_top_k_visited_urls(3))
    print(parser.get_number_of_unique_ips())
