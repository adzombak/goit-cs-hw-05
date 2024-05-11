import argparse
import asyncio
import aiofiles
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(src_path, dest_folder):
    try:
        extension = src_path.suffix[1:]
        target_folder = dest_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(src_path, "rb") as src_file:
            content = await src_file.read()

        target_file = target_folder / src_path.name
        async with aiofiles.open(target_file, "wb") as dest_file:
            await dest_file.write(content)
    except Exception as e:
        logging.error(f"Error copying file {src_path}: {e}")


async def read_folder(src_folder, dest_folder):
    for path in src_folder.rglob("*.*"):
        if path.is_file():
            await copy_file(path, dest_folder)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sort files by extension asynchronously."
    )
    parser.add_argument(
        "src_folder",
        type=str,
        nargs="?",
        default="./src",
        help="Source folder path",
    )
    parser.add_argument(
        "dest_folder",
        type=str,
        nargs="?",
        default="./dest",
        help="Destination folder path",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    src_folder = Path(args.src_folder)
    dest_folder = Path(args.dest_folder)

    asyncio.run(read_folder(src_folder, dest_folder))


if __name__ == "__main__":
    main()
