from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(visual_runtimes=["MT", "MD"])

    if platform.system() == "Windows":
        builder.add_common_builds(visual_versions=[12])

    if platform.system() == "Linux":
        for ver in ["4.8", "4.9", "5.2", "5.3"]:
            for arch in ["x86", "x86_64"]:
                for libcxx in ["libstdc++", "libstdc++11"]:
                    builder.add({"arch": arch,
                                 "build_type": "Release",
                                 "compiler": "gcc",
                                 "compiler.version": ver,
                                 "compiler.libcxx": libcxx},
                                 {})

    if platform.system() == "Darwin":
        for compiler_version in ["5.0", "5.1", "6.0", "6.1", "7.0"]:
            for arch in ["x86", "x86_64"]:
                for build_type in ["Release"]:
                    builder.add({"arch": arch,
                                 "build_type": build_type,
                                 "compiler": "apple-clang",
                                 "compiler.version": compiler_version}, {})
    builder.run()
