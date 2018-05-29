#!/bin/sh

set -e

COMPONENT=$1
VERSION=$2
URL=$3
TMP_DIR=`mktemp -d`
REPO="manu343726/llvm-sources"
PACKAGE="${REPO}/${COMPONENT}"
PACKAGE_RELEASE="${PACKAGE}/${VERSION}"
SRC_DIR=`pwd`

if which jfrog; then
    JFROG_CLI=`which jfrog`
elif [ -e ./jfrog ]; then
    JFROG_CLI="`pwd`/jfrog"
else
    JFROG_CLI_DIR=`mktemp -d`
    cd $JFROG_CLI_DIR && $SRC_DIR/get_jfrog.sh && $SRC_DIR
    JFROG_CLI=$JFROG_CLI_DIR/jfrog
fi

wget $URL -P $TMP_DIR
cd $TMP_DIR
FILENAME=`ls $TMP_DIR`
FILENAME_WE="${FILENAME%.*}"
ZIP_FILE="${FILENAME_WE}.gz"
xz -d $FILENAME

if [ ! -f $FILENAME_WE ]; then
    echo Extracted file FILENAME_WE not found!
    exit 1
fi

gzip -1 $FILENAME_WE

if [ ! -f $ZIP_FILE ]; then
    echo gzipped file $ZIP_FILE not found!
    exit 2
fi

if ! $JFROG_CLI bt package-show $PACKAGE; then
    echo package $PACKAGE not found, creating first
    $JFROG_CLI bt package-create $PACKAGE
fi

if ! $JFROG_CLI bt version-show $PACKAGE_RELEASE; then
    echo version $VERSION of $PACKAGE not found, creating first
    $JFROG_CLI bt version-create $PACKAGE_RELEASE
fi

$JFROG_CLI bt upload --publish --override $TMP_DIR/${ZIP_FILE} ${REPO}/${COMPONENT}/${VERSION}
