from conans import ConanFile, CMake, tools
import shutil, os
from distutils.version import LooseVersion

DEFAULT_LLVM_VERSION = "3.8.0"
CLANG_CONAN_TOOLS_VERSION = "0.3"
PARALLEL_BUILD=os.environ.get("CONAN_LLVM_SINGLE_THREAD_BUILD") is None

class LLVMConan(ConanFile):
    name = "llvm"
    version = os.environ.get("CONAN_VERSION_OVERRIDE", DEFAULT_LLVM_VERSION)
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

    def requirements(self):
        self.requires("clang_conan_tools/{}@{}/{}".format(os.environ.get("CLANG_CONAN_TOOLS_VERSION", CLANG_CONAN_TOOLS_VERSION), self.user, self.channel))

    def source(self):
        from common import get_sources
        get_sources("llvm", LLVMConan.version, "src")

    def build(self):
        from common import INSTALL_DIR, BUILD_DIR
        cmake = CMake(self, parallel=PARALLEL_BUILD)
        try:
            os.makedirs(INSTALL_DIR)
        except OSError:
            pass

        try:
            shutil.rmtree(BUILD_DIR)
        except OSError:
            pass

        cmake.configure(defs={
         "LLVM_INCLUDE_TESTS": True,
         "LLVM_BUILD_TESTS": True,
         "LLVM_INCLUDE_EXAMPLES": False,
         "LLVM_BUILD_EXAMPLES": False,
         "LLVM_INCLUDE_TOOLS": True,
         "LLVM_BUILD_TOOLS": True,
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
        import common
        common.package(self)

    def package_info(self):
        self.cpp_info.libs = list(filter(
            lambda lib: not lib in ['BugpointPasses', 'LLVMHello'],
            tools.collect_libs(self)))
