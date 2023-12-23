import flet as ft;
from mangapanda import MangaPanda;
import requests;
import os;

class MangaReader(ft.UserControl):
    def __init__(self, page):
        super().__init__();
        self.page = page;

    def download_chapter(self, name, links):
        folder = "{pwd}/chapters/{nm}".format(pwd = os.getcwd(), nm = '_'.join(name.split(" ")).lower());
        if os.path.exists(folder):
            return;
        else: 
            os.mkdir(folder);
            for n, link in enumerate(links):
                img = requests.get(link);
                with open(f"{folder}/ch{n}.jpg", "wb") as f:
                    f.write(img.content);

    def read(self, e):
        name = e.control.text;
        self.page.clean();
        images = ft.Column(width = self.page.width, height = self.page.height, scroll = ft.ScrollMode.ALWAYS);
        links = MangaPanda().fetch_image(name, 1);
        self.download_chapter(name, links);
        for n in range(len(links)):
            nm = '_'.join(name.split(" ")).lower();
            images.controls.append(
                ft.Container(alignment = ft.alignment.center, content = ft.Image(src = f"/chapters/{nm}/ch{n}.jpg", fit = ft.ImageFit.CONTAIN))
            );

        self.page.add(images);

    def search(self, e):
        name = e.control.value;
        self.page.clean();
        mangas_found = ft.Column(scroll = ft.ScrollMode.ALWAYS, height = self.page.height, width = self.page.width);
        mangas = MangaPanda().search(name);
        for manga in mangas:
            mangas_found.controls.append(
                ft.Row(controls = [
                    ft.Image(src = mangas[manga]["cover"]),
                    ft.Column(controls = [
                        ft.TextButton(text = manga, on_click = self.read),
                        ft.Text(mangas[manga]["genre"]),
                    ]),
                ])
            );
        self.page.add(mangas_found);

    def build(self):
        return ft.Column(controls = [
            ft.TextField(label = "Search", hint_text = "Solo Leveling", on_submit = self.search),
        ], alignment = ft.MainAxisAlignment.CENTER);
        
def entry(page):
    page.add(MangaReader(page));

ft.app(target = entry, view = None, assets_dir = "chapters", port=os.getenv("PORT", default=5000));
