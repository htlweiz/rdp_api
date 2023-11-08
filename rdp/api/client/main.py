
import os
from uploader import FileUploader


def main():

    # In this example there is only one room
    # so every device is in room with id of 1

    os.environ['NO_PROXY'] = '127.0.0.1'
    csvFileLocation = "./STD_öhm.csv"

    fileUploader = FileUploader(csvFileLocation)
    fileUploader.uploadDevice()
    fileUploader.uploadValue()


if __name__ == "__main__":
    main()
