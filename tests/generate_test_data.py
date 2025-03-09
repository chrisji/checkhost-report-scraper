import requests
from pathlib import Path

from checkhost_scraper.scraper import CheckHostReport, CheckHttpReportResult

TEST_DATA_DIR = Path(__file__).parent / "data"


def dump_example_report_html__check_http():
    # Get "check-http" report page and save it to a file
    url = "https://check-host.net/check-report/23d52df5k770?lang=en"
    response = requests.get(url)
    with open(TEST_DATA_DIR / "example_report__check_http_23d52df5k770.html", "w") as f:
        f.write(response.text)


def get_example_report__check_http():
    # Create corresponding 'expected' report and dump it to a file
    return CheckHostReport(
        report_id="23d52df5k770",
        permalink="https://check-host.net/check-report/23d52df5k770",
        report_type="check-http",
        target="https://1.1.1.1",
        date="2025-03-08T20:28:15",
        results=[
            CheckHttpReportResult(
                location="Brazil, Sao Paulo",
                result="OK",
                time="0.037 s",
                code="301 (Moved Permanently)",
                ip="1.1.1.1"
            ),
            # TODO: add middle results, if we want more tests.
            CheckHttpReportResult(
                location="Vietnam, Ho Chi Minh City",
                result="OK",
                time="0.180 s",
                code="301 (Moved Permanently)",
                ip="1.1.1.1"
            )
        ]
    )


def dump_example_report_html__ping_server():
    # Get "Ping" report page and save it to a file
    url = "https://check-host.net/check-report/23d58148k840?lang=en"
    response = requests.get(url)
    with open(TEST_DATA_DIR / "example_report__ping_server_23d58148k840.html", "w") as f:
        f.write(response.text)


def dump_example_report_html__tcp_connect():
    # Get "TCP" report page and save it to a file
    url = "https://check-host.net/check-report/23d581e0k7a?lang=en"
    response = requests.get(url)
    with open(TEST_DATA_DIR / "example_report__tcp_connect_23d581e0k7a.html", "w") as f:
        f.write(response.text)


def main():
    dump_example_report_html__check_http()
    dump_example_report_html__ping_server()
    dump_example_report_html__tcp_connect()


if __name__ == "__main__":
    main()
