from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangFrontend(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_frontend'
    llvm_component = 'clang'
    llvm_module = 'Frontend'
    llvm_requires = ['clang_ast', 'clang_basic', 'clang_driver', 'clang_edit', 'clang_lex', 'clang_parse', 'clang_sema', 'clang_serialization', 'llvm_bit_reader', 'llvm_option', 'llvm_profile_data', 'llvm_support']
