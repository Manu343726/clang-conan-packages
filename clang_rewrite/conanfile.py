from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangRewrite(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_rewrite'
    llvm_component = 'clang'
    llvm_module = 'Rewrite'
    llvm_requires = ['clang_headers', 'clang_basic', 'clang_lex', 'llvm_support']
