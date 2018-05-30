from conans import ConanFile, CMake
import shutil, os

DEFAULT_LIBCXX_VERSION = "3.8.0"
CLANG_CONAN_TOOLS_VERSION = "0.1"

class LibCxxConan(ConanFile):
    name = "libcxx"
    version = os.environ.get("CONAN_VERSION_OVERRIDE", DEFAULT_LIBCXX_VERSION)
    generators = "cmake"
    url = "http://github.com/Manu343726/libcxx-conan"
    license = "BSD"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"

    def configure(self):
        del self.settings.compiler.libcxx

        if "shared" in self.options:
            self.options["llvm"].shared = self.options.shared

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

    def requirements(self):
        self._package_reference = "{}@{}/{}".format(self.version, self.user, self.channel)
        self.requires("llvm/" + self._package_reference)
        self.requires("clang_conan_tools/{}@{}/{}".format(os.environ.get("CLANG_CONAN_TOOLS_VERSION", CLANG_CONAN_TOOLS_VERSION), self.user, self.channel))

    def source(self):
        from common import get_sources
        from conans.tools import download, patch
        get_sources("libcxx", LibCxxConan.version,
                                        "libcxx")

        download("https://github.com/llvm-mirror/libcxx/commit/6e02e89f65ca1ca1d6ce30fbc557563164dd327e.patch", "missing_glibc_xlocale.patch")
        patch(base_path="libcxx", patch_file="missing_glibc_xlocale.patch")

    def build(self):
        from common import BUILD_DIR, INSTALL_DIR
        cmake = CMake(self)

        for component in ["libcxx"]:
            build = os.path.join(BUILD_DIR, component)
            install = os.path.join(INSTALL_DIR, component)
            try:
                os.makedirs(install)
            except OSError:
                pass

            if not os.path.exists(os.path.join(self.source_folder,
                                               component,
                                               "CMakeListsOriginal.txt")):
                shutil.move(os.path.join(self.source_folder,
                                         component,
                                         "CMakeLists.txt"),
                            os.path.join(self.source_folder,
                                         component,
                                         "CMakeListsOriginal"))
                with open(os.path.join(self.source_folder,
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

            try:
                shutil.rmtree(build)
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
         "LLVM_INCLUDE_EXAMPLES": False,
         "LLVM_INCLUDE_GO_TESTS": False,
         "LLVM_BUILD_TESTS": False,
         "CMAKE_VERBOSE_MAKEFILE": True,
         "LLVM_TARGETS_TO_BUILD": "X86",
         "CMAKE_INSTALL_PREFIX": os.path.join(self.build_folder, INSTALL_DIR),
         "BUILD_SHARED_LIBS": self.options.shared if "shared" in self.options else False
        }, source_folder="libcxx")

        cmake.build()
        cmake.install()

    def package(self):
        from common import INSTALL_DIR
        for component in ["libcxx"]:
            install = os.path.join(INSTALL_DIR, component)
            self.copy(pattern="*",
                      dst="include",
                      src=os.path.join(install, "include"),
                      keep_path=True)
           for pattern in ["*.a*", "*.h", "*.so*", "*.lib", "*.dylib*", "*.dll*", "*.cmake"]:
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
