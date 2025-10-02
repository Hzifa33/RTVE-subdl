import requests
import os
import sys
import re
from urllib.parse import urlparse
from tqdm import tqdm
from colorama import Fore, Style, init
import time
from bs4 import BeautifulSoup 

init(autoreset=True)

C_TITLE = Fore.CYAN + Style.BRIGHT
C_INFO = Fore.YELLOW + Style.BRIGHT
C_SUCCESS = Fore.GREEN + Style.BRIGHT
C_ERROR = Fore.RED + Style.BRIGHT
C_PROMPT = Fore.MAGENTA
C_DATA = Fore.WHITE + Style.BRIGHT
C_RESET = Style.RESET_ALL


def find_video_id(page_url):
    print(f"{C_INFO}[1/4] Fetching video page to find Video ID and Title...")
    try:
        response = requests.get(page_url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        page_content = response.text
        match = re.search(r'"id":\s*(\d{5,})', page_content)
        if match:
            video_id = match.group(1)
            print(f"{C_SUCCESS}      -> Found Video ID: {C_DATA}{video_id}")
            
            return video_id, page_content
        else:
            print(f"{C_ERROR}      -> Could not find a Video ID on the page.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"{C_ERROR}      -> Failed to fetch the page: {e}")
        return None, None


def get_video_details(page_content):
    print(f"{C_INFO}[2/4] Analyzing page for Title and Episode info...")
    try:
        soup = BeautifulSoup(page_content, 'html.parser')
        
        
        title_element = soup.find('meta', property='og:title')
        if title_element and title_element.get('content'):
            title = title_element['content']
        else:
            title_element = soup.find('h1')
            if title_element:
                title = title_element.get_text(strip=True)
            else:
                title = "video_file" 

        
        season, episode = None, None
        
        match = re.search(r'(?:Temporada|T)\s*(\d+).*?(?:Cap[íi]tulo|Episodio|E)\s*(\d+)', title, re.IGNORECASE)
        if match:
            season, episode = match.groups()
        
        
        title = re.sub(r'(?:Temporada|T)\s*\d+.*?(?:Cap[íi]tulo|Episodio|E)\s*\d+', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\|.*', '', title) 
        title = title.strip()

        
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug) 
        slug = re.sub(r'[\s-]+', '_', slug).strip('_') 

        
        if season and episode:
            
            episode_info = f"S{int(season):02d}E{int(episode):02d}"
            base_filename = f"{slug}_{episode_info}"
        else:
            base_filename = slug
        
        print(f"{C_SUCCESS}      -> Detected base filename: {C_DATA}{base_filename}")
        return base_filename

    except Exception as e:
        print(f"{C_ERROR}      -> Could not analyze page details: {e}. Using a generic name.")
        return "video_file"

def get_subtitle_info_from_api(video_id):
    api_url = f"https://www.rtve.es/api/videos/{video_id}/subtitulos"
    print(f"{C_INFO}[3/4] Querying the subtitles API...")
    try:
        response = requests.get(api_url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        data = response.json()
        items = data.get("page", {}).get("items", [])
        subtitles_list = [{'lang': item['lang'], 'src': item['src']} for item in items if 'src' in item and 'lang' in item]
        return subtitles_list
    except requests.exceptions.RequestException:
        print(f"{C_ERROR}      -> Failed to query the API.")
        return []
    except (ValueError, KeyError):
        print(f"{C_ERROR}      -> Could not parse the API response.")
        return []

def handle_user_selection(available_subs):
    LANG_MAP = {
        'en': 'English', 'es': 'Español (Spanish)', 'ca': 'Català (Catalan)',
        'gl': 'Galego (Galician)', 'eu': 'Euskera (Basque)', 'va': 'Valencià (Valencian)'
    }
    print(f"\n{C_INFO}Multiple languages found. Please choose which to download:")
    for i, sub in enumerate(available_subs):
        lang_code = sub['lang'].lower()
        lang_name = LANG_MAP.get(lang_code, sub['lang'].upper())
        print(f"  {C_DATA}{i+1}{C_RESET}. {lang_name}")
    
    prompt = (
        f"{C_PROMPT}Enter the number(s) separated by commas (e.g., 1,3), or 'all' to download all:\n> {C_RESET}"
    )
    choice = input(prompt).strip().lower()

    if choice == 'all':
        return available_subs
    selected_subs = []
    try:
        indices = [int(i.strip()) - 1 for i in choice.split(',')]
        for index in indices:
            if 0 <= index < len(available_subs):
                selected_subs.append(available_subs[index])
            else:
                print(f"{C_ERROR}Warning: '{index+1}' is not a valid choice.")
        return selected_subs
    except ValueError:
        print(f"{C_ERROR}Invalid input. Please enter numbers, commas, or 'all'.")
        return []

def download_file(url, custom_filename):
    print(f"{C_INFO}      -> Downloading: {C_DATA}{custom_filename}{C_RESET}")
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        if os.path.exists(custom_filename):
            action = input(f"{C_PROMPT}[WARNING] File '{custom_filename}' exists. (O)verwrite or (S)kip? {C_RESET}").lower()
            if action != 'o':
                print(f"{C_INFO}      -> Skipping file.")
                return
        
        total_size = int(response.headers.get('content-length', 0))
        with open(custom_filename, 'wb') as f, tqdm(
            desc=custom_filename, total=total_size, unit='B', unit_scale=True,
            bar_format='{l_bar}%s{bar}%s{r_bar}' % (C_SUCCESS, C_RESET), ncols=80, leave=False
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
                bar.update(len(chunk))
        print(f"{C_SUCCESS}      -> Successfully saved '{custom_filename}'")
    except Exception as e:
        print(f"\n{C_ERROR}[ERROR] Download failed for this file: {e}")

def show_credits():
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    text_part1 = "</Developed by> "
    text_part2 = "Hzifa33"
    full_text = text_part1 + text_part2

    box_width = len(full_text) + 4
    side_padding = (terminal_width - box_width) // 2
    side_padding_str = ' ' * side_padding

    top_border = f"{side_padding_str}{C_TITLE}╔{'═' * (box_width - 2)}╗"
    bottom_border = f"{side_padding_str}{C_TITLE}╚{'═' * (box_width - 2)}╝"
    
    print("\n")
    print(top_border)

    sys.stdout.write(f"{side_padding_str}{C_TITLE}║ {C_RESET}")
    sys.stdout.flush()

    for char in text_part1:
        sys.stdout.write(C_SUCCESS + char)
        sys.stdout.flush()
        time.sleep(0.04)

    for char in text_part2:
        sys.stdout.write(C_DATA + Style.BRIGHT + char)
        sys.stdout.flush()
        time.sleep(0.08)

    sys.stdout.write(f"{C_TITLE} ║{C_RESET}")
    sys.stdout.flush()
    print()

    print(bottom_border)
    print()

def main():
    print(f"{C_TITLE}=====================================================")
    print(f"{C_TITLE} RTVE Subtitle Downloader (Smart Naming) V6.0 ")
    print(f"{C_TITLE}=====================================================")
    
    page_url = sys.argv[1] if len(sys.argv) > 1 else input(f"{C_PROMPT}Please enter the RTVE video page URL:\n> {C_RESET}")
    if not page_url:
        print(f"{C_ERROR}No URL entered. Exiting.")
        return

    video_id, page_content = find_video_id(page_url)
    if not video_id or not page_content:
        print(f"\n{C_ERROR}Could not proceed without a Video ID.")
        return

    
    base_name = get_video_details(page_content)

    available_subs = get_subtitle_info_from_api(video_id)
    if not available_subs:
        print(f"\n{C_ERROR}No subtitles found for this video.")
        return

    subs_to_download = []
    if len(available_subs) == 1:
        lang_code = available_subs[0]['lang'].upper()
        print(f"{C_SUCCESS}      -> Success! Found 1 subtitle: {C_DATA}{lang_code}{C_SUCCESS}. Starting download directly.")
        subs_to_download = available_subs
    else:
        subs_to_download = handle_user_selection(available_subs)

    if not subs_to_download:
        print(f"\n{C_INFO}No subtitles selected. Exiting.")
        return
    
    print(f"\n{C_INFO}[4/4] Preparing to download selected subtitles...")
    
    _, extension = os.path.splitext(os.path.basename(urlparse(subs_to_download[0]['src']).path))
    
    for i, sub_info in enumerate(subs_to_download):
        
        new_filename = f"{base_name}_{sub_info['lang']}{extension}"
        print(f"\n{C_INFO}Processing [{i+1}/{len(subs_to_download)}]: Language {C_DATA}{sub_info['lang'].upper()}")
        download_file(sub_info['src'], new_filename)

    print("\n" + C_SUCCESS + "---------------------------------------------")
    print(f"✅ All tasks complete!")
    print("---------------------------------------------")
    
    show_credits() 

if __name__ == "__main__":
    main()
