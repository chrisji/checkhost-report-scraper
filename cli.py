import argparse

from checkhost_scraper.scraper import CheckHostReportScraper


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape check-host report")
    parser.add_argument("report_id", type=str, help="The permalink ID of the report to scrape")
    args = parser.parse_args()

    scraper = CheckHostReportScraper()
    report = scraper.scrape(args.report_id)
    
    print(report.model_dump_json())
