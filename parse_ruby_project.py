import os
import sys
import re


# Various patterns needed
class RegexPattern:
    git_pattern = re.compile(
        r"^(https:\/\/github\.com\/|git@github\.com:)[a-zA-Z0-9]+\/(.*)\.git$")
    dependency_pattern = re.compile(r"^\s*require.*['|\"](.*)['|\"]")


def main():
    try:
        path_name = sys.argv[1]
    except IndexError:  # User doesnt enter a path to file or repo
        print("Error: Please enter either a project folder or a Git repo")
        print(
            "Usage: python3 parse_ruby_project.py [project_folder_or_git_repo]")
        print("Script terminated")
        return
    if is_valid_git_link(path_name):
        os.system("git clone {}".format(path_name))
        path_name = RegexPattern.git_pattern.match(path_name).group(2)

    if not os.path.exists(path_name):
        print("Error: Path is not exist or invalid")
        print("Script terminated")
        return
    print()
    ruby_files = get_ruby_files_from_root_folder(path_name)
    root_folder = os.path.basename(os.path.abspath(
        path_name))  # In case path_name is relative
    internal_deps_file = open("{}_internal_deps.list".format(root_folder), "w")
    external_deps_file = open("{}_external_deps.list".format(root_folder), "w")
    print("Successful: Generated {} and {}. Please check the output".format(
        internal_deps_file.name, external_deps_file.name))
    for file in ruby_files:
        deps = get_deps_from_ruby_file(file)
        source_path = file[file.index(root_folder) - 1:]
        for dep in deps:
            if dep in ruby_files:
                # -1 to take the leading slash "/"
                dep_path = dep[dep.index(root_folder) - 1:]
                internal_deps_file.write(
                    ":".join([source_path, dep_path, "require_internal"]))
                internal_deps_file.write("\n")
            else:
                dep_path = "/External/" + os.path.basename(dep)
                external_deps_file.write(
                    ":".join([source_path, dep_path, "require_external"]))
                external_deps_file.write("\n")
    internal_deps_file.close()
    external_deps_file.close()


def is_valid_git_link(link_path):
    return bool(RegexPattern.git_pattern.match(link_path))


def get_ruby_files_from_root_folder(folder_name):
    ruby_files = []
    for current_dir, dirs, files in os.walk(folder_name):
        files_with_path = map(lambda file: os.path.abspath(
            os.path.join(current_dir, file)), files)
        ruby_files.extend(get_ruby_files_from_list(files_with_path))
    return ruby_files


def get_ruby_files_from_list(file_list):
    return [file for file in file_list if is_ruby_file(file)]


def is_ruby_file(file_name):
    return file_name.endswith(".rb")


def get_deps_from_ruby_file(file_name):
    if not is_ruby_file(file_name):
        raise ValueError("Not Ruby file!")
    dependencies = []
    for line in open(file_name):
        x = RegexPattern.dependency_pattern.match(line)
        if x:
            dependency_name = x.group(1)
            if not dependency_name.endswith(".rb"):
                dependency_name += ".rb"
            deps_path = os.path.join(
                os.path.dirname(file_name), dependency_name)
            dependencies.append(os.path.abspath(deps_path))
    return dependencies


if __name__ == "__main__":
    main()
