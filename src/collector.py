"""
Script to fetch and save documents from the Brown Digital Repository API.
Searches for H.P. Lovecraft collection items by genre and saves them as JSON files.
"""

import json
import logging
import random
import sys
from enum import Enum
from time import sleep

import requests

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

logger = logging.getLogger(__name__)


class Collection(Enum):
    """Collection identifiers for BDR searches."""

    HOWARD_P_LOVECRAFT_COLLECTION = "bdr:jyhg75bu"


# Genre types to search for in the collection
GENRES = [
    "autograph letter",
    "autograph letter signed",
    "autograph note signed",
    "typed letter",
    "typed letter signed",
]

# API configuration
BASE_URL = "https://repository.library.brown.edu/api/search/"
PAGE_SIZE = 100
MIN_PAUSE_SECONDS = 1
MAX_PAUSE_SECONDS = 2


def save_document(doc: dict, output_dir: str = "./metadata") -> str:
    """
    Save a document as a JSON file.

    Args:
        doc: Document dictionary containing at minimum a 'pid' field
        output_dir: Directory to save the file (default: current directory)

    Returns:
        The filepath where the document was saved
    """
    pid = doc["pid"].split(":")[1]
    filepath = f"{output_dir}/{pid}.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(doc, file, indent=4)
    return filepath


def build_search_query(collection_id, genre):
    """
    Build the search query string for the BDR API.

    Args:
        collection_id: Collection identifier
        genre: Genre type to search for

    Returns:
        Formatted query string
    """
    query_parts = [
        f'rel_is_member_of_collection_ssim:"{collection_id}"',
        f'genre_local:"{genre}"',
        'mods_role_creator_ssim:"Lovecraft, H.P. (Howard Phillips)"',
        'mods_access_condition_rights_text_tsim:"No Copyright - United States."',
        'mods_access_condition_restriction_text_tsim:"Collection is open for research."',
    ]
    return " AND ".join(query_parts)


def fetch_and_save_documents(genre):
    """
    Fetch documents for a specific genre and save them as JSON files.

    Args:
        genre: The genre type to search for
    """
    query = build_search_query(Collection.HOWARD_P_LOVECRAFT_COLLECTION.value, genre)
    start = 0

    while True:
        logger.debug(f"start: {start}")

        try:
            params = {"q": query, "start": start, "rows": PAGE_SIZE}
            logger.info(f"GET: {BASE_URL} with params: {params}")

            response = requests.get(BASE_URL, params=params)

            logger.debug(f"status_code: {response.status_code}")

            if response.status_code == 200:
                docs = response.json()["response"]["docs"]
                logger.debug(f"len(docs): {len(docs)}")

                if not docs:
                    break

                for doc in docs:
                    save_document(doc)

                # Pause to avoid overwhelming the server
                pause = MIN_PAUSE_SECONDS + random.random() * (
                    MAX_PAUSE_SECONDS - MIN_PAUSE_SECONDS
                )
                logger.debug(f"pause for {pause:.2f} seconds")
                sleep(pause)
            else:
                logger.error(f"Request failed with status code: {response.status_code}")
                break

        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            break
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Data parsing error: {e}")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break

        start += PAGE_SIZE

    logger.info(f"Completed processing genre: {genre}")


def main():
    """Main entry point for the script."""
    for genre in GENRES:
        logger.info(f"Processing genre: {genre}")
        fetch_and_save_documents(genre)


if __name__ == "__main__":
    main()
