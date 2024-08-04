import subprocess
import argparse
import logging
from typing import Set

log_file = "brew_reinstall.log"

# Set up logging
logging.basicConfig(
    filename=log_file,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def get_installed_packages(cmd: str) -> Set[str]:
    """
    Retrieves a set of currently installed packages using the specified command.

    Args:
    cmd (str): The command to run to get the list of installed packages.

    Returns:
    Set[str]: A set of installed package names.
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return set(result.stdout.split())


def install_packages(
    list_file: str, install_cmd: str, type_name: str, installed_set: Set[str]
) -> None:
    """
    Installs packages from a specified list file if they are not already installed.

    Args:
    list_file (str): The file containing the list of packages to install.
    install_cmd (str): The command to use for installing a package.
    type_name (str): The type of packages being installed (e.g., 'cask', 'formula').
    installed_set (Set[str]): A set of already installed packages.
    """
    try:
        with open(list_file, "r") as f:
            packages = f.read().splitlines()
    except FileNotFoundError:
        logging.error(f"No {type_name} list file found.")
        return

    logging.info(f"Installing {type_name} packages from {list_file}...")
    for package in packages:
        if package in installed_set:
            logging.info(f"{package} is already installed.")
        else:
            logging.info(f"Installing {package}...")
            result = subprocess.run(
                f"{install_cmd} {package}", shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                logging.info(f"{package} installed successfully.")
            else:
                logging.error(f"Error installing {package}: {result.stderr}")


def verify_installation(type_name: str, list_cmd: str, list_file: str) -> None:
    """
    Verifies that all packages listed in a specified file are installed.

    Args:
    type_name (str): The type of packages being verified (e.g., 'cask', 'formula').
    list_cmd (str): The command to run to get the current list of installed packages.
    list_file (str): The file containing the list of packages to verify against.
    """
    logging.info(f"Verifying installed {type_name} packages...")
    current_packages = get_installed_packages(list_cmd)
    try:
        with open(list_file, "r") as f:
            expected_packages = set(f.read().splitlines())
    except FileNotFoundError:
        logging.error(f"No {type_name} list file found for verification.")
        return

    discrepancies = expected_packages - current_packages
    if discrepancies:
        logging.error(
            f"Discrepancies found in {type_name} package installation: {discrepancies}"
        )
    else:
        logging.info(f"All {type_name} packages are installed correctly.")


def main() -> None:
    """
    Main function that coordinates the reinstallation and verification of Homebrew packages.
    """
    parser = argparse.ArgumentParser(
        description="Reinstall Homebrew packages and verify installation."
    )
    parser.add_argument(
        "--cask-file", default="brew-cask.txt", help="Path to the cask list file"
    )
    parser.add_argument(
        "--formula-file",
        default="brew-formula.txt",
        help="Path to the formula list file",
    )
    parser.add_argument("--casks-only", action="store_true", help="Install only casks")
    parser.add_argument(
        "--formulas-only", action="store_true", help="Install only formulas"
    )
    args = parser.parse_args()

    # Get the current lists of installed casks and formulas
    installed_casks = get_installed_packages("brew list --cask")
    installed_formulas = get_installed_packages("brew list --formula")

    # Install casks and formulas based on arguments
    if args.casks_only:
        install_packages(args.cask_file, "brew install --cask", "cask", installed_casks)
        verify_installation("cask", "brew list --cask", args.cask_file)
    elif args.formulas_only:
        install_packages(
            args.formula_file, "brew install", "formula", installed_formulas
        )
        verify_installation("formula", "brew list --formula", args.formula_file)
    else:
        install_packages(args.cask_file, "brew install --cask", "cask", installed_casks)
        install_packages(
            args.formula_file, "brew install", "formula", installed_formulas
        )
        verify_installation("cask", "brew list --cask", args.cask_file)
        verify_installation("formula", "brew list --formula", args.formula_file)

    logging.info("Reinstallation complete!")


if __name__ == "__main__":
    main()
