# check-host-report-scraper
Scraper for permalinked check-reports made on `check-host.net`, e.g., https://check-host.net/check-report/23d4f6aekc8

`check-host.net` is a website that provides free services used for network diagnostics, such as checking the status of a website. There is an API for _creating_ reports, but not for _fetching_ existing reports. This package facilitates the latter.

## Usage

Install: `pip install -e .`

### Standalone 

```bash
python cli.py 23d4f6aekc8
```

```json
{
    "report_id": "23d4f6aekc8",
    "permalink": "https://check-host.net/check-report/23d4f6aekc8",
    "report_type": "check-http",
    "target": "http://google.com:80",
    "date": "2025-03-08T19:45:31",
    "results": null
}
```

### As a module

```python
from checkhost_scraper.scraper import CheckHostReportScraper

scraper = CheckHostReportScraper()
report = scraper.scrape("23d63999k1c2")

# report
CheckHostReport(
    report_id='23d63999k1c2',
    permalink='https://check-host.net/check-report/23d63999k1c2',
    report_type='check-http',
    target='http://google.com:80',
    date='2025-03-08T19:45:31',
    results=None, # TODO.
)
```

## Data structure

### Report meta-data

Available across all report types:
 * The `report_type` of report. One of `http-check`, `dns-check`, `ping-check`, `tcp-check`, `udp-check`.
 * The `target` of the report, Example: `https://example.com:443`
 * The `date` the report was made. Example: `2021-01-01T00:00:00`

### `results` structures
TODO: the results structure depends on the report type, and result extractors need to be written for each report type. The table data is populated by JavaScript (which exists in a `<script>` tag), though it may be easier to just render (e.g. with Selenium). 

The structure for `http-check` may look something like:

#### `http-check`

```json
[
        {
            "location": "Brazil, Sao Paulo",
            "result": "OK",
            "time": "0.076 s",
            "code": "301 (Moved Permanently)",
            "ip": "142.251.129.78"
        },
        {
            "location": "Bulgaria, Sofia",
            "result": "OK",
            "time": "0.293 s",
            "code": "301 (Moved Permanently)",
            "ip": "142.250.187.110"
        },
        ...
    ]
}
```

### Testing and development

1) Pull known test data from the site: `python tests/generate_test_data.py`
2) Run tests: `pytest`

If you believe the site has changed, then re-run the test data generation script.

### Disclaimer

_I am not responsible for the use of this scraper. While all requested data is public, I recommend (a) being respectful of the site's resources and (b) using the data ethically. Here and in general._
