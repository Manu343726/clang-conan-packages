from conans import python_requires
llvm_common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMConan(llvm_common.LLVMPackage):
    name = "llvm"
    version = llvm_common.LLVMPackage.version
    requires = 'gtest/1.8.1@bincrafters/stable'

    custom_cmake_options = {
        'LLVM_BUILD_TOOLS': True
    }
    package_info_exclude_libs = [
        'BugpointPasses', 'LLVMHello', 'LTO'
    ]
