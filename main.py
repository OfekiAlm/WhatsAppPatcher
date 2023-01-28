import argparse
import os
from termcolor import cprint
from extractor import Extractor
from patcher import Patcher


def main():
    parser = argparse.ArgumentParser(description="Bump Version")
    parser.add_argument("-path", "-p", dest="path", type=str, required=True)
    parser.add_argument("-output", "-o", dest="output", type=str, required=True)
    parser.add_argument(
        "--temp-path", dest="temp_path", type=str, default="./extracted"
    )
    args = parser.parse_args()
    if not os.path.exists(args.path) or not os.access(args.path, os.R_OK):
        cprint("[+] File doesn't exists or required reading permissions", color="red")
        exit(-1)
    if not args.path.endswith(".apk") or not args.output.endswith(".apk"):
        cprint(
            "[+] Input path and output path supposed to be a path to apk.", color="red"
        )
        exit(-1)
    extractor = Extractor(args.path, args.output)
    extractor.extract_apk()
    extractor.extract_dex()
    patcher = Patcher(extractor.temp_path, args.path)
    patcher.patch()
    extractor.compile_smali()
    cprint("[+] Smali has been compiled.", "green")
    extractor.sign_apk()
    cprint("[+] Apk has been signed.", "green")


if __name__ == "__main__":
    main()
