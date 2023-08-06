#!/usr/bin/python3
"""
Creates project structure for a python project installable as a module
"""
import argparse
import os
from string import Template


def main():
    """
    CLI Tool entry point
    """
    parser = argparse.ArgumentParser(
        description="Creates project structure for a python package")

    parser.add_argument("module_name", type=str, help="Name for python module")
    parser.add_argument("--path",
                        default=".",
                        help="Directory path to build project structure")
    parser.add_argument("--direnv",
                        action='store_true',
                        help="Create direnv config file")
    parser.add_argument("--virtualenv",
                        action='store_true',
                        help="Create virtualenv for module project directory")

    args = parser.parse_args()
    project_dir = os.path.join(args.path, args.module_name)
    os.mkdir(project_dir)
    os.mkdir(os.path.join(project_dir, "src"))
    module_dir = os.path.join(project_dir, "src", args.module_name)
    os.mkdir(module_dir)
    open(os.path.join(module_dir, "__init__.py"), 'w').close()
    setup_path = os.path.join(project_dir, "setup.py")

    if args.virtualenv:
        # create a virtual env in the root dir
        env_path = "{}/env".format(project_dir)
        os.system("python3 -m venv " + env_path)
    if args.direnv:
        with open(os.path.join(args.module_name, ".envrc"), "w") as f:
            if args.virtualenv:
                f.write("source env/bin/activate")

    (cwd, this_file) = os.path.split(__file__)
    template_path = os.path.join(cwd, "data", "setup.template")
    with open(template_path, 'r') as setup_template_file:
        setup_template = Template(setup_template_file.read())
        setup_py = setup_template.substitute(module=args.module_name)
        with open(setup_path, 'w') as setup_py_file:
            setup_py_file.write(setup_py)


if __name__ == "__main__":

    main()
