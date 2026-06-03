import csv
import json
import sys
from pathlib import Path


def convert_csv(input_file, output_file):
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        print(f"Error: {input_file} not found")
        return

    with open(input_path, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        with open(output_path, "w", encoding="utf-8") as json_file:
            json_file.write("[\n")

            first = True

            for row in reader:
                if not first:
                    json_file.write(",\n")

                json.dump(row, json_file, indent=4)

                first = False

            json_file.write("\n]")

    print(f"Successfully created {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("python csv_to_json.py <input.csv> <output.json>")
        sys.exit(1)

    convert_csv(sys.argv[1], sys.argv[2])