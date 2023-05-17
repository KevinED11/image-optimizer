from PIL import Image
import os
import humanize


class DirectoryNotFound(Exception):
    pass


def source_directory(directory: str) -> list[str]:
    dir_path = os.path.abspath(directory)  
    return os.listdir(dir_path)


def showImage(image_path: str) -> None:
    dir_path = os.path.abspath(image_path)
    with Image.open(dir_path) as image:
        image.show()
    

def images_metadata(images: list[str]) -> dict[str, list]:
    data = {}
    dir_path = os.path.abspath("images")
    for image in images:
        data[image] = []
        with Image.open(os.path.join(dir_path, image)) as img:
            data[image].append(img.format)
            data[image].append(img.size)

    return data

  
def optimize_images(images: list[str], from_directory: str, to_directory: str, quality: float = 50) -> None:
    from_dir_path = os.path.abspath(from_directory)
    to_dir_path = os.path.abspath(to_directory)

    os.makedirs(to_dir_path, exist_ok=True)

    for name_image in images:
        with Image.open(os.path.join(from_dir_path, name_image)) as img:
            file_name = f"optimized_{name_image}"
            img.save(to_dir_path + "/" + file_name, optimize=True, quality=quality)

                      
def get_images_size(images: list[str], directory: str) -> dict[str, float]:
    dir_path = os.path.abspath(directory)
    sizes = {}
    for image in images:
        sizes[image] = humanize.naturalsize(os.path.getsize(os.path.join(dir_path, image)))

    return sizes



def main():
    images = source_directory(directory="images")
    images2 = source_directory(directory="dist")
  

    metadata = images_metadata(images)
    print(metadata)

    optimize_images(images, from_directory="images",
                    to_directory="/home/kevind/Documentos/Workspace", quality=10)
    
    sizes = get_images_size(images, directory="images")
    sizes2 = get_images_size(images2, directory="dist")
    print(sizes)
    print(sizes2)
    

if __name__ == "__main__":
    main()