from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urlsplit

filenames = """
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/youre-invited-to-a-ceili-exploring-irish-dance.jpg
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/irish_dance.ashx
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/irish_dance.ashx
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/irish-dancers.ashx
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/irish-shoes.ashx
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/irish_costumes_2.jpg
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/irish_costumes_3.jpg
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/irish_costumes_4.jpg
   https://artsedge.kennedy-center.org/~/media/ArtsEdge/Images/LessonArt/grade-3-4/ceili/stolen-child.ashx
""".strip().split("\n")

filenames = [x.strip() for x in filenames]

def create_carousel(filenames):
    """Take a list of filenames and create a HTML5App.
       It is not the job of this function to convert URLs to filenames!"""

    with open("html/play_template.html", "rb") as f:
        html_bytes = f.read()

    soup = BeautifulSoup(html_bytes, "html5lib")
    # note: this just uses the order in the HTML document -- not very stable
    small_slick_replace, large_slick_replace = soup.findAll("divreplace")

    def add_image(parent_tag, imgsrc, thumbnail=False):
        div_tag = soup.new_tag("div")
        img_tag = soup.new_tag("img")
        img_tag.attrs['src'] = imgsrc
        if thumbnail:
            img_tag.attrs['width'] = 100
            img_tag.attrs['height'] = 100
        div_tag.insert(0, img_tag)
        parent_tag.insert(0, div_tag)

    # this could probably be tidied to remove the <placeholder> tag.
    large_slick = soup.new_tag("placeholder")
    for filename in reversed(filenames):
        add_image(large_slick, filename)

    small_slick = soup.new_tag("placeholder")
    for filename in reversed(filenames):
        add_image(small_slick, filename, thumbnail=True)

    large_slick_replace.replace_with(large_slick)
    small_slick_replace.replace_with(small_slick)
    large_slick.replaceWithChildren()
    small_slick.replaceWithChildren()

    with open("html/play_output.html", "w") as f:
        f.write(soup.prettify())

create_carousel(filenames)
