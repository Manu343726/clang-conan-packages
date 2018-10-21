from conans import ConanFile, CMake, tools
import shutil, os

DEFAULT_COMPILERRT_VERSION = "3.8.0"
CLANG_CONAN_TOOLS_VERSION = "0.3"

class CompilerRTConan(ConanFile):
    name = "compiler-rt"
    version = os.environ.get("CONAN_VERSION_OVERRIDE", DEFAULT_COMPILERRT_VERSION)
    generators = "cmake"
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

    def requirements(self):
        self._package_reference = "{}@{}/{}".format(self.version, self.user, self.channel)
        self.requires("llvm/" + self._package_reference)
        self.requires("clang_conan_tools/{}@{}/{}".format(os.environ.get("CLANG_CONAN_TOOLS_VERSION", CLANG_CONAN_TOOLS_VERSION), self.user, self.channel))

    def source(self):
        from common import get_sources
        get_sources("compiler-rt", CompilerRTConan.version,
                                        "compiler-rt")

    def build(self):
        from common import BUILD_DIR, INSTALL_DIR
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
                 "COMPILER_RT_BUILD_XRAY": False, # XRay cannot be built either, depends on lib/sanitizer_common
                 "CMAKE_INSTALL_PREFIX": os.path.join(self.build_folder, INSTALL_DIR),
                 "BUILD_SHARED_LIBS": self.options.shared if "shared" in self.options else False
                }, source_folder="compiler-rt")
                cmake.build()
                cmake.install()

    def package(self):
        import common
        common.package(self)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
