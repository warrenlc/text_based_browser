import argparse
import os
import collections
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def invalid_site(site_name):
    if site_name != "back":
        return "." not in site_name

def open_page(website, path):
    file_name = path + "/" + website[7:-4]
    r = requests.get(website)
    soup = BeautifulSoup(r.content, 'html.parser')
    tags = ['title', 'p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    to_show = soup.find_all(tags)
    to_print = []
    for k in to_show:
        if k.name == 'a' and k.text.strip() != "":
            to_print.append(Fore.BLUE + k.text)
        elif k.text.strip() != "":
            to_print.append(k.text)
    page = ""
    with open(file_name, "w") as writing:
        for k in to_print:

            print(k)
            page += k
            writing.write(k)
    return page


def main():
    parser = argparse.ArgumentParser(description="get the path for the webpage file")
    parser.add_argument("path", type=str)
    args = parser.parse_args()

    try:
        os.mkdir(args.path)
    except FileExistsError:
        print("Error. File already exists")

    history = collections.deque()

    while True:
        try:
            site = input()
            if site == "exit":
                break
            if site == "back":
                print(history.popleft())
            else:
                if "https://" not in site:
                    site = "https://" + site
                page = open_page(site, args.path)
                history.append(page)
        except requests.exceptions.InvalidURL:
            print("Incorrect URL")
        except requests.exceptions.ConnectionError:
            print("Incorrect URL")


if __name__ == '__main__':
    main()
