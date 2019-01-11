from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangSerialization(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_serialization'
    llvm_component = 'clang'
    llvm_module = 'Serialization'
    llvm_requires = ['clang_headers', 'clang_ast', 'clang_basic', 'clang_lex', 'clang_sema', 'llvm_bit_reader', 'llvm_support']
