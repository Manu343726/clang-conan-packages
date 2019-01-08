from conans import ConanFile

from llvmpackage import *
from llvmcomponentpackage import *
from llvmmodulepackage import *

class LLVMCommon(ConanFile):
    name = 'llvm-common'
    version = '0.0.0'
    url = 'http://gitlab.com/Manu343726/clang-conan-packages'
    license = 'MIT'
    description = 'Common package recipes for LLVM packages'
    exports = '*.py'
