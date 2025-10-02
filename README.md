# rtve-subdl — RTVE Subtitle Downloader
**Author:** Hzifa33

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

---

## Overview

`rtve-subdl` is a lightweight command-line tool to download subtitle files from RTVE video pages and save them with human-friendly, "smart" filenames. The tool:

- Extracts a video ID from an RTVE page,
- Calls RTVE's subtitles API to list available subtitle tracks,
- Lets the user choose language(s) interactively (or downloads directly when only one language is available),
- Names subtitle files using a clean slug and optional `SxxExx` episode notation,
- Shows a progress bar and handles file overwrite prompts.

This repository contains the implementation (single-file script), installation instructions, usage examples, and recommendations for production hardening.

---

## Table of contents

- [Quick start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Filename conventions](#filename-conventions)
- [Examples](#examples)
- [Design notes & analysis](#design-notes--analysis)
- [Limitations & recommendations](#limitations--recommendations)
- [Development & contribution](#development--contribution)
- [Security & legal](#security--legal)
- [License](#license)
- [Credits](#credits)

---

## Quick start

```bash
# create a venv (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows (PowerShell)

# install dependencies
pip install -r requirements.txt

# run (interactive)
python rtve_subdl.py "https://www.rtve.es/your-video-page-url"


---

Installation

1. Clone the repository:

git clone https://github.com/Hzifa33/rtve-subdl.git
cd rtve-subdl


2. Install dependencies:

pip install -r requirements.txt


3. Run the script:

python rtve_subdl.py

You can either pass the RTVE video page URL as the first argument or input it when prompted.




---

Usage

Basic invocation:

python rtve_subdl.py "https://www.rtve.es/your-video-page-url"

If no argument is provided, the script prompts for the URL:

Please enter the RTVE video page URL:
> https://www.rtve.es/...

When multiple subtitle languages are found, an interactive prompt allows selecting:

all to download every listed subtitle

a comma-separated list of numbers (e.g., 1,3) to choose specific tracks


If a subtitle file already exists, the script prompts to (O)verwrite or (S)kip.


---

Filename conventions

The script attempts to create a readable base filename from the page title:

It extracts title from og:title or <h1>.

Removes season/episode fragments (e.g., Temporada 1 Capítulo 2) and, if found, appends S01E02.

Slug format: lowercase, non-alphanumeric characters removed, spaces replaced with underscores.

Final filename pattern: <slug>[_SxxExx]_<lang><ext>
Example: the_show_something_S01E02_en.srt



---

Examples

Single subtitle available (automatic download):

-> Found 1 subtitle: EN. Starting download directly.

Output: title_S01E02_en.srt

Multiple subtitles found (interactive):

1. Español (Spanish)
2. English
3. Català (Catalan)
Enter the number(s) separated by commas (e.g., 1,3), or 'all' to download all:
> 2

Output: title_S01E02_en.srt



---

Design notes & analysis

Key functions & responsibilities

find_video_id(page_url): fetches page HTML and extracts a numeric id using a regex ("id":\s*(\d{5,})).

get_video_details(page_content): extracts the title and tries to detect season/episode, builds a slug and base filename.

get_subtitle_info_from_api(video_id): queries https://www.rtve.es/api/videos/{video_id}/subtitulos and builds a list of {lang, src} items.

handle_user_selection(...): displays options and parses user input (supports all and comma-separated selections).

download_file(url, filename): streams the subtitle and shows a tqdm progress bar; prompts for overwrite if file exists.

show_credits(): prints a small animated credit box with Hzifa33.


Observations

The script is synchronous and single-threaded.

The script uses BeautifulSoup with html.parser (no external parser required).

There is basic error handling around networking and JSON parsing.



---

Limitations & recommendations (actionable)

1. Robust ID extraction

Current regex looks for "id": <5+ digits>. Consider parsing JSON objects embedded in the page or searching for canonical metadata to avoid fragile regex matches.

Use a more permissive pattern or parse JavaScript-injected JSON safely.



2. User interface improvements

Replace input() prompts with argparse flags for non-interactive automation:

--url, --lang, --all, --output-dir, --overwrite, --no-progress.


Provide --yes to auto-overwrite.



3. HTTP resilience

Use a requests.Session() and requests.adapters.HTTPAdapter with retries and backoff.

Add timeout and clear error messages for common HTTP status codes (401, 403, 404, 429).



4. Testing & CI

Add unit tests for slug generation, filename formatting, and API parsing.

Add GitHub Actions for linting (flake8/ruff), type checking (mypy), and running tests.



5. Packaging & distribution

If desired, refactor to a package with console entry point (setup.cfg/pyproject.toml) so users can pip install . and run rtve-subdl.



6. Safety & legal

Add a clear Security & Legal section in README. Verify RTVE terms of service before automated downloads.

Consider rate-limiting requests to the API.



7. Internationalization

The LANG map is useful but limited. Consider mapping names for any encountered language code using a lookup library (pycountry) to show human-readable names.



8. File extension handling

The script obtains the extension from the first subtitle URL. If multiple subtitle URLs have different extensions, consider deriving extension per-file.





---

Development & contribution

Contributions are welcome. Suggested workflow:

1. Fork the repo.


2. Create a feature branch: git checkout -b feat/argparse-cli.


3. Open a pull request with tests and a short changelog entry.



Suggested CI:

python -m pytest

ruff/flake8 and mypy (optional)



---

Security & legal

Important: This project interacts with RTVE web pages and their API. Before using or distributing this tool, confirm that automated access is permitted by RTVE's Terms of Service and any applicable local laws. Do not use this tool for unauthorized mass scraping or to circumvent access controls.


---

License

This repository suggests the MIT license (see LICENSE). Update as needed for your project.


---

Credits

Developer: Hzifa33

Built with: requests, BeautifulSoup4, tqdm, colorama



---

Changelog (summary)

v6.0 — Current single-file script: ID extraction, API lookup, interactive language selection, smart filename generation, download with progress bar.





---

2) requirements.txt

requests>=2.28
tqdm>=4.64
colorama>=0.4.6
beautifulsoup4>=4.12

> Notes:

These are conservative minimum versions that cover modern improvements (choose exact pins if you need reproducible builds).

re, os, sys, urllib.parse, time are standard library modules and do not appear here.





---

3) Long repository Description (detailed paragraph — use in project page or long description field)

rtve-subdl is a focused command-line utility for retrieving subtitle tracks from RTVE video pages and saving them with readable, machine-friendly filenames. The tool automatically extracts a numeric video identifier from a provided RTVE page, queries RTVE’s public subtitle API, and either downloads a single available subtitle or presents an interactive language-selection prompt for multiple tracks. Filenames are normalized into a slug form and, when season/episode metadata is detected, include an `SxxEyy` marker for easy archival and media-player compatibility. The script is intentionally minimal and dependency-light, designed for end-users and developers who need a reliable, scriptable subtitle extraction workflow. Users should confirm compliance with RTVE’s usage terms before automating downloads.


---

4) Short repository blurb / the short "About" text to put under the repository name on GitHub

One-line tagline (<= 140 chars):

Smart CLI tool to download and auto-name subtitles from RTVE video pages — interactive language selection and episode-aware filenames.

About (2–3 lines you can paste into the repository "About" box):

RTVE subtitle downloader with smart filename generation and interactive language selection. Extracts RTVE video IDs, queries the subtitles API, and saves subtitles as readable slugs with optional SxxEyy notation. Maintained by Hzifa33.

Suggested repository topics / tags

python, subtitles, rtve, scraper, cli, downloader, media-tools


---

Final notes & suggested next steps (recommended actions you can take now)

Add these files to your repo root:

README.md (use the content above)

requirements.txt (use the content above)

Optionally LICENSE (MIT) and .gitignore (Python standard).


Consider refactoring to add argparse for non-interactive use and CI for tests.

If you want, I can:

produce a pyproject.toml and setup.cfg to package the script,

convert the script to a proper package with entry point rtve-subdl,

add GitHub Actions CI workflow yaml for lint/tests,

or write unit tests for the slug/filename logic

