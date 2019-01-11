from llvmpackage import LLVMPackage
from conans import tools
import os

class LLVMModulePackage(LLVMPackage):
    version = LLVMPackage.version

    @property
    def _header_only(self):
        return getattr(self, 'header_only', False)

    def build_requirements(self):
        if not hasattr(self, 'llvm_component'):
            raise RuntimeError('LLVM Module package {} has no associated base LLVM component set'.format(self.name))

        if not self._header_only and not hasattr(self, 'llvm_module'):
            raise RuntimeError('LLVM Module package {} has not associtated {} module set'.format(self.name, self.llvm_component))

        self.build_requires(self._llvm_dependency_package(self.llvm_component))

    def configure(self):
        super().configure()

        self.output.info("Requiring llvm base component dependency '{}' as shared library: {}".format(self.llvm_component, self._build_shared))
        self.options[self.llvm_component].shared = self._build_shared
        self.options[self.llvm_component].sources_repo = self.options.sources_repo

    def package(self):
        if not self._header_only:
            component_lib_dir = os.path.join(self.deps_cpp_info[self.llvm_component].rootpath, 'lib')
            self.output.info('Packaging {} library files, imported from {} package lib dir (\"{}\")'.format(self.name, self.llvm_component, component_lib_dir))

            if hasattr(self, 'library_name'):
                self.output.info('Copying library file by given name "{}"'.format(self.library_name))
                lib_globs = ['*{}.*'.format(self.library_name)]
            else:
                lib_globs = [
                    '*{}{}.*'.format(self.llvm_component.lower(), self.llvm_module),
                    '*{}{}.*'.format(self.llvm_component.upper(), self.llvm_module)
                ]

            for lib_glob in lib_globs:
                self.copy(lib_glob,
                    src=component_lib_dir,
                    dst='lib',
                    keep_path=False)

        if self._header_only:
            if not hasattr(self, 'include_dirs'):
                self.include_dirs = [os.path.join(self.llvm_component, self.llvm_module)]

            for include_dir in self.include_dirs:
                self.output.info('Packaging headers from \"{}\"'.format(include_dir))
                self.copy('*',
                    src=os.path.join(self.deps_cpp_info[self.llvm_component].rootpath, 'include', include_dir),
                    dst=os.path.join('include', include_dir))

    def package_id(self):
        if self._header_only:
            self.info.header_only()

    def package_info(self):
        if not self._header_only:
            self.cpp_info.libs = tools.collect_libs(self)
