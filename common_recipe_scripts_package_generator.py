#!/usr/bin/python
import argparse, os, shutil

def generate_test(args, recipe_dir):
    os.mkdir(os.path.join(recipe_dir, "test_package"))
    with open(os.path.join(recipe_dir, "test_package", "conanfile.py"), "w") as conanfile:
        conanfile.write("""
from conans import ConanFile, tools
import sys, os

def check_syspath():
    package_found = False

    for path in sys.path:
        if "{package}" in path and os.path.isfile(os.path.join(path, "__init__.py")):
            package_found = True
            break

    if not package_found:
        raise Exception("Package {package} not found in python module path")


class {package_class}ConanTestFile(ConanFile):
    def source(self):
        check_syspath()

    def build(self):
        check_syspath()

    def test(self):
        check_syspath()
""".format(package=args.package, version=args.version, user=args.user, channel=args.channel,
    package_class=args.package.replace("-", "_")))


def generate_recipe(args, recipe_dir):
    with open(os.path.join(recipe_dir, "conanfile.py"), "w") as conanfile:
        conanfile.write("""
from conans import ConanFile
import os

class {package_class}ConanFile(ConanFile):
    name = "{package}"
    version = "{version}"
    description = "Common recipe scripts for {package} module"
    url = "{url}"
    license = "MIT"
    exports = "{package}/*.py"
    build_policy = "missing"
    generators = "virtualenv"

    def package(self):
        self.copy("*.py")

    def package_info(self):
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "{package}"))
""".format(package=args.package, version=args.version, url=args.url,
    package_class=args.package.replace("-", "_")))



def setup_recipe(args):
    # Create directory for the recipe
    recipe_dir = "conan_recipe_" + args.package
    os.mkdir(recipe_dir)
    module_dir = os.path.join(recipe_dir, args.package)

    # Copy the python module tree into the recipe dir
    shutil.copytree(src=args.package, dst=module_dir)

    return recipe_dir


parser = argparse.ArgumentParser(description="conan.io recipe generator for python recipe scripts packages")
parser.add_argument("package")
parser.add_argument("version")
parser.add_argument("user")
parser.add_argument("channel")
parser.add_argument("--with-test", action="store_true")
parser.add_argument("--url", default="https://gitlab.com/Manu343726/clang-conan-packages")
args = parser.parse_args()

recipe_dir = setup_recipe(args)
generate_recipe(args, recipe_dir)

if args.with_test:
    generate_test(args, recipe_dir)

print(recipe_dir)
