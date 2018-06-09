from conans import ConanFile, CMake
import shutil, os

DEFAULT_CLANG_VERSION = "3.8.0"
CLANG_CONAN_TOOLS_VERSION = "0.3"

class ClangConan(ConanFile):
    name = "clang"
    version = os.environ.get("CONAN_VERSION_OVERRIDE", DEFAULT_CLANG_VERSION)
    generators = "cmake"
    url = "http://gitlab.com/Manu343726/clang-conan"
    license = "BSD"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "extra_tools": [True, False]}
    default_options = "shared=True", "extra_tools=True"

    def configure(self):
        del self.settings.compiler.libcxx

        if "shared" in self.options:
            self.options["llvm"].shared = self.options.shared
            self.options["compiler-rt"].shared = self.options.shared
            self.options["libcxx"].shared = self.options.shared

    def requirements(self):
        self._package_reference = "{}@{}/{}".format(self.version, self.user, self.channel)

        self.requires("llvm/" + self._package_reference)
        self.requires("compiler-rt/" + self._package_reference)
        self.requires("clang_conan_tools/{}@{}/{}".format(os.environ.get("CLANG_CONAN_TOOLS_VERSION", CLANG_CONAN_TOOLS_VERSION), self.user, self.channel))

        if self.settings.compiler != "Visual Studio":
            self.requires("libcxx/" + self._package_reference)


    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared
            self.options.extra_tools = False

    def source(self):
        from common import get_sources
        get_sources("cfe", ClangConan.version,
                                        "clang")

        if self.options.extra_tools:
            get_sources("clang-tools-extra", ClangConan.version,
                                            "clang/tools/extra")

    def build(self):
        from common import BUILD_DIR, INSTALL_DIR
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
        import common
        common.package(self)

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
