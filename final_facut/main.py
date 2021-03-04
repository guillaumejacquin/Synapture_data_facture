from pdf_info import *


def main():
    arg = "alaid.png"
    values = (parse_type_file(arg))
    
    arg_json = arg + ".json"
    f = open(arg_json, "a")
    f.write(str(values))

    print(values)

main()

