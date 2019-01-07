#!/bin/bash

# This scripts runs lddtree utility on all libraries packaged by a given LLVM component
# lddtree is part of pax-utils

LLVM_COMPONENT=$1
LLVM_VERSION=$2
CHANNEL=$3
PACKAGE_PATH=$HOME/.conan/data/$LLVM_COMPONENT/$LLVM_VERSION/$CHANNEL/package

if [[ ! -d "$PACKAGE_PATH" ]]; then
    echo "Package directory $#PACKAGE_PATH does not exist"
    return 1
fi

for lib in $(find "$PACKAGE_PATH" -name "*.so"); do
    echo lddtree $lib
    lddtree $lib
done
