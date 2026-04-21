import argparse
import subprocess
import sys
import os
import shutil
import shlex

os.environ["IDF_TARGET"] = "esp32s3"

projects = ["Flash_Model", "Q_HUFDEL", "Check_Model"]

def main():
    parser = argparse.ArgumentParser(description="Run idf projects with selected model")
    parser.add_argument('-m', '--model', help='Model lenet: e.g., 513')
    parser.add_argument('--dry-run', action='store_true', help='Print commands without executing')
    args = parser.parse_args()

    root_dir = os.path.dirname(os.path.abspath(__file__))

    model = args.model
    if not model:
        try:
            model = input("Model lenet: (e.g., 513) ")
        except EOFError:
            print("No model provided and input not available. Use --model.")
            sys.exit(1)

    if not model:
        print("No model provided. Exiting.")
        sys.exit(1)

    # Determine idf command. For dry-run skip availability check.
    if args.dry_run:
        idf_cmd = 'idf.py'
    else:
        idf_cmd = None
        for candidate in ("idf.py", "idf"):
            if shutil.which(candidate):
                idf_cmd = candidate
                break

        if idf_cmd is None:
            print("Error: 'idf.py' not found in PATH.")
            print("Activate ESP-IDF environment (run export.bat/export.ps1) or add ESP-IDF tools to PATH.")
            sys.exit(1)

    for proj in projects:
        proj_path = os.path.join(root_dir, proj)
        print(f"\n=== Running {proj} with model {model} ===")

        cmd_build = [idf_cmd, '-C', proj_path, 'build', f'-DLENET_MODEL={model}', '-DDEMO_SCRIPT=1']
        cmd_flash = [idf_cmd, '-C', proj_path, 'flash']
        cmd_monitor = [idf_cmd, '-C', proj_path, 'monitor', '-b', '115200']

        if args.dry_run:
            def cmd_to_str(cmd_list):
                if os.name == 'nt':
                    return subprocess.list2cmdline(cmd_list)
                return ' '.join(shlex.quote(x) for x in cmd_list)

            print('DRY RUN:', cmd_to_str(cmd_build))
            print('DRY RUN:', cmd_to_str(cmd_flash))
            print('DRY RUN:', cmd_to_str(cmd_monitor))
            continue

        def cmd_to_str(cmd_list):
            if os.name == 'nt':
                return subprocess.list2cmdline(cmd_list)
            return ' '.join(shlex.quote(x) for x in cmd_list)

        def run_command(cmd_list, check=False):
            # On Windows use the shell so file associations (py->python) work
            # properly. On POSIX run the list form directly.
            if os.name == 'nt':
                cmd_str = subprocess.list2cmdline(cmd_list)
                return subprocess.run(cmd_str, shell=True, check=check)
            return subprocess.run(cmd_list, check=check)

        try:
            run_command(cmd_build, check=True)
            run_command(cmd_flash, check=True)
            print("Monitoring serial output...")
            run_command(cmd_monitor, check=False)
        except subprocess.CalledProcessError as e:
            print(f"Command failed for project {proj}: {e}")
            sys.exit(e.returncode)
        except FileNotFoundError as e:
            print(f"Failed to run command: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()