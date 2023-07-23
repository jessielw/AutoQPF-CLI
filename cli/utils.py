import argparse
import glob
from pathlib import Path


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    """Custom help formatter for argparse that modifies the format of action invocations.

    Inherits from argparse.RawTextHelpFormatter and overrides the _format_action_invocation method.
    This formatter adds a comma after each option string, and removes the default metavar from the
    args string of optional arguments that have no explicit metavar specified.

    Attributes:
        max_help_position (int): The maximum starting column for the help string.
        width (int): The width of the help string.

    Methods:
        _format_action_invocation(action): Overrides the method in RawTextHelpFormatter.
            Modifies the format of action invocations by adding a comma after each option string
            and removing the default metavar from the args string of optional arguments that have
            no explicit metavar specified. Returns the modified string."""

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)

        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)

        option_strings = ", ".join(action.option_strings)
        return f"{option_strings}, {args_string}"


class FileParser:
    def parse_input_s(self, args_list: list):
        """
        Parse the input arguments and return a list of Path objects representing the input files.

        Args:
            args_list (list): List of input arguments.

        Returns:
            list: List of Path objects representing the input files.

        Raises:
            FileNotFoundError: If an input path is not a valid file path.
        """
        input_s = []

        # check for nested directories
        args_list = self._get_files_from_directory(args_list)

        # find all files
        for arg_input in args_list:
            arg_input = str(arg_input)
            # non recursive
            if "*" in arg_input:
                input_s.extend(Path(p) for p in glob.glob(arg_input))

            # recursive search
            elif "**" in arg_input:
                input_s.extend(Path(p) for p in glob.glob(arg_input, recursive=True))

            # single file path
            elif (
                Path(arg_input).exists()
                and Path(arg_input).is_file()
                and arg_input.strip() != ""
            ):
                input_s.append(Path(arg_input))
            else:
                raise FileNotFoundError(f"{arg_input} is not a valid input path.")

        return input_s

    @staticmethod
    def _get_files_from_directory(file_s: list):
        file_s_list = []
        for input_file in file_s:
            input_file = Path(input_file)
            if input_file.is_dir():
                for find_file in input_file.rglob("*"):
                    if find_file.is_file():
                        file_s_list.append(find_file)
            elif input_file.is_file():
                file_s_list.append(input_file)
        return file_s_list


def fps_type(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            raise argparse.ArgumentTypeError("FPS must be a valid integer or float.")
