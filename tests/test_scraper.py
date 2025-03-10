import pytest
from pathlib import Path
from generate_test_data import (
    get_example_report__check_http,
    get_example_report__check_dns,
    get_example_report__check_ping,
    get_example_report__check_udp,
    get_example_report__check_tcp,
)
from checkhost_scraper.scraper import CheckHostReportScraper
from checkhost_scraper.models import CheckHostReport


TEST_DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="module")
def scraper():
    return CheckHostReportScraper()


def _check_report_equals(obtained_report: CheckHostReport, expected_report: CheckHostReport):
    # Check report metadata
    assert obtained_report.report_id == expected_report.report_id
    assert obtained_report.permalink == expected_report.permalink
    assert obtained_report.report_type == expected_report.report_type
    assert obtained_report.target == expected_report.target
    assert obtained_report.date == expected_report.date
    # Check the first and last results
    assert obtained_report.results[0] == expected_report.results[0]
    assert obtained_report.results[-1] == expected_report.results[-1]


def test_check_http_report(scraper: CheckHostReportScraper):
    page_html = (TEST_DATA_DIR / "example_report__check_http_23d52df5k770.html").read_text()
    expected_report = get_example_report__check_http()
    obtained_report = scraper._parse_report(page_html)
    _check_report_equals(obtained_report, expected_report)


def test_check_dns_report(scraper: CheckHostReportScraper):
    page_html = (TEST_DATA_DIR / "example_report__check_dns_23e21752kd44.html").read_text()
    expected_report = get_example_report__check_dns()
    obtained_report = scraper._parse_report(page_html)
    _check_report_equals(obtained_report, expected_report)


def test_check_ping_report(scraper: CheckHostReportScraper):
    page_html = (TEST_DATA_DIR / "example_report__check_ping_23d58148k840.html").read_text()
    expected_report = get_example_report__check_ping()
    obtained_report = scraper._parse_report(page_html)
    _check_report_equals(obtained_report, expected_report)


def test_check_udp_report(scraper: CheckHostReportScraper):
    page_html = (TEST_DATA_DIR / "example_report__check_udp_23e215c0k319.html").read_text()
    expected_report = get_example_report__check_udp()
    obtained_report = scraper._parse_report(page_html)
    _check_report_equals(obtained_report, expected_report)


def test_check_tcp_report(scraper: CheckHostReportScraper):
    page_html = (TEST_DATA_DIR / "example_report__check_tcp_23d581e0k7a.html").read_text()
    expected_report = get_example_report__check_tcp()
    obtained_report = scraper._parse_report(page_html)
    _check_report_equals(obtained_report, expected_report)
    