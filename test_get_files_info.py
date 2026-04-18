from functions.get_files_info import get_files_info

result = get_files_info("calculator", ".")
print(result)
print("")
result = get_files_info("calculator", "pkg")
print(result)
print("")
result = get_files_info("calculator", "/bin")
print(result)
print("")
result = get_files_info("calculator", "../")
print(result)
print("")
