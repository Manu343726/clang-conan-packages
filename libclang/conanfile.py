from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class Libclang(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'libclang'
    llvm_component = 'clang'
    llvm_module = 'clang'
    library_name = 'libclang'
    llvm_requires = ['clang_ast', 'clang_basic', 'clang_frontend', 'clang_index', 'clang_lex', 'clang_sema', 'clang_tooling', 'clang_arc_migrate', 'llvm_x86_codegen', 'llvm_x86_asm_printer', 'llvm_x86_asm_parser', 'llvm_x86_desc', 'llvm_x86_info', 'llvm_support']
    include_dirs = ['clang-c']
