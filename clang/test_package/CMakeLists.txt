PROJECT(ClangExample)
cmake_minimum_required(VERSION 3.0)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

CONAN_BASIC_SETUP()

find_package(LLVM REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)

message(STATUS "Found LLVM version: ${LLVM_PACKAGE_VERSION}")
message(STATUS "Found LLVMConfig.cmake in: ${LLVM_DIR}")

add_executable(libtooling_example libtooling.cpp)
add_executable(libclang_example libclang.cpp)

llvm_map_components_to_libnames(llvm_libs support core)
target_link_libraries(libtooling_example PRIVATE ${llvm_libs} clangTooling)
target_link_libraries(libclang_example PRIVATE libclang)
