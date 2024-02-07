import sys
import argparse
from pathlib import Path

from auto_qpf.qpf_exceptions import (
    ChapterIndexError,
    ImproperChapterError,
    NoChapterDataError,
)

from cli.utils import CustomHelpFormatter, FileParser, fps_type
from cli._version import __version__, program_name
from cli.process import process_args, create_stax_rip_directory
from cli.exit import _exit_application, exit_fail, exit_success


def qpf_cli(dropped=False):
    # Top-level parser
    parser = argparse.ArgumentParser(
        prog=program_name, formatter_class=CustomHelpFormatter
    )

    # Add a global -v flag
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # common args
    parser.add_argument(
        "-i",
        "--input",
        nargs="+",
        help="Input file paths or directories",
        metavar="INPUT",
        required=False,
    )
    parser.add_argument(
        "-s",
        "--staxrip-batch",
        action="store_true",
        help="If used, will auto create StaxRip temp directories with proper QPF files inside.",
    )
    parser.add_argument(
        "-f",
        "--fps",
        type=fps_type,
        default=23.976,
        help="Define source file FPS.",
    )
    parser.add_argument(
        "-a",
        "--auto-fps",
        action="store_true",
        help="If used, will over ride any user fps input if the input file is a media file.",
    )
    parser.add_argument(
        "-c",
        "--chapter-chunks",
        type=float,
        default=5.0,
        help="If chapters are generated, sets the percentage of total duration they will be created for.",
    )    
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output file path. Output will be put alongside input.",
    )
    #############################################################
    ######################### Execute ###########################
    #############################################################
    # check if a file or directory was dropped on the exe
    if dropped:
        args, _ = parser.parse_known_args()
        setattr(args, "input", [dropped])
        if any(Path(i).is_dir() for i in [dropped]):
            setattr(args, "staxrip_batch", True)

    # if not parse args like normally
    else:
        args = parser.parse_args()

    arg_list = [arg for arg in vars(args).values()]
    if all(arg is False or arg is None or arg == 23.976 for arg in arg_list):
        if not hasattr(args, "version"):
            parser.print_usage()
            _exit_application("", exit_fail)

    if not args.input:
        _exit_application("No input was provided.", exit_fail)

    file_inputs = FileParser().parse_input_s(args.input)

    if not file_inputs:
        _exit_application("No input files we're found.", exit_fail)

    # if input was provided
    files_processed = 0
    for file_input in file_inputs:
        if args.staxrip_batch:
            # create staxrip dir
            file_output = create_stax_rip_directory(file_input)
        else:
            if args.output:
                file_output = Path(args.output)
            else:
                file_output = Path(file_input).with_suffix(".qpf")
            
        # ensure directories are made
        file_output.parent.mkdir(parents=True, exist_ok=True)

        try:
            process_arguments = process_args(
                file_input=file_input,
                file_output=file_output,
                fps=args.fps,
                auto_detect_fps=args.auto_fps,
                chapter_chunks=args.chapter_chunks,
            )
            print(f"QPF Created: {process_arguments}")
            files_processed = files_processed + 1
        except ChapterIndexError:
            _exit_application(
                "Issue getting the correct index from the chapters", exit_fail
            )

        except ImproperChapterError:
            _exit_application("Input has improper or corrupted chapters", exit_fail)

        except NoChapterDataError:
            _exit_application("Input has no chapter data", exit_fail)

    _exit_application(f"Total files processed: {files_processed}", exit_success)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Drag and drop a directory/media-file/ogm file or run this in a terminal and use '-h' for commands usage."
        )
        input()
    elif len(sys.argv) >= 2:
        # Check if a file was dropped on the CLI, if so run a default set of commands,
        # if not continue like normal
        file_or_dir = Path(sys.argv[1])
        if file_or_dir.is_file() or file_or_dir.is_dir():
            qpf_cli(dropped=file_or_dir)
        else:
            qpf_cli()
    else:
        _exit_application("Use 'AutoQPF-CLI -h' to see a list of commands", exit_fail)
