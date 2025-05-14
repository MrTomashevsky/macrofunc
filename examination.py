from main import *

argv = ["--def_cstr_literals", "literals.txt",
        # "-o", "source/cpp2.cpp",
        "source/cpp.cpp"
        ]  # sys.argv[1:]
main(argv)


# from MacroWorkWithVariables import *

# print(create__IS_WORD__()(" hels"))

# from MacroWorkWithVariables import TmpWriteFile

# import time
# with TmpWriteFile("t.txt", ["hello", "world"]) as tf:
#     time.sleep(5)
#     print(tf.file.writelines(["h", "l"]))
#     tf.file.flush()

#     time.sleep(5)
