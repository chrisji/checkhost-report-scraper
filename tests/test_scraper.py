from pathlib import Path
from generate_test_data import get_example_report__check_http
from checkhost_scraper.scraper import CheckHostReportScraper


TEST_DATA_DIR = Path(__file__).parent / "data"


def test_check_http_report():

    page_html = (TEST_DATA_DIR / "example_report__check_http_23d52df5k770.html").read_text()
    expected_report = get_example_report__check_http()

    scraper = CheckHostReportScraper()
    obtained_report = scraper._parse_report(page_html)

    assert obtained_report.report_id == expected_report.report_id
    assert obtained_report.permalink == expected_report.permalink
    assert obtained_report.report_type == expected_report.report_type
    assert obtained_report.target == expected_report.target
    assert obtained_report.date == expected_report.date

    assert obtained_report.results[0] == expected_report.results[0]
    assert obtained_report.results[-1] == expected_report.results[-1]
