from contextlib import contextmanager
from conans.tools import download, unzip
import shutil
import os
import platform


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



SOURCES_REPOSITORY = os.environ.get("CONAN_LLVM_SOURCES_REPO", "https://dl.bintray.com/manu343726/llvm-sources")

def get_sources(component, version, dest):
    package_name = "{}-{}.src".format(component, version)
    file_url = "{url}/{package}.tar.gz".format(url=SOURCES_REPOSITORY, package=package_name)
    extract_from_url(file_url)
    shutil.move(package_name, dest)

BUILD_DIR = ("C:/__build" if platform.system == "Windows"
             else "build")
INSTALL_DIR = "install"  # This needs to be a relative path

def package(conanfile):
    self.copy(pattern="*",
              dst="include",
              src=os.path.join(INSTALL_DIR, "include"),
              keep_path=True)
    for pattern in ["*.a*", "*.h", "*.so*", "*.lib", "*.dylib*", "*.dll*", "*.cmake"]:
        self.copy(pattern=pattern,
                  dst="lib",
                  src=os.path.join(INSTALL_DIR, "lib"),
                  keep_path=True)
    self.copy(pattern="*",
              dst="share",
              src=os.path.join(INSTALL_DIR, "share"),
              keep_path=True)
    self.copy(pattern="*",
              dst="bin",
              src=os.path.join(INSTALL_DIR, "bin"),
              keep_path=True)
    self.copy(pattern="*",
              dst="libexec",
              src=os.path.join(INSTALL_DIR, "libexec"),
              keep_path=True)
