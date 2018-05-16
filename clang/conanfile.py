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

class ClangConan(ConanFile):
    name = "clang"
    version = os.environ.get("CONAN_VERSION_OVERRIDE", VERSION)
    generators = "cmake"
    requires = ("llvm/3.8.0@Manu343726/testing",
                "compiler-rt/3.8.0@Manu343726/testing")
    url = "http://github.com/Manu343726/clang-conan"
    license = "BSD"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "extra_tools": [True, False]}
    default_options = "shared=True"

    def configure(self):
        del self.settings.compiler.libcxx

        if "shared" in self.options:
            self.options["llvm"].shared = self.options.shared
            self.options["compiler-rt"].shared = self.options.shared
            self.options["libcxx"].shared = self.options.shared

    def requirements(self):
        if self.settings.compiler != "Visual Studio":
            self.requires("libcxx/3.8.0@Manu343726/testing")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared
            self.options.extra_tools = False

    def source(self):
        download_extract_llvm_component("cfe", ClangConan.version,
                                        "clang")

        if self.options.extra_tools:
            download_extract_llvm_component("clang-tools-extra", ClangConan.version,
                                            "clang/tools/extra")

    def build(self):
        if self.settings.arch == "x86_64" and self.settings.compiler == "Visual Studio":
            cmake = CMake(self, toolset="host=x64")
        else:
            cmake = CMake(self)

        for component in ["clang"]:
            build = os.path.join(BUILD_DIR, component)
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
             "CMAKE_INSTALL_PREFIX": os.path.join(self.build_folder, INSTALL_DIR),
             "BUILD_SHARED_LIBS": self.options.shared if "shared" in self.options else False,
             "CLANG_ENABLE_ARCMT": False,
             "CLANG_TOOL_ARCMT_TEST_BUILD": False,
             "CLANG_TOOL_CLANG_CHECK_BUILD": False,
             "CLANG_TOOL_CLANG_FORMAT_BUILD": False,
             "CLANG_TOOL_CLANG_FUZZER_BUILD": False,
             "CLANG_TOOL_DIAGTOOL_BUILD": False,
             "CLANG_TOOL_DRIVER_BUILD": False,
             "CLANG_TOOL_DIAGTOOL_BUILD": False,
             "CLANG_TOOL_CLANG_FUZZER_BUILD": False
            }, source_dir="clang")
            cmake.build()
            cmake.install()

    def package(self):
        for component in ["clang"]:
            install = os.path.join(self.build_folder, INSTALL_DIR)
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
        self.copy(pattern="*",
                  dst="lib",
                  src="exports/lib",
                  keep_path=True)
        self.copy(pattern="*",
                  dst="include",
                  src="exports/include",
                  keep_path=True)

    def conan_info(self):
        self.info.settings.build_type = "Release"

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*", dst="include/c++/v1", src="include/c++/v1")
        self.copy("*libclang_rt.*", dst="lib", src="lib")
