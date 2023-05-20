from PIL import Image
import os
import humanize


class DirectoryNotFound(Exception):
    pass


class DirectoryIsEmpty(Exception):
    pass


def get_files(directory: str) -> list[str]:
    dir_path = os.path.abspath(directory)
    if not os.path.exists(dir_path):
        raise DirectoryNotFound(f"Directory not found: {dir_path}")
    
    files = os.listdir(dir_path)
    if not files:
        raise DirectoryIsEmpty("This directory is empty")

    return files


def filter_files(files: list[str]) -> list[str]:
    if not isinstance(files, list) or not files :
        raise ValueError("Invalid argument")
    
    if valid_files := [file for file in files
                       if os.path.splitext(file)[1]
                       in [".jpg", ".webp", ".png"]]:
        return valid_files
    raise DirectoryIsEmpty("This directory is empty")


def show_image(image_path: str) -> None:
    dir_path = os.path.abspath(image_path)
    with Image.open(dir_path) as image:
        image.show()


def images_metadata(images: list[str]) -> dict[str, list]:
    dir_path = os.path.abspath("images")
    data = {}
    for image in images:
        data[image] = []
        with Image.open(os.path.join(dir_path, image)) as img:
            data[image].append(img.format)
            data[image].append(img.size)

    return data


def optimize_images(images: list[str], from_directory: str,
                    to_directory: str, quality: float = 50,
                    output_format: str= "WEBP") -> None:
    from_dir_path = os.path.abspath(from_directory)
    to_dir_path = os.path.abspath(to_directory)

    os.makedirs(to_dir_path, exist_ok=True)

    for name_image in images:
        with Image.open(os.path.join(from_dir_path, name_image)) as img:
            file_name = f"optimized_{os.path.splitext(name_image)[0]}"
            output_path = os.path.join(to_dir_path, file_name + "." + output_format.lower())
            img.save(output_path,
                     optimize=True, quality=quality,
                     format=output_format)


def get_images_size(images: list[str], directory: str) -> dict[str, str]:
    dir_path = os.path.abspath(directory)
    sizes = {}
    for image in images:
        sizes[image] = humanize.naturalsize(
            os.path.getsize(os.path.join(dir_path, image)))

    return sizes


def main() -> None:
    try:
        images = get_files(directory="images")
        images2 = get_files(directory="dist")
        filter = filter_files(images)
        filter2 = filter_files(images2)

        metadata = images_metadata(images)
        print(metadata)

        optimize_images(filter, from_directory="images",
                        to_directory="/home/kevind/Documentos/Workspace",
                        quality=50)

        sizes = get_images_size(filter, directory="images")
        sizes2 = get_images_size(filter2, directory="dist")
        print(sizes)
        print(sizes2)
    except (DirectoryNotFound, DirectoryIsEmpty, 
            ValueError) as err:
        print(err)


if __name__ == "__main__":
    main()
