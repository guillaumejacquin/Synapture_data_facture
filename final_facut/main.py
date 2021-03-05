from pdf_info import *


def main():
    arg = "test/test1.pdf"
    values = (parse_type_file(arg))
    
    arg_json = arg + ".json"
    f = open(arg_json, "a")
    f.write(str(values))

    print(values)

main()

