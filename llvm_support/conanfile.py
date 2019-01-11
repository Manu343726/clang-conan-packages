from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMSupport(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_support'
    llvm_component = 'llvm'
    llvm_module = 'Support'
    llvm_requires = ['llvm_headers', 'llvm_demangle']

    def package_info(self):
        super().package_info()
        self.cpp_info.libs.append('pthread')
        self.cpp_info.libs.append('dl')
        self.cpp_info.libs.append('z')
        self.cpp_info.libs.append('tinfo')
