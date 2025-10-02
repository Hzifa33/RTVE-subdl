# rtve-subdl2

[![CI](https://img.shields.io/badge/ci-GitHub%20Actions-blue)](https://github.com/Hzifa33/rtve-subdl/actions)
[![PyPI](https://img.shields.io/badge/pypi-not%20published-lightgrey)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**rtve-subdl2** — Lightweight, professional Python CLI & library to discover and download subtitles (SRT/VTT) from RTVE with intelligent naming and batch support.

---

## Table of contents

- [Overview](#overview)  
- [Key features](#key-features)  
- [Quickstart (CLI)](#quickstart-cli)  
- [Programmatic usage (optional)](#programmatic-usage-optional)  
- [Installation](#installation)  
- [Examples](#examples)  
- [Configuration & options](#configuration--options)  
- [Project layout](#project-layout)  
- [Development & tests](#development--tests)  
- [Security & legal notice](#security--legal-notice)  
- [Contributing](#contributing)  
- [License](#license)

---

## Overview

`rtve-subdl` is a focused command-line utility and Python helper library designed to locate subtitle resources for RTVE videos and download them with a predictable, sanitized filename template. It is built for reliability, automation and integration into media processing pipelines.

It intentionally keeps a small dependency surface and provides both interactive and non-interactive modes for scripting and CI usage.

---

## Key features

- Resolve RTVE video page → extract video ID and metadata (title / season / episode when available).  
- Query RTVE subtitle API endpoints and discover available subtitle files.  
- Download single or multiple languages (SRT / VTT) with an intelligent file-naming scheme: `slug_S01E02_es.srt`.  
- Interactive language selection or non-interactive `--langs` / `--all` flags for automation.  
- Robust network handling with `requests.Session()` and a progress bar (via `tqdm`).  
- Clean CLI UX (colorized output via `colorama`) and safe filename sanitization.  
- Minimal, easy-to-pin runtime dependencies.

---

## Quickstart (CLI)

### From GitHub (recommended during development)
```bash
pip install git+https://github.com/Hzifa33/rtve-subdl.git
