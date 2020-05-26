from PIL import Image
from PyPDF2 import PdfFileMerger

from services.repositories import save_photo, create_random_string


def photo_converter(photoList):
    filename = create_random_string()
    imageList = []
    for url in photoList:
        path = save_photo(url)
        imageList.append(Image.open(path))

    first = imageList[0]
    del imageList[0]
    path = "static/docs/" + filename + ".pdf"
    print(filename)
    if len(imageList) != 0:
        first.save(path, save_all=True, append_images=imageList)
    else:
        first.save(path)
    return path


def add_photo_to_file(main_file_path, add_file_path):
    merger = PdfFileMerger()
    merger.append(main_file_path)
    print("main path {}".format(main_file_path))
    merger.append(add_file_path)
    filename = create_random_string()
    path = "static/docs/" + filename + ".pdf"
    merger.write(path)
    merger.close()
    return path


if __name__ == '__main__':
    pathList = ["photos/arpufuer.png", ]
    photo_converter(pathList)
