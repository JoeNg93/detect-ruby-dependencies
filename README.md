# This project is used to get all the dependencies of a Ruby project and save it to a file

# Features:
  + Support either a path to project or a Git repo link
  + Detect both external dependencies and internal dependencies

## File structure:
  + **parse_ruby_project.py**: Main script, see the usage below
  + **test_parse_ruby_project.py**: Several test cases for the script

## Usage:
  + Run the script: **$python3 parse_ruby_project.py [path_to_project_or_git_link]**
  + Run test case: **$python3 test_parse_ruby_project.py**


## Output:

**Result will be saved to:**

```
[project_name]_internal_deps.list (internal dependencies)
[project_name]_external_deps.list (external dependencies)
```

**Contents of output:**

```
[source_path]:[dependency_path]:[type_of_require]
```

**Example:**

*project_internal_deps.list*:

```
/project/a.rb:/project/b.rb:require_internal
```

*project_external_deps.list*
```
/project/a.rb:/External/my_external.rb:require_external
```

## Limitation:

As far as I'm concerned, there are several ways to require a dependency in Ruby. This project is not a perfect implementation.

For example, it cannot detect dependencies from **Rails** project (since Rails use another file to automatically import all the deps from Gemfile)
