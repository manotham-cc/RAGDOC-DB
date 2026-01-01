import logging
import sys
import os

# Add project root to sys.path to ensure modules can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.gen_data import init_cybersecurity_table
from ragdoc.build_index import build_vector_index

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_all_databases():
    """
    Initializes both the structured SQL database and the Vector database.
    """
    print("==========================================")
    print(" STARTING SYSTEM INITIALIZATION")
    print("==========================================")

    # 1. Initialize Structured Database
    print("\n[1/2] Initializing SQL Database (Cybersecurity Incidents)...")
    try:
        init_cybersecurity_table()
    except Exception as e:
        logger.error(f"Failed to initialize SQL Database: {e}")

    # 2. Initialize Vector Database
    print("\n[2/2] Initializing Vector Database (Documents)...")
    try:
        build_vector_index()
    except Exception as e:
        logger.error(f"Failed to initialize Vector Database: {e}")

    print("\n==========================================")
    print(" INITIALIZATION COMPLETE")
    print("==========================================")

if __name__ == "__main__":
    init_all_databases()
