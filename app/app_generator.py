import argparse
import os
from services.image_processor import ImageProcessor


def main(title: str, subtitle: str, output_path: str):
    image_processor = ImageProcessor()
    image_bytes = image_processor.add_text_to_image(title, subtitle)

    # Создаем директорию, если она не существует
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(image_bytes.getvalue())
    print(f"Image saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate an image with title and subtitle."
    )
    parser.add_argument(
        "-t", "--title", type=str, required=True, help="Title text for the image"
    )
    parser.add_argument(
        "-s", "--subtitle", type=str, required=True, help="Subtitle text for the image"
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        default="output/image.png",
        help="Output path for the generated image",
    )

    args = parser.parse_args()
    main(args.title, args.subtitle, args.output_path)
