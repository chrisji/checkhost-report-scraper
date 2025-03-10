from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from typing import List, Union, Optional

from .models import (
    CheckHostReport,
    CheckHttpReportResult,
    CheckDnsReportResult,
    CheckPingReportResult,
    CheckTcpReportResult,
    CheckUdpReportResult,
    InvalidReport,
    ReportNotFoundException
)


CHECK_HOST_URL = "https://check-host.net/check-report/{report_id}?lang=en" # Use lang=en to ensure English version
DATETIME_FORMAT = "%a %b %d %H:%M:%S UTC %Y" # Example: "Sat Mar 08 20:28:15 UTC 2025"
REPORT_TYPE = Union[CheckHttpReportResult, CheckDnsReportResult, CheckPingReportResult, CheckTcpReportResult, CheckUdpReportResult]
EXPECTED_HTTP_REPORT_HEADERS = ["Location", "Result", "Time", "Code", "IP address"]
EXPECTED_PING_REPORT_HEADERS = ["Location", "Result", "rtt min / avg / max", "IP address"]
EXPECTED_TCP_REPORT_HEADERS = ["Location", "Result", "Time", "IP address"]
EXPECTED_UDP_REPORT_HEADERS = ["Location", "Result", "IP address"]
EXPECTED_DNS_REPORT_HEADERS = ["Location", "Result", "TTL"]


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

        # Set-up selenium driver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)


    def _get_source(self, url: str) -> str:
        """
        Fetches the HTML source of a webpage and returns it as a string.
        """
        self.driver.get(url)
        response_text = self.driver.page_source
        return response_text


    def scrape(self, report_id: str) -> Union[CheckHostReport, InvalidReport]:
        """
        Fetches the report from check-host.net and returns a CheckHostReport object.
        
        :param report_id: The ID of the report to scrape
        :return: CheckHostReport object
        """
        url = CHECK_HOST_URL.format(report_id=report_id)
        return self._parse_report(self._get_source(url))
        

    def _parse_report(self, report_html: str) -> Union[CheckHostReport, InvalidReport]:
        """
        Parses the HTML of a check-host.net report and returns
        a CheckHostReport object.
        
        :param report_html: The full HTML of the report page
        :return: CheckHostReport object
        """
        soup = BeautifulSoup(report_html, "html.parser")
        report_id = self._parse_report_id(soup)

        try:        
            self._check_valid(soup)
        except ReportNotFoundException as e:
            return InvalidReport(
                report_id=report_id,
                reason=e.message,
            )
        
        report_type = self._parse_type(soup)
        return CheckHostReport(
            report_id=report_id,
            permalink=self._parse_report_permalink(soup),
            report_type=report_type,
            target=self._parse_target(soup),
            date=self._parse_checked_on_datetime(soup),
            results=self._parse_results(soup, report_type),
        )


    def _check_valid(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Example html element to parse:

        <h1>Check report was removed</h1>
        """
        h1_text = soup.find("h1").text.strip()
        if h1_text == "Check report was removed":
            raise ReportNotFoundException
        return None


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

        <link rel="canonical" href="https://check-host.net/check-report/23d52df5k770">
        """
        link = soup.find("link", attrs={"rel": "canonical"})
        return link["href"].split("check-report/")[-1]
    

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
        :param soup: BeautifulSoup object of the report page. Note that JavaScript
         is used to populate the tabled data, so we need to make sure the page source
         has first been rendered (e.g., with Selenium) before parsing the results.

        Example table element structure:
        <tbody>
            <tr>
                <td class="location whitespace-nowrap">
                    <div class="z-1 node_info  tooltip ">
                    <div class="overflow-hidden text-ellipsis">
                        <img class="flag inline" src="/images/flags/cz.png" alt="cz">
                        <span class="popover_action cursor-pointer border-dashed border-b border-gray-600" onclick="open_popover(event, 'popover_id_cz1.node.check-host.net', 'top')">Czechia, C.Budejovice</span>
                    </div>
                    ...
                <td class="result" id="result_cz1.node.check-host.net"><div>OK</div></td>
                <td class="time" id="result_time_cz1.node.check-host.net"><div>0.024 s</div></td>
                <td class="code" id="result_code_cz1.node.check-host.net"><div>301 (Moved Permanently)</div></td>
                <td class="ip" id="result_ip_cz1.node.check-host.net"><div>1.1.1.1</div></td>
                ...
        """
        table = soup.find("table") 
        headers = [th.text for th in table.find('thead').find('tr').find_all('th')]
        rows = table.find("tbody").find_all("tr", recursive=False)

        # Check if table headers are as expected
        assert headers == EXPECTED_HTTP_REPORT_HEADERS

        results = []
        for row in rows:
            loc_td = row.find("td", class_="location")
            results.append(
                CheckHttpReportResult(
                    country_code=loc_td.find("img")['alt'].upper(),
                    location=loc_td.find("span").text,
                    result=row.find("td", class_="result").text,
                    time=row.find("td", class_="time").text,
                    code=row.find("td", class_="code").text,
                    ip=row.find("td", class_="ip").text
                )
            )
        return results
    

    def _parse_check_dns_results(self, soup: str) -> list[CheckDnsReportResult]:
        """
        :param soup: BeautifulSoup object of the report page. Note that JavaScript
         is used to populate the tabled data, so we need to make sure the page source
         has first been rendered (e.g., with Selenium) before parsing the results.
        """
        table = soup.find("table")
        headers = [th.text for th in table.find('thead').find('tr').find_all('th')]
        rows = table.find("tbody").find_all("tr", recursive=False)

        # Check if table headers are as expected
        assert headers == EXPECTED_DNS_REPORT_HEADERS

        results = []
        for row in rows:
            loc_td = row.find("td", class_="location")
            # Convert CSV "results" to a set
            result_csv_str = row.find("td", class_="result").text
            result_set = set([x.strip() for x in result_csv_str.split(",")])

            results.append(
                CheckDnsReportResult(
                    country_code=loc_td.find("img")['alt'].upper(),
                    location=loc_td.find("span").text,
                    result=result_set,
                    ttl=row.find("td", class_="ttl").text
                )
            )
        return results


    def _parse_check_ping_results(self, soup: str) -> list[CheckPingReportResult]:
        """
        :param soup: BeautifulSoup object of the report page. Note that JavaScript
         is used to populate the tabled data, so we need to make sure the page source
         has first been rendered (e.g., with Selenium) before parsing the results.
        """
        table = soup.find("table")
        headers = [th.text for th in table.find('thead').find('tr').find_all('th')]
        rows = table.find("tbody").find_all("tr", recursive=False)

        # Check if table headers are as expected
        assert headers == EXPECTED_PING_REPORT_HEADERS

        results = []
        for row in rows:
            loc_td = row.find("td", class_="location")

            # The "ip" <td> is identified with an id starting with "result_ip_"
            ip_td = [t for t in row.find_all("td") if t.get("id", "").startswith("result_ip_")][0]

            results.append(
                CheckPingReportResult(
                    country_code=loc_td.find("img")['alt'].upper(),
                    location=loc_td.find("span").text,
                    result=row.find("td", class_="result").text,
                    rtt=row.find("td", class_="rtt").text,
                    ip=ip_td.text
                )
            )
        return results


    def _parse_check_tcp_results(self, soup: str) -> list[CheckTcpReportResult]:
        """
        :param soup: BeautifulSoup object of the report page. Note that JavaScript
         is used to populate the tabled data, so we need to make sure the page source
         has first been rendered (e.g., with Selenium) before parsing the results.
        """
        table = soup.find("table")
        headers = [th.text for th in table.find('thead').find('tr').find_all('th')]
        rows = table.find("tbody").find_all("tr", recursive=False)

        # Check if table headers are as expected
        assert headers == EXPECTED_TCP_REPORT_HEADERS

        results = []
        for row in rows:
            loc_td = row.find("td", class_="location")

            # The "time" <td> is identified with an id starting with "result_time_"
            time_td = [t for t in row.find_all("td") if t.get("id", "").startswith("result_time_")][0]

            results.append(
                CheckTcpReportResult(
                    country_code=loc_td.find("img")['alt'].upper(),
                    location=loc_td.find("span").text,
                    result=row.find("td", class_="result").text,
                    time=time_td.text,
                    ip=row.find("td", class_="ip").text
                )
            )
        return results


    def _parse_check_udp_results(self, soup: str) -> list[CheckUdpReportResult]:
        """
        :param soup: BeautifulSoup object of the report page. Note that JavaScript
         is used to populate the tabled data, so we need to make sure the page source
         has first been rendered (e.g., with Selenium) before parsing the results.
        """
        table = soup.find("table")
        headers = [th.text for th in table.find('thead').find('tr').find_all('th')]
        rows = table.find("tbody").find_all("tr", recursive=False)

        # Check if table headers are as expected
        assert headers == EXPECTED_UDP_REPORT_HEADERS
        
        results = []
        for row in rows:
            loc_td = row.find("td", class_="location")
            results.append(
                CheckUdpReportResult(
                    country_code=loc_td.find("img")['alt'].upper(),
                    location=loc_td.find("span").text,
                    result=row.find("td", class_="result").text,
                    ip=row.find("td", class_="ip").text
                )
            )
        return results
