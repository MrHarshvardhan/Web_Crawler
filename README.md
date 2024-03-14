# Web Crawler

Web Crawler is a Python script designed to fetch URLs and check given domain names.

## Description

The Web Crawler is a Python-based application designed to crawl web pages and retrieve URLs similar to web.archive.org. It provides functionalities to fetch URLs from specified hosts or a list of domains and to check the status of given domain names.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MrHarshvardhan/Web_Crawler

```
### Arguments

- `function`: Specify the function to execute (`pull` or `check`).
- `--host HOST`: Domain/Host Name.
- `--threads THREADS`: The number of threads (default: 5).
- `--with-subs WITH_SUBS`: Specify `yes` or `no` (default: `yes`).
- `--loadfile LOADFILE`: File location.
- `-o OUTPUTFILE`, `--outputfile OUTPUTFILE`: Output file to save results.

## Examples

### Pull Function

To fetch URLs from a specific host:

```bash
python web_crawler.py pull --host example.com
```

To fetch URLs from a list of domains:

```bash
python web_crawler.py pull --loadfile domains.txt
```

To check the status of given domain names:
```bash
python web_crawler.py check --loadfile domains.txt
```
#### Additional Options
To specify the number of threads:

```bash
python web_crawler.py pull --host example.com --threads 10

```
To save the results to an output file:
```bash
python  web_crawler.py pull --host example.com --outputfile results.txt

```
