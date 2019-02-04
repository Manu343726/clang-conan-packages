from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangExecs(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_executables'
    llvm_component = 'clang'
    llvm_module = 'clang'
    llvm_requires = []

    def package(self):
        self.copy_from_component('clang*', src='bin', dst='bin', keep_path=False)

    def package_info(self):
        self.cpp_info.libs = []
