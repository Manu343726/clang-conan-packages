from conans import python_requires
import os
llvm_common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangConan(llvm_common.LLVMPackage):
    name = "clang"
    version = llvm_common.LLVMPackage.version
    llvm_requires = ['llvm', 'compiler-rt']
    llvm_component = 'cfe'
    custom_cmake_options = {
        'CLANG_BUILD_TOOLS': True,
        'LLVM_ENABLE_PIC': False
    }
    package_exclude_libs = ['libclang.so*']

    def build(self):
        self.custom_cmake_options['LIBCLANG_BUILD_STATIC'] = not self._build_shared

        super().build()

    def package(self):
        super().package()

        if not self._build_shared:
            self.copy(
                pattern='libclang.a',
                src=os.path.join(self.build_folder, 'lib'),
                dst='lib',
                keep_path = False)

            clang_targets_file = os.path.join(self._install_lib_dir, 'cmake', 'clang', 'ClangTargets.cmake')
            clang_target_properties_file = os.path.join(self._install_lib_dir, 'cmake', 'clang', 'ClangTargets-{}.cmake'.format(str(self.settings.build_type).lower()))

            self.output.info('Patching Clang cmake scripts to import static libclang')

            if not llvm_common.replace_in_file(clang_targets_file,
                    r'add_library\(libclang SHARED IMPORTED\)',
r'''add_library(libclang STATIC IMPORTED)
set_target_properties(libclang PROPERTIES INTERFACE_LINK_LIBRARIES
    clangAST
    clangBasic
    clangFrontend
    clangIndex
    clangLex
    clangSema
    clangTooling
    LLVMCore
    LLVMSupport)'''):
                self.output.warn('No SHARED -> STATIC replacement of IMPORT libclang library done!')

            if not llvm_common.replace_in_file(clang_target_properties_file,
                r'IMPORTED_SONAME_{} "${{_IMPORT_PREFIX}}/lib/libclang.so((\.[0-9]+)*)"'.format(str(self.settings.build_type).upper()),
                r''):
                self.output.warn('No IMPORT_SONAME_<BUILD TYPE> libclang IMPORTED target property found!')

            if not llvm_common.replace_in_file(clang_target_properties_file,
                    r'libclang.so((\.[0-9]+)*)', 'libclang.a'):
                self.output.warn('No libclang.so.xxx references found!')

    def package_info(self):
        super().package_info()

        if self._build_shared:
            self.cpp_info.libs.append('libclang')
