#define __STDC_CONSTANT_MACROS
#define __STDC_LIMIT_MACROS

#include "clang/Tooling/Tooling.h"
#include "clang/Tooling/CommonOptionsParser.h"

using namespace clang::tooling;

static llvm::cl::OptionCategory MyToolCategory("my-tool-options");

int main(int argc, const char **argv) {
    CommonOptionsParser parser(argc, argv, MyToolCategory, llvm::cl::ZeroOrMore);
    return 0;
}