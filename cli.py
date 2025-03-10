import argparse
from pathlib import Path
from typing import Optional

from checkhost_scraper.scraper import CheckHostReportScraper


def process(scraper: CheckHostReportScraper, inputs: list[str], output_path: Optional[Path]):
    if output_path:
        _process_to_file(scraper, inputs, Path(output_path))
    else:
        _process_to_stdout(scraper, inputs)


def _process_to_stdout(scraper: CheckHostReportScraper, inputs: list[str]):
    for report_id in inputs:
        report = scraper.scrape(report_id)
        print(report.model_dump_json())


def _process_to_file(scraper: CheckHostReportScraper, inputs: list[str], output_path: Path):
    with open(output_path, "w") as out_f:
        for report_id in inputs:
            report = scraper.scrape(report_id)
            out_f.write(report.model_dump_json() + "\n")


def main():
    parser = argparse.ArgumentParser(description="Scrape check-host report")
    parser.add_argument("--report_id", type=str, help="The permalink ID of the report to scrape", required=False)
    parser.add_argument("--report_ids_file", type=str, help="The file containing the report IDs to scrape, one per line", required=False)
    parser.add_argument("--output_file", type=str, help="JSON lines file to write the scraped reports to", required=False)
    args = parser.parse_args()

    scraper = CheckHostReportScraper()
    
    if args.report_id:
        process(scraper, [args.report_id], args.output_file)    
    elif args.report_ids_file:
        report_ids = [_id.strip() for _id in Path(args.report_ids_file).read_text().splitlines() if _id.strip()]
        process(scraper, report_ids, args.output_file)
    else:
        parser.error("Either --report_id or --report_ids_file must be provided")


if __name__ == "__main__":
    main()