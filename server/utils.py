from pathlib import Path
import logging
import aiofiles
import csv
import io
import asyncio
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# read data from csv file
def read_data_from_csv_file(filename):
    filepath = Path(filename)
    if not filepath.is_file():
        logger.error(f"File not found at path: {filename}")
        return []
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8', newline='') as f:
            content = f.read()
            # Use io.StringIO to allow the standard csv library to read the async content
            string_io_content = io.StringIO(content)
            reader = csv.DictReader(string_io_content)
            data = [row for row in reader]
            logger.info(f"Successfully read {len(data)} rows from {filename}")
    except Exception as e:
        logger.error(f"An error occurred while reading the file {filename}: {e}")
        return []

    return data

# read data from csv file
async def async_read_data_from_csv_file(filename: str) -> list[dict]:
    """
    Asynchronously reads data from a CSV file and returns it as a list of dictionaries.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a row.
                    Returns an empty list if the file is not found or an error occurs.
    """
    filepath = Path(filename)
    if not filepath.is_file():
        logger.error(f"File not found at path: {filename}")
        return []

    data = []
    try:
        async with aiofiles.open(filepath, mode='r', encoding='utf-8', newline='') as f:
            content = await f.read()
            # Use io.StringIO to allow the standard csv library to read the async content
            string_io_content = io.StringIO(content)
            reader = csv.DictReader(string_io_content)
            data = [row for row in reader]
            logger.info(f"Successfully read {len(data)} rows from {filename}")
    except Exception as e:
        logger.error(f"An error occurred while reading the file {filename}: {e}")
        return []

    return data



async def main():
    # Create a dummy CSV file for testing
    file_to_read = "test_data.csv"
    with open(file_to_read, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "value"])
        writer.writerow(["1", "alpha", "100"])
        writer.writerow(["2", "beta", "200"])
        writer.writerow(["3", "gamma", "300"])

    # Test reading the created file
    list_of_dicts = await read_data_from_csv_file(file_to_read)
    print(list_of_dicts)

    # Test reading a non-existent file
    list_of_dicts_error = await read_data_from_csv_file("non_existent_file.csv")
    print(list_of_dicts_error)

if __name__ == "__main__":
    asyncio.run(main())