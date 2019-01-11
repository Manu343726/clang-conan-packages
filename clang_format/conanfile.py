from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangFormat(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_format'
    llvm_component = 'clang'
    llvm_module = 'Format'
    llvm_requires = ['clang_headers', 'clang_basic', 'clang_lex', 'clang_tooling_core', 'llvm_support']
