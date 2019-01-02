from conans import python_requires
llvm_common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class CompilerRTConan(llvm_common.LLVMPackage):
    name = "compiler-rt"
    version = llvm_common.LLVMPackage.version
    llvm_requires = ['llvm']
    custom_cmake_options = {
        'COMPILER_RT_BUILD_SANITIZERS': False,
        'COMPILER_RT_BUILD_XRAY': False
    }
