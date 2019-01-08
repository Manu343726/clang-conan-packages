from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangARCMigrate(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_arc_migrate'
    llvm_component = 'clang'
    llvm_module = 'ARCMigrate'
    llvm_requires = ['clang_ast', 'clang_analysis', 'clang_basic', 'clang_edit', 'clang_frontend', 'clang_lex', 'clang_rewrite', 'clang_sema', 'clang_serialization', 'clang_static_analyzer_checkers', 'llvm_support']
