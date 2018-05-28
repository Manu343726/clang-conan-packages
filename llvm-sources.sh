#!/bin/sh

set -e

COMPONENT=$1
VERSION=$2
URL=$3
TMP_DIR=`mktemp -d`
REPO="manu343726/llvm-sources"
PACKAGE="${REPO}/${COMPONENT}"
PACKAGE_RELEASE="${PACKAGE}/${VERSION}"

if which jfrog; then
    JFROG_CLI=`which jfrog`
elif [ -e ./jfrog ]; then
    JFROG_CLI="`pwd`/jfrog"
else
    JFROG_CLI_DIR=`mktemp -d`
    SRC_DIR=`pwd`
    cd $JFROG_CLI_DIR && $SRC_DIR/get_jfrog.sh && $SRC_DIR
    JFROG_CLI=$JFROG_CLI_DIR/jfrog
fi

wget $URL -P $TMP_DIR

if ! $JFROG_CLI bt package-show $PACKAGE; then
    echo package $PACKAGE not found, creating first
    $JFROG_CLI bt package-create $PACKAGE
fi

if ! $JFROG_CLI bt version-show $PACKAGE_RELEASE; then
    echo version $VERSION of $PACKAGE not found, creating first
    $JFROG_CLI bt version-create $PACKAGE_RELEASE
fi

$JFROG_CLI bt upload --publish --override $TMP_DIR/* ${REPO}/${COMPONENT}/${VERSION}
