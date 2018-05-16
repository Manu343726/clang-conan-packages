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
    major, minor, _ = release.split(".")
    release_branch = "release_{}{}".format(major, minor)
    os.system("git clone https://github.com/llvm-mirror/{} --branch {} {}".format(
        component, release_branch, extract_to))


BUILD_DIR = ("C:/__build" if platform.system == "Windows"
             else "build")
INSTALL_DIR = "install"  # This needs to be a relative path

class CompilerRTConan(ConanFile):
    name = "compiler-rt"
    version = os.environ.get("CONAN_VERSION_OVERRIDE", VERSION)
    generators = "cmake"
    requires = ("llvm/3.8.0@Manu343726/testing", )
    url = "http://github.com/Manu343726/compiler-rt-conan"
    license = "BSD"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources="*.patch"

    def configure(self):
        del self.settings.compiler.libcxx

        if "shared" in self.options:
            self.options["llvm"].shared = self.options.shared

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

    def source(self):
        download_extract_llvm_component("compiler-rt", CompilerRTConan.version,
                                        "compiler-rt")

    def build(self):
        cmake = CMake(self)

        for component in ["compiler-rt"]:
            install = os.path.join(INSTALL_DIR, component)
            try:
                os.makedirs(install)
            except OSError:
                pass

            if not os.path.exists(os.path.join(self.build_folder,
                                               component,
                                               "CMakeListsOriginal.txt")):
                shutil.move(os.path.join(self.build_folder,
                                         component,
                                         "CMakeLists.txt"),
                            os.path.join(self.build_folder,
                                         component,
                                         "CMakeListsOriginal"))
                with open(os.path.join(self.build_folder,
                                       component,
                                       "CMakeLists.txt"), "w") as cmakelists_file:
                    cmakelists_file.write("cmake_minimum_required(VERSION 2.8)\n"
                                          "include(\"${CMAKE_CURRENT_LIST_DIR}/../conanbuildinfo.cmake\")\n"
                                          "conan_basic_setup()\n"
                                          "set (CMAKE_PREFIX_PATH \"${CONAN_LLVM_ROOT}\")\n"
                                          "set (CMAKE_PROGRAM_PATH \"${CONAN_BIN_DIRS_LLVM}\")\n"
                                          "if (APPLE OR UNIX)\n"
                                          "  set (CMAKE_EXE_LINKER_FLAGS \"${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath,${CONAN_LIB_DIRS}\")\n"
                                          "  set (CMAKE_SHARED_LINKER_FLAGS \"${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath,${CONAN_LIB_DIRS}\")\n"
                                          "endif ()\n"
                                          "message (STATUS \"${CMAKE_PROGRAM_PATH}\")\n"
                                          "include(CMakeListsOriginal)\n")

                cmake.configure(defs={
                 "CLANG_INCLUDE_DOCS": False,
                 "CLANG_INCLUDE_TESTS": False,
                 "CLANG_TOOLS_INCLUDE_EXTRA_DOCS": False,
                 "COMPILER_RT_INCLUDE_TESTS": False,
                 "LIBCXX_INCLUDE_TESTS": False,
                 "LIBCXX_INCLUDE_DOCS": False,
                 "LLVM_INCLUDE_TESTS": False,
                 "LLVM_INCLUDE_EXAMPLES": False,
                 "LLVM_INCLUDE_GO_TESTS": False,
                 "LLVM_BUILD_TESTS": False,
                 "CMAKE_VERBOSE_MAKEFILE": True,
                 "LLVM_TARGETS_TO_BUILD": "X86",
                 # AddressSanitizers disabled, cannot be built with latest glibc
                 # I tried first to patch the sanitizers, without result. See sanitizer_stack_t_glibc.patch
                 "COMPILER_RT_BUILD_SANITIZERS": False,
                 "CMAKE_INSTALL_PREFIX": os.path.join(self.build_folder, INSTALL_DIR),
                 "BUILD_SHARED_LIBS": self.options.shared if "shared" in self.options else False
                }, source_folder="compiler-rt")
                cmake.build()
                cmake.install()

    def package(self):
        for component in ["compiler-rt"]:
            install = os.path.join(INSTALL_DIR, component)
            self.copy(pattern="*",
                      dst="include",
                      src=os.path.join(install, "include"),
                      keep_path=True)
            for pattern in ["*.a", "*.h", "*.so*", "*.lib", "*.dylib", "*.dll", "*.cmake"]:
                self.copy(pattern=pattern,
                          dst="lib",
                          src=os.path.join(install, "lib"),
                          keep_path=True)
            self.copy(pattern="*",
                      dst="share",
                      src=os.path.join(install, "share"),
                      keep_path=True)
            self.copy(pattern="*",
                      dst="bin",
                      src=os.path.join(install, "bin"),
                      keep_path=True)
            self.copy(pattern="*",
                      dst="libexec",
                      src=os.path.join(install, "libexec"),
                      keep_path=True)

