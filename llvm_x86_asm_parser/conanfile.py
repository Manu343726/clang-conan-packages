from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMX86AsmParser(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_x86_asm_parser'
    llvm_component = 'llvm'
    llvm_module = 'X86AsmParser'
    llvm_requires = ['llvm_mc', 'llvm_support', 'llvm_x86_utils']
