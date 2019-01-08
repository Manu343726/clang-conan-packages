from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMProfileData(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_profile_data'
    llvm_component = 'llvm'
    llvm_module = 'ProfileData'
    llvm_requires = ['llvm_core', 'llvm_support']
