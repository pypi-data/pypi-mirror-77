# Torrent Tracker Scraper

A UDP torrent tracker scraper written in Python 3

![Jenkins](https://jenkins.psr42.online/job/torrent-tracker-scraper/badge/icon?)
[![PyPI version](https://badge.fury.io/py/torrent-tracker-scraper.svg)](https://badge.fury.io/py/torrent-tracker-scraper)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

<img src="docs/imgs/car-thief.jpg" width="400">

## Installation

```bash
pipenv install torrent-tracker-scraper
pipenv shell
```

<img src="docs/imgs/thief-downloading-python-package.jpg" width="400">

## Usage

### Pass in a list of infohashes

```python
from torrent_tracker_scraper import scraper

scraper = scraper.Scraper(
    infohashes=[
        "82026E5C56F0AEACEDCE2D7BC2074A644BC50990",
        "04D9A2D3FAEA111356519A0E0775E5EAEE9C944A",
    ]
)
results = scraper.scrape()
print(results)

[
    ...,
    {
        'tracker': 'udp://explodie.org:6969',
        'results': [
            {
                'infohash': '82026E5C56F0AEACEDCE2D7BC2074A644BC50990',
                'seeders': 246,
                'completed': 0,
                'leechers': 36
            },
            {
                'infohash': '04D9A2D3FAEA111356519A0E0775E5EAEE9C944A',
                'seeders': 7,
                'completed': 0,
                'leechers': 27
            }
        ]
    },
    ...
```

Get your scrapped information

<img src="docs/imgs/thief-with-an-early.2000s-limp-bizkit-cd.jpg" width="400">

### Pass in a list of trackers

```python
from torrent_tracker_scraper import scraper

scraper = scraper.Scraper(
    trackers=["udp://explodie.org:6969/annouce"],
    infohashes=[
        "82026E5C56F0AEACEDCE2D7BC2074A644BC50990",
        "04D9A2D3FAEA111356519A0E0775E5EAEE9C944A",
    ],
)
results = scraper.scrape()
print(results)

[
    ...,
    {
        'tracker': 'udp://explodie.org:6969',
        'results': [
            {
                'infohash': '82026E5C56F0AEACEDCE2D7BC2074A644BC50990',
                'seeders': 246,
                'completed': 0,
                'leechers': 36
            },
            {
                'infohash': '04D9A2D3FAEA111356519A0E0775E5EAEE9C944A',
                'seeders': 7,
                'completed': 0,
                'leechers': 27
            }
        ]
    },
    ...
```

## Testing

```bash
pipenv install --dev
pipenv run pytest
```

<img src="docs/imgs/thief-reviewing-unit-test-reports.jpg" width="400">

## Help/Contributing

Use the normal GitHub bug reporting flow i.e Create an issue here
<https://github.com/project-mk-ultra/torrent-tracker-scraper/issues>.

Fork the code, make your changes and create a pull request.

<img src="docs/imgs/thief-tiptoe.jpg" width="400">

## Contributors

1. <https://github.com/dessalines>
