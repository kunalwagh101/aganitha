import argparse
import logging
from aganitha.pubmed_fetcher import PubMedFetcher

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output.")
    parser.add_argument("-f", "--file", type=str, help="Output filename (CSV).")
    args = parser.parse_args()

    fetcher = PubMedFetcher(api_key="25778206d420606b80b20a420eef37ce4608")

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    try:
        paper_ids = fetcher.fetch_paper_ids(args.query)
        if args.debug:
            print(f"Found {len(paper_ids)} papers.")

        paper_details = fetcher.fetch_paper_details(paper_ids)
        if args.file:
            fetcher.save_to_csv(paper_details, args.file)
            print(f"Results saved to {args.file}")
        else:
            for paper in paper_details:
                print(paper)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()