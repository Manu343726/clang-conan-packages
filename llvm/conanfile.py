from conans import ConanFile, CMake
import shutil, os

DEFAULT_LLVM_VERSION = "3.8.0"
CLANG_CONAN_TOOLS_VERSION = "0.3"

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
         "LLVM_BUILD_TESTS": False,
         "LLVM_INCLUDE_EXAMPLES": False,
         "LLVM_BUILD_EXAMPLES": False,
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
        import common
        common.package(self)
