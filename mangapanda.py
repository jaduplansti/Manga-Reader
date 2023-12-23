import requests;
from bs4 import BeautifulSoup;
from AnilistPython import Anilist

class MangaPanda():
  def __init__(self):
    self.url = "https://mangapanda.in";

  def search(self, name):
    mangas = {};
    page = requests.get("{url}/search?q={name}".format(url = self.url, name = name.replace(" ", "+")));
    parsed_page = BeautifulSoup(page.content, "html.parser");
    for x in parsed_page.find_all("div", class_ = "media-body"):
      name = x.find("a")["title"];
      try: 
        manga = Anilist().get_manga(name);
        mangas.update({
          name : {
          "cover" : manga["cover_image"],
          "genre" : ','.join(manga["genres"]),
          "chapters" : manga["chapters"],
          "desc" : manga["desc"],
        }
        });
      except IndexError as err:
        pass;
    
    return mangas;
    
  def fetch_image(self, manga, chapter):
    page = requests.get("{url}/{name}-chapter-{chapter}#1".format(url = self.url, name = '-'.join(manga.split(" ")), chapter = chapter));
    parser = BeautifulSoup(page.content, "html.parser");
    images = parser.find("p", id = "arraydata").text.split(",");
    return images;
