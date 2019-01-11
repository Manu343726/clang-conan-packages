from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangEdit(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_edit'
    llvm_component = 'clang'
    llvm_module = 'Edit'
    llvm_requires = ['clang_headers', 'clang_ast', 'clang_basic', 'clang_lex', 'llvm_support']
