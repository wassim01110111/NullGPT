import json
import traceback

from bs4 import BeautifulSoup
from pageDL import html_folder, sanitize_filename, url_list_path

not_support_html = set()

DEBUG = True


def unsupported(url):
    print(url, "is not supported yet")
    not_support_html.add(url)


def paragraph_analysis(paragraph):
    input(paragraph.get_text().replace("\n", ""))


def main():
    with open(url_list_path, "r", encoding="utf-8") as f:
        url_list = json.load(f)

    error_html = set()

    total = len(url_list)

    for i, url in enumerate(url_list, start=1):
        print(url)
        file_path = html_folder / f"{sanitize_filename(url)}.html"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
            containers = soup.find_all("div", class_="mw-content-ltr mw-parser-output")
            if containers:
                main_container = containers[0]
                for aside in main_container.find_all("aside"):
                    aside.decompose()
                paragraphs = containers[0].find_all("p", recursive=False)
                for p in paragraphs:
                    if p.get_text(strip=True):
                        paragraph_analysis(p)
            else:
                unsupported(url)

            percent = (i / total) * 100
            print(f"Processed {i}/{total} ({percent:.2f}%) - {url}")
        except Exception as e:
            error_html.add(url)
            print(f"\n❌ Error while processing URL: {url}")
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception message: {e}")
            print("Traceback:")
            traceback.print_exc()


if __name__ == "__main__":
    main()
