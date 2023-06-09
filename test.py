import os
import unittest
from main import (
    DirectoryNotFound,
    DirectoryIsEmpty,
    get_files,
    images_metadata,
    optimize_images,
    get_images_size,
    filter_files,
    get_absolute_path
)
import tempfile


class TestImgOptimizer(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_directory = get_files(get_absolute_path("images"))
        self.invalid_directory = "imgs"
        self.filtered_files = filter_files(self.valid_directory)

    def test_get_files(self) -> None:
        valid_directory_images = get_files("images")
        self.assertTrue(valid_directory_images)
        self.assertIsInstance(valid_directory_images, list)

        for file in valid_directory_images:
            self.assertIsInstance(file, str)

        invalid_directory_example = self.invalid_directory
        with self.assertRaises(DirectoryNotFound):
            get_files(invalid_directory_example)

        with self.assertRaises(DirectoryIsEmpty):
            filter_files(get_files(os.getcwd()))

    def test_filter_files(self) -> None:
        filter = self.filtered_files
        self.assertIsInstance(filter, list)

        for filter_file in filter:
            self.assertIsInstance(filter_file, str)

        # invalid argument
        with self.assertRaises(ValueError):
            filter_files(files=[])

    def test_images_metadata(self) -> None:
        images = self.valid_directory
        metadata = images_metadata(images)

        self.assertIsInstance(metadata, dict)

    def test_optimize_images(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            images = self.filtered_files
            optimize_images(
                images, from_directory="images", to_directory=temp_dir, quality=50
            )

            optimized_images = get_files(temp_dir)

            self.assertEqual(len(images), len(optimized_images))

            for original_image, optimized_image in zip(images, optimized_images):
                original_size = os.path.getsize(os.path.join("images", original_image))
                optimized_size = os.path.getsize(
                    os.path.join(temp_dir, optimized_image)
                )
                self.assertLess(
                    optimized_size,
                    original_size,
                    f"Optimized image {optimized_image} is not smaller than the original.",
                )

    def test_get_images_size(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            images = self.filtered_files

            optimize_images(
                images, from_directory="images", to_directory=temp_dir, quality=50
            )

            images_optimized = filter_files(get_files(temp_dir))
            sizes_original_img = get_images_size(images, directory="images")
            sizes_optimized_img = get_images_size(images_optimized, directory=temp_dir)

            self.assertIsInstance(sizes_original_img, dict)

            for key in sizes_original_img.keys():
                self.assertIsInstance(key, str)

            for value in sizes_original_img.values():
                self.assertIsInstance(value, str)

            original_sizes = [
                float(value.split(" ")[0]) for value in sizes_original_img.values()
            ]
            optimized_sizes = [
                float(value.split(" ")[0]) for value in sizes_optimized_img.values()
            ]

            for i in range(len(original_sizes)):
                original_size = original_sizes[i]
                optimized_size = optimized_sizes[i]
                self.assertLess(
                    optimized_size,
                    original_size,
                    f"Image {i+1}: Optimized size is not smaller than original size.",
                )


if __name__ == "__main__":
    unittest.main()
