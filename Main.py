import subprocess
import re
import os

# Function to print a cool-looking banner
def print_banner():
    banner = """
    ***************************************
    *                                     *
    *      WELCOME TO DVD ENCODER CLI     *
    *                                     *
    ***************************************
    """
    print(banner)

# Function to find HandBrakeCLI.exe in the same directory as the script
def get_handbrake_path():
    # Get the directory of the current script or executable
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to HandBrakeCLI.exe
    handbrake_path = os.path.join(script_dir, 'HandBrakeCLI.exe')
    return handbrake_path

# Function to run HandBrakeCLI and list all titles
def scan_dvd_titles(dvd_drive):
    try:
        # Get the HandBrakeCLI path
        handbrake_path = get_handbrake_path()

        # Inform the user that the DVD scan is in progress
        print(f"Scanning DVD titles from {dvd_drive}, please wait...")

        # Run HandBrakeCLI command to scan the DVD and capture output
        result = subprocess.run([handbrake_path, '--input', f'\\\\.\\{dvd_drive}', '--title', '0', '--scan'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='latin1')

        # Extract and format the title and duration using regular expressions
        titles = []
        title_pattern = re.compile(r'\+ title (\d+):')
        duration_pattern = re.compile(r'\+ duration: (\d{2}:\d{2}:\d{2})')

        lines = result.stdout.splitlines()
        current_title = None
        
        for line in lines:
            # Find title numbers
            title_match = title_pattern.search(line)
            if title_match:
                current_title = title_match.group(1)

            # Find durations
            if current_title:
                duration_match = duration_pattern.search(line)
                if duration_match:
                    titles.append((current_title, duration_match.group(1)))
                    current_title = None  # Reset after processing

        # If titles are found, print them
        if titles:
            print("Available DVD Titles and Durations:")
            for title, duration in titles:
                print(f"Title {title}: {duration}")
        else:
            print("No titles found.")
            
        return titles

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to encode selected titles
def encode_title(dvd_drive, output_dir, title_num):
    try:
        # Get the HandBrakeCLI path
        handbrake_path = get_handbrake_path()

        output_file = f"{output_dir}/output_title_{title_num}.mp4"
        print(f"Encoding Title {title_num} from {dvd_drive}...")

        # HandBrakeCLI encoding command
        subprocess.run([
            handbrake_path, '-i', f'\\\\.\\{dvd_drive}', '-o', output_file,
            '-e', 'x264', '-q', '23', '--title', title_num,
            '--width', '720', '--height', '576', '--rate', '25',
            '--pfr', '--decomb', '--audio', '1', '--aencoder', 'copy',
            '--mixdown', 'stereo', '--arate', '48', '--ab', '192',
            '--format', 'av_mp4', '--encoder-preset', 'veryfast',
            '--encoder-level', '4.1', '--optimize', '--crop', '0:0:0:0'
        ])

        print(f"Title {title_num} encoding complete. Saved to {output_file}")

    except Exception as e:
        print(f"An error occurred while encoding Title {title_num}: {e}")

# Main function to handle encoding flow
def main():
    # Display a cool-looking banner
    print_banner()

    # Get DVD source drive and output directory first
    dvd_drive = input("Enter the DVD drive letter (e.g., E): ").strip().upper()
    output_dir = input("Enter the target directory to save encoded files (e.g., Z:/Videos): ").strip()

    # Ask whether to store drive and output directory for reuse
    store_values = input("Do you want to store the source DVD drive and target directory for reuse during this session? (yes/no): ").strip().lower()

    # Initialize variables to store drive and target directory if the user chooses to store them
    stored_dvd_drive = dvd_drive if store_values == 'yes' else None
    stored_output_dir = output_dir if store_values == 'yes' else None

    while True:
        # Use stored values if available, otherwise ask again for each loop
        if stored_dvd_drive is None or stored_output_dir is None:
            dvd_drive = input("Enter the DVD drive letter (e.g., E): ").strip().upper()
            output_dir = input("Enter the target directory to save encoded files (e.g., Z:/Videos): ").strip()

        # Scan for titles
        titles = scan_dvd_titles(dvd_drive)

        # If titles are found, prompt user to select titles for encoding
        if titles:
            while True:
                title_nums = input("Enter the title numbers you want to encode, separated by commas (e.g., 14,15): ")
                selected_titles = [t.strip() for t in title_nums.split(',') if t.strip()]

                # Encode selected titles
                for title_num in selected_titles:
                    encode_title(dvd_drive, output_dir, title_num)

                # Ask if the user wants to encode another title from the same DVD
                another_title = input("Do you want to encode another title from this DVD? (yes/no): ").strip().lower()
                if another_title == 'yes':
                    # Rescan the DVD and display the titles again
                    titles = scan_dvd_titles(dvd_drive)
                else:
                    # Ask if they want to use stored values or enter new ones after completing current DVD
                    if stored_dvd_drive and stored_output_dir:
                        reuse_values = input("Do you want to reuse the stored drive and target directory? (yes/no): ").strip().lower()
                        if reuse_values == 'no':
                            # Reset stored values and prompt for new ones
                            stored_dvd_drive = None
                            stored_output_dir = None
                            dvd_drive = input("Enter the new DVD drive letter (e.g., E): ").strip().upper()
                            output_dir = input("Enter the new target directory to save encoded files (e.g., Z:/Videos): ").strip()
                            break
                    else:
                        break

        # Ask if the user wants to encode titles from another DVD
        another_dvd = input("Do you want to encode titles from a new DVD? (yes/no): ").strip().lower()
        if another_dvd == 'yes':
            continue
        else:
            print("Exiting script. All encoding complete.")
            break

if __name__ == "__main__":
    main()

