from pydantic import BaseModel
from typing import List, Union, Optional


class CheckHttpReportResult(BaseModel):
    """
    Single result (row) of a "check-http" report

    Example structure:
    {
        "country_code": "BR",
        "location": "Brazil, Sao Paulo",
        "result": "OK",
        "time": "0.076 s",
        "code": "301 (Moved Permanently)",
        "ip": "1.1.1.1"
    }
    """
    country_code: str
    location: str
    result: str
    time: str
    code: str
    ip: str


class CheckDnsReportResult(BaseModel):
    """
    Single result (row) of a "check-dns" report
    
    Not implemented yet
    """
    ...


class CheckPingReportResult(BaseModel):
    """
    Single result (row) of a "check-ping" report
    
    Not implemented yet
    """
    ...


class CheckTcpReportResult(BaseModel):
    """
    Single result (row) of a "check-tcp" report
    
    Not implemented yet
    """
    ...


class CheckUdpReportResult(BaseModel):
    """
    Single result (row) of a "check-udp" report
    
    Not implemented yet
    """
    ...


class CheckHostReport(BaseModel):
    """
    Represents a full report from check-host.net

    Example structure:
    {
        "report_id": "23d4f6aekc8",
        "permalink": "https://check-host.net/check-report/23d4f6aekc8",
        "report_type": "check-http",
        "target": "http://google.com:80",
        "date": "2025-03-08T19:45:31",
        "results": [
            ...
        ]
    }
    """
    report_id: str
    permalink: str
    report_type: str
    target: str
    date: str
    results: Optional[List[Union[
        CheckHttpReportResult, 
        CheckDnsReportResult, 
        CheckPingReportResult, 
        CheckTcpReportResult, 
        CheckUdpReportResult
    ]]] = None
