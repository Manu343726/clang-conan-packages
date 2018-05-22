from contextlib import contextmanager
from conans import ConanFile, CMake
from conans.tools import download, unzip
import shutil
import os
import platform

VERSION = "3.8.0"


@contextmanager
def in_dir(directory):
    last_dir = os.getcwd()
    try:
        os.makedirs(directory)
    except OSError:
        pass

    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(last_dir)


def extract_from_url(url):
    print("download {}".format(url))
    zip_name = os.path.basename(url)
    download(url, zip_name)
    unzip(zip_name)
    os.unlink(zip_name)


def download_extract_llvm_component(component, release, extract_to):
    extract_from_url("https://bintray.com/artifact/download/"
                     "polysquare/LLVM/{comp}-{ver}.src.zip"
                     "".format(ver=release, comp=component))
    shutil.move("{comp}-{ver}.src".format(comp=component,
                                          ver=release),
                extract_to)


BUILD_DIR = ("C:/__build" if platform.system == "Windows"
             else "build")
INSTALL_DIR = "install"  # This needs to be a relative path
