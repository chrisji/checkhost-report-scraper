# checkhost-report-scraper

![Coverage](tests/assets/coverage-badge.svg)

Scraper for permalinked check-reports made on `check-host.net`, e.g., https://check-host.net/check-report/23d4f6aekc8

`check-host.net` is a website that provides free services used for network diagnostics, such as checking the status of a website. There is an API for _creating_ reports, but not for _fetching_ existing reports. This package facilitates the latter.

## Usage

### Standalone 

```bash
python cli.py --report_id 23d4f6aekc8
```

```json
{
    "report_id": "23d4f6aekc8",
    "permalink": "https://check-host.net/check-report/23d4f6aekc8",
    "report_type": "check-http",
    "target": "http://google.com:80",
    "date": "2025-03-08T19:45:31",
    "results": [
        {
            "country_code": "BR",
            "location": "Brazil, Sao Paulo",
            "result": "OK",
            "time": "0.076 s",
            "code": "301 (Moved Permanently)",
            "ip": "1.1.1.1",
        }
    ]
}
```

### As a package

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
    results=[
        CheckHostResult(
            country_code='BR',
            location='Brazil, Sao Paulo',
            result='OK',
            time='0.076 s',
            code='301 (Moved Permanently)',
            ip='1.1.1.1'
        ),
        ...
        CheckHostResult(
            country_code='BG',
            location='Bulgaria, Sofia',
            result='OK',
            time='0.293 s',
            code='301 (Moved Permanently)',
            ip='1.1.1.1'
        )
    ]
)
```

## Install

Add to `requirements.txt`

```txt
checkhost_scraper @ git+https://github.com/chrisji/checkhost-report-scraper.git@v1.0.0
```

or clone and install

```bash
git clone https://github.com/chrisji/checkhost-report-scraper.git
cd checkhost-report-scraper
pip install -e .
```

## Data structure

Report metadata is available and consistent for all report types:
 * The `report_type`. One of `http-check`, `dns-check`, `ping-check`, `tcp-check`, `udp-check`.
 * The `target` of the report, Example: `https://example.com:443`
 * The `date` the report was made (iso format). Example: `2021-01-01T00:00:00`

The `results` structure changes depending on the report type, and parsing currently covers:

 - [x] `http-check`
 - [x] `dns-check`
 - [x] `ping-check`
 - [x] `tcp-check`
 - [x] `udp-check`

See `checkhost_scraper/models.py` for details on the results structure for each type.

#### Example `http-check` jsonified `result`.

```json
[
    {
        "country_code": "BR",
        "location": "Brazil, Sao Paulo",
        "result": "OK",
        "time": "0.076 s",
        "code": "301 (Moved Permanently)",
        "ip": "142.251.129.78"
    },
    {
        "country_code": "BG",
        "location": "Bulgaria, Sofia",
        "result": "OK",
        "time": "0.293 s",
        "code": "301 (Moved Permanently)",
        "ip": "142.250.187.110"
    }
]

```

### Testing and development

1) Pull known test data from the site: `python tests/generate_test_data.py`
2) Run tests with coverage: `pytest --cov=checkhost_scraper`

Run tests / checks and update coverage badge: `sh run-checks.sh`

### Disclaimer

I am not responsible for the use of this scraper. While all requested data is public, I recommend (a) being respectful of the site's resources and (b) using the data ethically.
