from pathlib import Path
from subprocess import run
import os


def build_app():
    # define and create pyinstaller output path
    pyinstaller_folder = Path(Path(__file__).parent / "pyinstaller_build")
    pyinstaller_folder.mkdir(exist_ok=True)

    # define paths before changing directory
    script = Path(Path.cwd() / "autoqpf-cli.py")
    icon_path = Path(Path.cwd() / "autoqpf.ico")

    # change directory so we output all of pyinstallers files in it's own folder
    os.chdir(pyinstaller_folder)

    # run pyinstaller command
    build_job = run(
        [
            "pyinstaller",
            "-n",
            "autoqpf-cli",
            "--onefile",
            f"--icon={str(icon_path)}",
            str(script),
        ]
    )

    # ensure output of exe
    success = "Did not complete successfully"
    if (
        Path(Path("dist") / "autoqpf-cli").is_file()
        and str(build_job.returncode) == "0"
    ):
        success = f'\nSuccess!\nPath to executable: {str(Path.cwd() / (Path(Path("dist") / "autoqpf-cli")))}'

    # change directory back to original directory
    os.chdir(script.parent)

    # return success message
    return success


if __name__ == "__main__":
    build = build_app()
    print(build)
