from main import *

argv = ["--def_cstr_literals", "literals.txt",
        "-o", "source/cpp2.cpp",
        "source/cpp.cpp"
        ]  # sys.argv[1:]
main(argv)
