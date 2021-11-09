import requests  # getting content of the TED Talk page
from bs4 import BeautifulSoup  # web scraping
import re  # Regular Expression patter matching
import sys  # for argument parsing


def get_url():
    """
    Gets the url from the argument
    if url is not found, throws an error
    Returns the TED Talk url
    """
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        sys.exit("Error: Please enter the TED Talk URL")
    return url


def scrape_mp4_url(url):
    """
    Gets the TED Talk URL and
    Scrapes the webpage for .mp4 reference
    Returns the mp4 url
    """
    print("Scraping the page " + url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
    result = ''
    for val in soup.findAll("script"):
        if (re.search("talkPage.init", str(val))) is not None:
            result = str(val)
    print("Scraping complete ...")
    result_mp4 = re.search("(?P<url>https?://[^\s]+)(mp4)", result).group("url")
    mp4_url = result_mp4.split('"')[0]
    print("MP4 URL Found!")
    return mp4_url


def download_and_save(mp4_url):
    """
    Gets the mp4 url
    Gets the mp4 file using requests module
    Saves it in a file
    """
    print("Download about to start")
    print("Downloading video from " + mp4_url)
    r = requests.get(mp4_url)
    print("Download Complete ....!")
    file_name = mp4_url.split("/")[-1].split('?')[0]
    print("Storing video in - " + file_name)
    with open(file_name, 'wb') as f:
        f.write(r.content)

    print("File has been Saved !")


def main():
    url = get_url()
    mp4_url = scrape_mp4_url(url)
    download_and_save(mp4_url)


if __name__ == '__main__':
    main()
