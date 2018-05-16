from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager(visual_runtimes=["MT", "MD"])
    builder.add_common_builds()
    builder.run()
