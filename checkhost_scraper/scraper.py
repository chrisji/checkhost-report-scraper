import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Union

from .models import (
    CheckHostReport,
    CheckHttpReportResult,
    CheckDnsReportResult,
    CheckPingReportResult,
    CheckTcpReportResult,
    CheckUdpReportResult
)


CHECK_HOST_URL = "https://check-host.net/check-report/{report_id}?lang=en" # Use lang=en to ensure English version
DATETIME_FORMAT = "%a %b %d %H:%M:%S UTC %Y" # Example: "Sat Mar 08 20:28:15 UTC 2025"
REPORT_TYPE = Union[CheckHttpReportResult, CheckDnsReportResult, CheckPingReportResult, CheckTcpReportResult, CheckUdpReportResult]


class CheckHostReportScraper:
    """
    Scrapes check-host.net for a report and returns a CheckHostReport object.

    TODO: add proxy support

    Example usage:
    >>> scraper = CheckHostReportScraper()
    >>> report = scraper.scrape("23d52df5k770")
    >>> print(report.model_dump_json())
    """
    def __init__(self):
        # Maps report type to string found in the h1 tag
        self.check_report_map = {
            "Check website": "check-http",
            "DNS": "check-dns",
            "Ping server": "check-ping",
            "TCP connect": "check-tcp",
            "UDP connect": "check-udp"
        }

        # Maps report type to function that parses the results
        self.check_report_funcs = {
            "check-http": self._parse_check_http_results,
            "check-dns": self._parse_check_dns_results,
            "check-ping": self._parse_check_ping_results,
            "check-tcp": self._parse_check_tcp_results,
            "check-udp": self._parse_check_udp_results,
        }


    def scrape(self, report_id: str) -> CheckHostReport:
        """
        Fetches the report from check-host.net and returns a CheckHostReport object.
        
        :param report_id: The ID of the report to scrape
        :return: CheckHostReport object
        """
        url = CHECK_HOST_URL.format(report_id=report_id)
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch report: {response.status_code}")
        return self._parse_report(response.text)
        

    def _parse_report(self, report_html: str) -> CheckHostReport:
        """
        Parses the HTML of a check-host.net report and returns
        a CheckHostReport object.
        
        :param report_html: The full HTML of the report page
        :return: CheckHostReport object
        """
        soup = BeautifulSoup(report_html, "html.parser")
        
        report_id = self._parse_report_id(soup)
        permalink = self._parse_report_permalink(soup)
        _type = self._parse_type(soup)
        target = self._parse_target(soup)
        date = self._parse_checked_on_datetime(soup)
        results = self._parse_results(soup, _type)

        return CheckHostReport(
            report_id=report_id,
            permalink=permalink,
            report_type=_type,
            target=target,
            date=date,
            results=results,
        )


    def _parse_results(self, soup: BeautifulSoup, report_type: str) -> List[REPORT_TYPE]:
        """
        Parses the results of a check-host.net report and returns
        a list of result objects.

        :param soup: BeautifulSoup object of the report page
        :param report_type: The type of report to parse
        :return: List of result objects
        """
        if report_type not in self.check_report_funcs:
            raise ValueError(f"Unknown report type: {report_type}")
        return self.check_report_funcs[report_type](soup)
        

    def _parse_type(self, soup: BeautifulSoup) -> str:
        """
        Example html element to parse:

        <div class="text-center basis-11/12">
          <h1>Check website <div class="inline-block">
            <span class="break-all bg-neutral-200 px-1">https://1.1.1.1</span></div>
          </h1>
        </div>
        """
        h1 = soup.find("h1")
        div_inline_block = h1.find("div", class_="inline-block")
        extracted_type = h1.text.split(div_inline_block.text)[0].strip()
        if extracted_type in self.check_report_map:
            return self.check_report_map[extracted_type]
        else:
            raise ValueError(f"Unknown report type: {extracted_type}")
    

    def _parse_report_id(self, soup: BeautifulSoup) -> str:
        """
        Example html element to parse:

        <div id="report_permalink" class="mb-0.5 flex justify-between">
            <div>
                <a href="https://check-host.net/check-report/23d52df5k770">
                Permanent link to this check report</a> |
            ...
        """
        div = soup.find("div", id="report_permalink")
        a = div.find("a")
        return a["href"].split("check-report/")[-1]
    

    def _parse_report_permalink(self, soup: BeautifulSoup) -> str:
        """
        Example html element to parse:

        <div id="report_permalink" class="mb-0.5 flex justify-between">
            <div>
                <a href="https://check-host.net/check-report/23d52df5k770">
                Permanent link to this check report</a> | <span>Share on</span>
            ...
        """
        div = soup.find("div", id="report_permalink")
        a = div.find("a")
        return a["href"]


    def _parse_target(self, soup: BeautifulSoup) -> str:
        """
        Example html element to parse:

        <div class="text-center basis-11/12">
          <h1>Check website <div class="inline-block">
          <span class="break-all bg-neutral-200 px-1">https://1.1.1.1</span></div></h1>
        </div>
        """
        target_span = soup.find("h1").find("span")
        return target_span.text.strip()


    def _parse_checked_on_datetime(self, soup: BeautifulSoup) -> str:
        """
        Example html element to parse:

        <div>Checked on <strong>Sat Mar 08 20:28:15 UTC 2025</strong> |
            <a href="/check-http?host=https://1.1.1.1">
                Check again
            </a>
        </div>
        """
        for d in soup.find_all("div"):
            if d.text.strip().startswith("Checked on"):
                checked_str = d.find("strong").text
                return datetime.strptime(checked_str, DATETIME_FORMAT).isoformat()
        return None
    

    def _parse_check_http_results(self, soup: str) -> list[CheckHttpReportResult]:
        """
        TODO:

        NOTE: JavaScript used to populate the table, so we need to
        use Selenium or similar to render the page and get the table data.
        """
        return None
    

    def _parse_check_dns_results(self, soup: str) -> list[CheckDnsReportResult]:
        """
        TODO
        """
        return None


    def _parse_check_ping_results(self, soup: str) -> list[CheckPingReportResult]:
        """
        TODO
        """
        return None


    def _parse_check_tcp_results(self, soup: str) -> list[CheckTcpReportResult]:
        """
        TODO
        """
        return None


    def _parse_check_udp_results(self, soup: str) -> list[CheckUdpReportResult]:
        """
        TODO
        """
        return None
