from BlockManager import Block, BlockGenerator
from StorageManager import FileController
from DataInitializer import DataInitializer
import hashlib, json


def main():
    block_height = FileController.get_block_height()
    print block_height
    DataInitializer.initialize_block()


if __name__ == "__main__":
    main()
