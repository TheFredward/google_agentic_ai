from functions.write_file import write_file


def test():
    result = write_file("calculator", "lorem.txt", "waitn this isn't lorem ipsum")
    print(result)
    print("")
    result = write_file("calculator", "pkg/mrelorem.txt", "lorem ipsum dolor sit amet")
    print(result)
    print("")
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)
    print("")


if __file__:
    test()
