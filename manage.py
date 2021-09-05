from bs4 import BeautifulSoup
import requests
import json
from termcolor import colored

def get_links(url):
    """
        Get "stuff" links in each page of the website ( from the first 20 links on the main page )
    """
    req = requests.get(url)

    #open the main-page "index.html"
    with open("app/index.html", "w", encoding='utf-8') as file:
        file.write(req.text)

    with open("app/index.html", encoding='utf-8') as file:
        src = file.read()


    soup = BeautifulSoup(src, "lxml")

    all_links = soup.find(class_="course").find_all("a")
    main_page = soup.find("h1", class_='main-page')


    projects_links_in_stuff = []
    project_urls = []
    # get all links on main_page
    for link in all_links:
        project_link_text = link.text
        project_url = url + link.get("href")
        project_urls.append(project_url)

    #get the necessary ending of url in project_urls
    for project_url in project_urls:
        req = requests.get(project_url)
        project_name = project_url.split('/')[-1]

        # add files in directory data
        with open(f"app/data/{project_name}", "w", encoding='utf-8') as file:
            file.write(req.text)

        with open(f"app/data/{project_name}",encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        #find in the footer class "stuff" and get links
        stuff = soup.find("div", class_='stuff')
        if stuff is not None:
            all_linksfooter = soup.find("div", class_='stuff').find_all("a")
        else:
            continue
        
        #append the links in json file
        for link in all_linksfooter:
            linkfooter_text = link.text
            linkfooter_url = link.get("href")

            projects_links_in_stuff.append (
                {
                    'Название': linkfooter_text,
                    'Ссылка': linkfooter_url
                }
            )
        with open('app/json/all_links_in20lessons.json', "w", encoding="utf-8") as file:
            json.dump(projects_links_in_stuff, file, indent=5, ensure_ascii=False)
        
def main():
    get_links("https://kidkodschool.github.io/")

if __name__ == '__main__':
    main()