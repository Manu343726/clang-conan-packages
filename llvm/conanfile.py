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

class LLVMConan(ConanFile):
    name = "llvm"
    version = os.environ.get("CONAN_VERSION_OVERRIDE", VERSION)
    generators = "cmake"
    requires = tuple()
    url = "http://github.com/smspillaz/llvm-conan"
    license = "BSD"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared


    def source(self):
        download_extract_llvm_component("llvm", LLVMConan.version, "src")

    def build(self):
        cmake = CMake(self)
        try:
            os.makedirs(INSTALL_DIR)
        except OSError:
            pass

        try:
            shutil.rmtree(BUILD_DIR)
        except OSError:
            pass

        cmake.configure(defs={
         "CLANG_INCLUDE_DOCS": False,
         "CLANG_INCLUDE_TESTS": False,
         "CLANG_TOOLS_INCLUDE_EXTRA_DOCS": False,
         "COMPILER_RT_INCLUDE_TESTS": False,
         "LIBCXX_INCLUDE_TESTS": False,
         "LIBCXX_INCLUDE_DOCS": False,
         "LLVM_INCLUDE_TESTS": False,
         "LLVM_INCLUDE_TOOLS": True,
         "LLVM_BUILD_TOOLS": True,
         "LLVM_TOOL_LLVM_AR_BUILD": False,
         "LLVM_TOOL_LLVM_AS_BUILD": False,
         "LLVM_TOOL_LLVM_AS_FUZZER_BUILD": False,
         "LLVM_TOOL_LLVM_BUGPOINT_BUILD": False,
         "LLVM_TOOL_LLVM_BUGPOINT_PASSES_BUILD": False,
         "LLVM_TOOL_LLVM_BCANALYZER_BUILD": False,
         "LLVM_TOOL_LLVM_COV_BUILD": False,
         "LLVM_TOOL_LLVM_CXXDUMP_BUILD": False,
         "LLVM_TOOL_LLVM_DSYMUTIL_BUILD": False,
         "LLVM_TOOL_LLVM_LLC_BUILD": False,
         "LLVM_TOOL_LLVM_LLI_BUILD": False,
         "LLVM_TOOL_LLVM_DWARFDUMP_BUILD": False,
         "LLVM_TOOL_LLVM_DIS_BUILD": False,
         "LLVM_TOOL_LLVM_EXTRACT_BUILD": False,
         "LLVM_TOOL_LLVM_C_TEST_BUILD": False,
         "LLVM_TOOL_LLVM_DIFF_BUILD": False,
         "LLVM_TOOL_LLVM_GO_BUILD": False,
         "LLVM_TOOL_LLVM_JITLISTENER_BUILD": False,
         "LLVM_TOOL_LLVM_MCMARKUP_BUILD": False,
         "LLVM_TOOL_LLVM_MC_BUILD": False,
         "LLVM_TOOL_LLVM_MC_FUZZER_BUILD": False,
         "LLVM_TOOL_LLVM_NM_BUILD": False,
         "LLVM_TOOL_LLVM_OBJDUMP_BUILD": False,
         "LLVM_TOOL_LLVM_PDBDUMP_BUILD": False,
         "LLVM_TOOL_LLVM_PROFDATA_BUILD": False,
         "LLVM_TOOL_LLVM_RTDYLD_BUILD": False,
         "LLVM_TOOL_LLVM_SIZE_BUILD": False,
         "LLVM_TOOL_LLVM_SPLIT_BUILD": False,
         "LLVM_TOOL_LLVM_STRESS_BUILD": False,
         "LLVM_TOOL_LLVM_SYMBOLIZER_BUILD": False,
         "LLVM_TOOL_LLVM_LTO_BUILD": False,
         "LLVM_TOOL_LLVM_OBJ2YAML_BUILD": False,
         "LLVM_TOOL_LLVM_OPT_BUILD": False,
         "LLVM_TOOL_LLVM_SANCOV_BUILD": False,
         "LLVM_TOOL_LLVM_SANSTATS_BUILD": False,
         "LLVM_TOOL_LLVM_VERIFY_USELISTORDER_BUILD": False,
         "LLVM_TOOL_LLVM_XCODE_TOOLCHAIN_BUILD": False,
         "LLVM_TOOL_LLVM_YAML2OBJ_BUILD": False,
         "LLVM_INCLUDE_EXAMPLES": False,
         "LLVM_INCLUDE_GO_TESTS": False,
         "LLVM_BUILD_TESTS": False,
         "CMAKE_VERBOSE_MAKEFILE": True,
         "LLVM_TARGETS_TO_BUILD": "X86",
         "CMAKE_INSTALL_PREFIX": os.path.join(self.build_folder, INSTALL_DIR),
         "BUILD_SHARED_LIBS": self.options.shared if "shared" in self.options else False
        }, source_folder="src")
        cmake.build()
        cmake.install()

    def conan_info(self):
        self.info.settings.build_type = "Release"

    def package(self):
        self.copy(pattern="*",
                  dst="include",
                  src=os.path.join(INSTALL_DIR, "include"),
                  keep_path=True)
        for pattern in ["*.a", "*.h", "*.so", "*.lib", "*.dylib", "*.dll", "*.cmake"]:
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
