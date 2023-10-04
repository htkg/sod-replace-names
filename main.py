import json, time, random, sys, argparse, os
import brotli
import logging

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(
    prog="Shadows of Doubt",
    description="Change civilian names to custom names.\nPlease provide file path to .citb or .cit file and file path to .txt or .csv file containing names that you want see in the game.",
    epilog="Github: @htkg",
)

parser.add_argument("cities_fp", help="Filepath of city to modify")
parser.add_argument("names_fp", help="Filepath to .csv containing names to use")
parser.add_argument("delimiter", help="(Only CSV applicable) Delimiter of the names file. Default is ;", default=";", nargs="?")

args = parser.parse_args()

# Check if the filepaths are valid
if not os.path.isfile(args.cities_fp):
    logging.error(
        f'"{args.cities_fp}" is not a valid cities filepath. It should be full or relative path to the .citb or .cit file. It could be found in C:\\Users\\...\\AppData\\LocalLow\\ColePowered Games\\Shadows of Doubt\\Cities'
    )
    sys.exit()
elif not os.path.isfile(args.names_fp):
    logging.error(
        f'"{args.names_fp}" is not a valid names filepath. File should be in .txt or .csv format.'
    )
    sys.exit()


# Read the cities file
def read_cities_file(cities_fp):
    ts_start = time.time()
    if cities_fp.endswith(".citb"):
        with open(args.cities_fp, "rb") as f:
            cities_file = json.loads(brotli.decompress(f.read()).decode("utf-8"))
        return cities_file, time.time() - ts_start
    if cities_fp.endswith(".cit"):
        with open(args.cities_fp, "r", encoding="utf-8") as f:
            cities_file = json.load(f)
        return cities_file, time.time() - ts_start
    else:
        logging.error("Cities file must be in .citb or .cit format")
        sys.exit()

def read_names_file(names_fp):
    # get format of the file
    file_format = names_fp.split(".")[-1]
    if file_format not in ["txt", "csv"]:
        logging.error(
            "Names file must be in .txt or .csv format and contain one fullname per line where first word is the first name and last word is the last name."
        )
        sys.exit()

    if file_format == "txt":
        with open(names_fp, "r", encoding="utf-8") as f:
            # create a list from \n
            lines = [line.strip() for line in f.readlines()]
            lines = [line for line in lines if line]

        return lines
    elif file_format == "csv": # delimited by ;
        import csv
        lines = []
        with open(names_fp, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                # join row elements into a single string (fullname)
                full_name = ' '.join(row).strip()
                # make sure the line is not empty or just a delimiter
                if full_name and len(row) > 1:
                    lines.append(full_name)
        return lines


def parse_name(fullname):
    start = fullname.find("'")
    if start != -1:  # Nickname found
        end = fullname.find("'", start + 1)
        if end != -1:  # Closing quotation is found
            nickname = fullname[start+1 : end].strip()
            fullname_without_nickname = ' '.join((fullname[:start] + fullname[end+1:]).split())
        else:
            fullname_without_nickname = fullname.strip()
            nickname = None
    else:
        fullname_without_nickname = fullname.strip()
        nickname = None

    fullname_parts = fullname_without_nickname.split(' ')

    if len(fullname_parts) > 1:
        first_name = fullname_parts[0].strip()
        last_name = ' '.join(fullname_parts[1:]).strip()
    else:
        first_name = fullname_without_nickname.strip()
        last_name = None

    return fullname_without_nickname, first_name, last_name, nickname


logging.info("Reading city file...")
cities_file, time_exec = read_cities_file(args.cities_fp)
logging.debug(f"Finished reading {args.cities_fp} in {time_exec:.2f} seconds.")
logging.info("Reading names file...")

names = read_names_file(args.names_fp)
citizens = cities_file["citizens"]

logging.info(f"Got {len(citizens)} citizens and {len(names)} names.")

def get_names_sample_by_len(custom_names, cit_len):
    """This function solves case if there are more custom names than citizens.

    For example, custom names file has only 32 names and city have 512 citizens. Every custom name would be used.
    For example 2, custom names file has 512 names and city have 32 citizens. Only 32 names would be used.

    Args:
        custom_names (list): List of custom names
        cit_len (int): Length of the citizens list

    Returns:
        list: Sample of custom names
    """

    min_length = min(cit_len, len(custom_names)) 
    sample = random.sample(custom_names, min_length)

    if min_length != len(custom_names):
        logging.warning(f"Using {min_length} custom names out of {len(custom_names)} available because there are only {cit_len} citizens in the city file.")
        
    return sample


custom_names_sample = get_names_sample_by_len(names, len(citizens))

def get_new_names(custom_names, citizens):
    """This function creates a dictionary of new names.

    Args:
        custom_names (list): List of custom names
        citizens (list): List of citizens

    Returns:
        dict: Dictionary of new names
    """

    new_names = {}
    for i, citizen in enumerate(citizens):
        if i >= len(custom_names):
            break
        new_names[citizen["humanID"]] = custom_names[i]

    return new_names

new_names = get_new_names(custom_names_sample, citizens)


confirmation_msg = input(f"{len(new_names)} civilians out of {len(citizens)} citizens would be changed. Rest will be the same.\nAre you sure you want to change names? (Y/n): ").strip().lower()
if confirmation_msg not in ["y", "yes", "", " "]:
    logging.info("Exiting...")
    sys.exit()
    
logging.info("Changing names...")
for citizen in citizens:
    if citizen["humanID"] in new_names.keys():
        new_name = new_names[citizen["humanID"]]
        fullname, first_name, last_name, nickname = parse_name(new_name)
        
        if not first_name or not last_name:
            logging.warning(f"Skipping {fullname} because it does not have a first name or last name. Please make sure that your names file is in the correct format. Each citizen have a name and surname. Nickname is optional and specified like: Alex 'nickname' Smith")
            continue
        
        citizen["firstName"] = first_name
        citizen["surName"] = last_name
        citizen["casualName"] = nickname if nickname else ''
        citizen["citizenName"] = fullname
        logging.info(f"Changed #{citizen['humanID']} to {fullname} (Firstname: {first_name} | Surname: {last_name}) (Nick: {nickname})")

city_filename = os.path.basename(args.cities_fp)

# create folder output if not exists
if not os.path.exists("output"):
    os.makedirs("output")

with open(os.path.join("output", city_filename), "wb") as f:
    if city_filename.endswith(".citb"):
        logging.info("Compressing... This could take up to 5 minutes.")
        json_dump = json.dumps(cities_file).encode("utf-8")
        bytes_file = brotli.compress(json_dump, quality=7)
    elif city_filename.endswith(".cit"):
        logging.info("Encoding...")
        bytes_file = json.dumps(cities_file).encode("utf-8")

    logging.info(f"Saving {city_filename} to output folder...")
    f.write(bytes_file)
    print(f"\nDone! Saved to the current folder: output/{city_filename}. Please backup your original file before replacing it. Remember: save games in the game refer to the filename of the city file. Please do not rename the file. New file should have exact filename as original file.\n\nMove output/{city_filename} to C:\\Users\\...\\AppData\\LocalLow\\ColePowered Games\\Shadows of Doubt\\Cities")