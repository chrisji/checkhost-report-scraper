from selenium import webdriver
from pathlib import Path

from checkhost_scraper.scraper import CheckHostReport
from checkhost_scraper.models import (
    CheckHostReport,
    CheckHttpReportResult,
    CheckDnsReportResult,
    CheckPingReportResult,
    CheckTcpReportResult,
    CheckUdpReportResult
)


TEST_DATA_DIR = Path(__file__).parent / "data"

# Set-up selenium driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


def _get_source(url: str) -> str:
    """
    Fetches the HTML source of a webpage and returns it as a string."
    """
    # Selenium-based implementation
    driver.get(url)
    response_text = driver.page_source
    return response_text


def dump_example_report_html__check_http():
    # Get "check-http" report page and save it to a file
    url = "https://check-host.net/check-report/23d52df5k770?lang=en"
    page_source = _get_source(url)
    with open(TEST_DATA_DIR / "example_report__check_http_23d52df5k770.html", "w") as f:
        f.write(page_source)


def get_example_report__check_http():
    return CheckHostReport(
        report_id="23d52df5k770",
        permalink="https://check-host.net/check-report/23d52df5k770",
        report_type="check-http",
        target="https://1.1.1.1",
        date="2025-03-08T20:28:15",
        results=[
            CheckHttpReportResult(
                country_code="BR",
                location="Brazil, Sao Paulo",
                result="OK",
                time="0.037 s",
                code="301 (Moved Permanently)",
                ip="1.1.1.1"
            ),
            # TODO: add middle results, if we want more tests.
            CheckHttpReportResult(
                country_code="VN",
                location="Vietnam, Ho Chi Minh City",
                result="OK",
                time="0.180 s",
                code="301 (Moved Permanently)",
                ip="1.1.1.1"
            )
        ]
    )


def dump_example_report_html__check_ping():
    # Get "Ping" report page and save it to a file
    url = "https://check-host.net/check-report/23d58148k840?lang=en"
    page_source = _get_source(url)
    with open(TEST_DATA_DIR / "example_report__check_ping_23d58148k840.html", "w") as f:
        f.write(page_source)


def get_example_report__check_ping():
    return CheckHostReport(
        report_id="23d58148k840",
        permalink="https://check-host.net/check-report/23d58148k840",
        report_type="check-ping",
        target="one.one.one.one",
        date="2025-03-08T21:28:20",
        results=[
            CheckPingReportResult(
                country_code="BR",
                location="Brazil, Sao Paulo",
                result="4 / 4",
                rtt="1.4 / 1.8 / 2.4 ms",
                ip="1.1.1.1"
            ),
            # TODO: add middle results, if we want more tests.
            CheckPingReportResult(
                country_code="VN",
                location="Vietnam, Ho Chi Minh City",
                result="4 / 4",
                rtt="46.9 / 46.9 / 46.9 ms",
                ip="1.1.1.1"
            )
        ]
    )


def dump_example_report_html__check_tcp():
    # Get "TCP" report page and save it to a file
    url = "https://check-host.net/check-report/23d581e0k7a?lang=en"
    page_source = _get_source(url)
    with open(TEST_DATA_DIR / "example_report__check_tcp_23d581e0k7a.html", "w") as f:
        f.write(page_source)


def get_example_report__check_tcp():
    return CheckHostReport(
        report_id="23d581e0k7a",
        permalink="https://check-host.net/check-report/23d581e0k7a",
        report_type="check-tcp",
        target="4.2.2.2:53",
        date="2025-03-08T21:28:52",
        results=[
            CheckTcpReportResult(
                country_code="BR",
                location="Brazil, Sao Paulo",
                result="Connected",
                time="0.110 s",
                ip="4.2.2.2",
            ),
            # TODO: add middle results, if we want more tests.
            CheckTcpReportResult(
                country_code="VN",
                location="Vietnam, Ho Chi Minh City",
                result="Connected",
                time="0.030 s",
                ip="4.2.2.2",
            )
        ]
    )


def dump_example_report_html__check_udp():
    # Get "UDP" report page and save it to a file
    url = "https://check-host.net/check-report/23e215c0k319?lang=en"
    page_source = _get_source(url)
    with open(TEST_DATA_DIR / "example_report__check_udp_23e215c0k319.html", "w") as f:
        f.write(page_source)


def get_example_report__check_udp():
    return CheckHostReport(
        report_id="23e215c0k319",
        permalink="https://check-host.net/check-report/23e215c0k319",
        report_type="check-udp",
        target="8.8.8.8:53",
        date="2025-03-10T13:03:45",
        results=[
            CheckUdpReportResult(
                country_code="BR",
                location="Brazil, Sao Paulo",
                result="Open or filtered",
                ip="8.8.8.8",
            ),
            # TODO: add middle results, if we want more tests.
            CheckUdpReportResult(
                country_code="VN",
                location="Vietnam, Ho Chi Minh City",
                result="Open or filtered",
                ip="8.8.8.8",
            )
        ]
    )


def dump_example_report_html__check_dns():
    # Get "DNS" report page and save it to a file
    url = "https://check-host.net/check-report/23e21752kd44?lang=en"
    page_source = _get_source(url)
    with open(TEST_DATA_DIR / "example_report__check_dns_23e21752kd44.html", "w") as f:
        f.write(page_source)


def get_example_report__check_dns():
    return CheckHostReport(
        report_id="23e21752kd44",
        permalink="https://check-host.net/check-report/23e21752kd44",
        report_type="check-dns",
        target="www.google.com",
        date="2025-03-10T13:04:50",
        results=[
            CheckDnsReportResult(
                country_code="BR",
                location="Brazil, Sao Paulo",
                result={"2800:3f0:4004:805::2004", "142.251.135.100"},
                ttl="1m 13s"
            ),
            # TODO: add middle results, if we want more tests.
            CheckDnsReportResult(
                country_code="VN",
                location="Vietnam, Ho Chi Minh City",
                result={"2404:6800:4005:819::2004", "142.250.76.228"},
                ttl="5m 0s"
            )
        ]
    )


def main():
    dump_example_report_html__check_http()
    dump_example_report_html__check_ping()
    dump_example_report_html__check_tcp()
    dump_example_report_html__check_udp()
    dump_example_report_html__check_dns()


if __name__ == "__main__":
    main()
