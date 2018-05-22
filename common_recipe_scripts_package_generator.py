#!/usr/bin/python
import argparse, os

def generate_test(args):
    os.mkdir(os.path.join(args.package, "test_package"))
    with open(os.path.join(args.package, "test_package", "conanfile.py"), "w") as conanfile:
        conanfile.write("""
from conans import ConanFile, tools

class {package_class}ConanTestFile(ConanFile):
    def source(self):
	with tools.pythonpath(self):
	    import {package_class}

    def build(self):
	with tools.pythonpath(self):
	    import {package_class}

    def test(self):
        pass
""".format(package=args.package, version=args.version, user=args.user, channel=args.channel,
    package_class=args.package.replace("-", "_")))


def generate_recipe(args):
    with open(os.path.join(args.package, "conanfile.py"), "w") as conanfile:
        conanfile.write("""
from conans import ConanFile

class {package_class}ConanFile(ConanFile):
    name = "{package}"
    version = "{version}"
    description = "Common recipe scripts for {package} module"
    url = "{url}"
    license = "MIT"
    exports = "*"
    build_policy = "missing"
    generators = "virtualenv"

    def package(self):
        self.copy("*.py")

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
""".format(package=args.package, version=args.version, url=args.url,
    package_class=args.package.replace("-", "_")))


parser = argparse.ArgumentParser(description="conan.io recipe generator for python recipe scripts packages")
parser.add_argument("package")
parser.add_argument("version")
parser.add_argument("user")
parser.add_argument("channel")
parser.add_argument("--with-test", action="store_true")
parser.add_argument("--url", default="https://gitlab.com/Manu343726/clang-conan-packages")
args = parser.parse_args()

generate_recipe(args)

if args.with_test:
    generate_test(args)
