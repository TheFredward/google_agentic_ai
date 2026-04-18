import os


def get_files_info(working_directory, directory=""):
    absolute_wrk_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_wrk_directory, directory))
    valid_target_dir = (
        os.path.commonpath([absolute_wrk_directory, target_dir])
        == absolute_wrk_directory
    )
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    if valid_target_dir:
        found_items_dir = []
        for item in os.listdir(target_dir):
            item_file_path = os.path.join(target_dir, item)
            found_items_dir.append(
                f"- {item}: file_size={os.path.getsize(item_file_path)}, is_dir={os.path.isdir(item_file_path)}"
            )
        return "\n".join(found_items_dir)
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
