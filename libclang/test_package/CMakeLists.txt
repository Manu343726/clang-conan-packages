PROJECT(ClangExample)
cmake_minimum_required(VERSION 3.0)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

CONAN_BASIC_SETUP(TARGETS)

add_executable(libclang_example libclang.cpp)

target_link_libraries(libclang_example PRIVATE CONAN_PKG::libclang)
