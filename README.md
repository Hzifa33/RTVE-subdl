# rtve-subdl
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful and user-friendly Python script to download subtitles from [RTVE.es](https://www.rtve.es/play/) videos with intelligent, series-friendly file naming.



## ✨ Features

* **Smart File Naming**: Automatically detects series, season, and episode numbers from the video title to name files in a clean `series_name_s01e02_es.vtt` format.
* **Multiple Language Support**: If a video offers subtitles in multiple languages (e.g., Spanish, English, Catalan), it prompts you to choose which ones to download.
* **Interactive & Direct Mode**: Run the script and paste a URL, or provide the URL as a command-line argument for faster workflow.
* **Elegant Progress Bar**: A clean progress bar shows download status, powered by `tqdm`.
* **User-Friendly Interface**: Colorful and informative console output guides you through the process.
* **Safe Overwrite**: Checks if a file already exists and asks for confirmation before overwriting.

---

## 🚀 Installation

To use this script, you'll need Python 3.7 or newer.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Hzifa33/rtve-subdl.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd rtve-subdl
    ```

3.  **Install the required dependencies:**
    *(It is highly recommended to do this within a [Python virtual environment](https://docs.python.org/3/library/venv.html).)*
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 Usage

You can run the script in two ways:

### Interactive Mode

Simply run the script without any arguments. It will prompt you to enter the RTVE video URL.

```bash
python rtve-subdl.py
```
**Example:**
```
Please enter the RTVE video page URL:
> https://www.rtve.es/play/videos/el-ministerio-del-tiempo/ministerio-del-tiempo-1-capitulo-1-tiempo/3013349/
```

### Direct Mode

Pass the video URL directly as a command-line argument. **Make sure to enclose the URL in quotes.**

```bash
python rtve-subdl.py "https://www.rtve.es/play/videos/some-video-url/"
```

The script will then handle the rest, and the downloaded subtitle files will be saved in the same directory.

---

## 🛠️ How It Works

The script automates the following process:

1.  **Fetch Video ID**: It first scrapes the video page URL to find the unique internal `Video ID`.
2.  **Extract Details**: It then parses the page's HTML to extract the title and look for season/episode patterns for smart naming.
3.  **Query API**: It uses the official RTVE API (`https://www.rtve.es/api/videos/{video_id}/subtitulos`) to get a list of all available subtitle languages and their direct download links.
4.  **User Selection**: If multiple languages are available, it presents a clear menu for the user to select the desired files.
5.  **Download**: Finally, it downloads the selected subtitle(s) using a streaming request to handle large files efficiently, displaying a progress bar during the process.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
Developed by **Hzifa33**.
