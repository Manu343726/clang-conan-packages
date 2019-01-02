from conans import ConanFile, CMake
import conans.tools
import os, re

def replace_in_file(file, line_to_search, replace_with):
    with open(file, 'r') as input_file:
        input = input_file.read()

    output = re.sub(line_to_search, replace_with, input, flags=re.MULTILINE)

    if input == output:
        return False

    with open(file, 'w') as output_file:
        output_file.write(output)

    return True

class LLVMPackage(ConanFile):
    VERSION = '6.0.1'
    SOURCE_DIR = '.'
    BUILD_DIR = 'build'
    INSTALL_DIR = 'install'
    PARALLEL_BUILD = os.environ.get('CONAN_LLVM_SINGLE_THREAD_BUILD') is None

    version = os.environ.get("CONAN_VERSION_OVERRIDE", VERSION)
    license = 'BSD'
    url = 'https://gitlab.com/Manu343726/clang-conan-packages'
    generators = 'cmake', 'cmake_paths', 'cmake_find_package'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False],
        'sources_repo': 'ANY'
    }
    default_options = 'shared=False', 'sources_repo=https://dl.bintray.com/manu343726/llvm-sources'

    def configure(self):
        del self.settings.compiler.libcxx

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.shared

    @property
    def _llvm_component(self):
        return getattr(self, 'llvm_component', self.name)

    @property
    def source_package_name(self):
        return '{}-{}.src'.format(self._llvm_component, self.version)

    @property
    def _source_dir(self):
        return os.path.join(self.SOURCE_DIR, self.source_package_name)

    @property
    def _root_cmake_file(self):
        return os.path.join(self._source_dir, 'CMakeLists.txt')

    def _llvm_dependency_package(self, component):
        return '{}/{}@{}/{}'.format(component, self.version, self.user, self.channel)

    @property
    def _llvm_requires(self):
        return getattr(self, 'llvm_requires', [])

    def requirements(self):
        for component in self._llvm_requires:
            self.requires(self._llvm_dependency_package(component))

    def configure(self):
        for component in self._llvm_requires:
            self.options[component].shared = self._build_shared

    def source(self):
        self.output.info('Downloading {} sources package {} from {} ...'.format(self._llvm_component, self.source_package_name, self.options.sources_repo))
        url = '{}/{}.tar.gz'.format(self.options.sources_repo, self.source_package_name)
        conans.tools.get(url, destination=self.SOURCE_DIR)

        if self._llvm_requires:
            replace_in_file(self._root_cmake_file, r'project\((.+)\)',
r'''message(STATUS "Main {} CMakeLists.txt (${{CMAKE_CURRENT_LIST_DIR}}) patched by conan")
project(\1)
include("${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake")
conan_basic_setup()
list(APPEND CMAKE_PROGRAM_PATH ${{CONAN_BIN_DIRS}})
message(STATUS "CMAKE_PROGRAM_PATH: ${{CMAKE_PROGRAM_PATH}}")
'''.format(self.name))

    @property
    def _install_dir(self):
        return os.path.join(self.build_folder, self.INSTALL_DIR)

    @property
    def _install_include_dir(self):
        return os.path.join(self._install_dir, 'include')

    @property
    def _install_lib_dir(self):
        return os.path.join(self._install_dir, 'lib')

    @property
    def _install_bin_dir(self):
        return os.path.join(self._install_dir, 'bin')

    @property
    def _build_shared(self):
        return self.options.shared if 'shared' in self.options else False

    def build(self):
        llvm_cmake_options = [
            'INCLUDE_TESTS',
            'BUILD_TESTS',
            'INCLUDE_EXAMPLES',
            'BUILD_EXAMPLES',
            'INCLUDE_DOCS',
            'BUILD_TOOLS'
        ]

        cmake_options = {}

        for option in llvm_cmake_options:
            cmake_options['{}_{}'.format(self.name.upper(), option)] = False
            cmake_options['LLVM_' + option] = False


        self.output.info('Building LLVM package \'{}\' as shared libs: {}'.format(self.name, self._build_shared))

        cmake_options['CMAKE_INSTALL_PREFIX'] = self._install_dir
        cmake_options['CMAKE_VERBOSE_MAKEFILE'] = True
        cmake_options['BUILD_SHARED_LIBS'] = self._build_shared
        cmake_options['LLVM_TARGETS_TO_BUILD'] = 'X86'

        if hasattr(self, 'custom_cmake_options'):
            cmake_options.update(dict(self.custom_cmake_options))

        cmake = CMake(self, parallel=self.PARALLEL_BUILD)
        cmake.configure(defs=cmake_options, source_folder=self._source_dir)
        cmake.build()
        cmake.install()

    def package(self):
        self.output.info('Packaging LLVM component "{}". Copying from install dir {}'.format(self._llvm_component, self._install_dir))

        exclude_headers  = getattr(self, 'package_exclude_headers', None)
        exclude_libs     = getattr(self, 'package_exclude_libs', None)
        exclude_binaries = getattr(self, 'package_exclude_binaries', None)

        self.copy(pattern='*',
            excludes=exclude_headers,
            dst='include',
            src=self._install_include_dir,
            keep_path=True)

        for glob in ['*.a', '*.so*', '*.dll', '*.dylib', '*.cmake', '*.h']:
            self.copy(pattern=glob,
                excludes=exclude_libs,
                dst='lib',
                src=self._install_lib_dir,
                keep_path=True,
                symlinks=True)

        self.copy(pattern="*",
            excludes=exclude_binaries,
            dst="bin",
            src=self._install_bin_dir,
            keep_path=True)

        self.output.info('Packaging of LLVM component "{}" done'.format(self._llvm_component))

        if hasattr(self, 'after_package') and callable(self.after_package):
            self.output.info('Running after_package hook')
            self.after_package()

    def package_info(self):
        collected_libs = conans.tools.collect_libs(self)

        if hasattr(self, 'package_info_exclude_libs'):
            self.output.info('Filtering out libs {} from cpp_info.libs'.format(self.package_info_exclude_libs))
            self.cpp_info.libs = list(filter(lambda lib: not lib in self.package_info_exclude_libs, collected_libs))
        else:
            self.cpp_info.libs = collected_libs

        if self.settings.os == "Linux":
            self.cpp_info.libs.append('dl')
