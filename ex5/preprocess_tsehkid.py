import csv
import re

# Define input and output files
input_csv = "ex5/tshekid_office2003.csv"  # Update with actual path
output_csv = "ex5/input1.txt"  # Output with customer IDs retained and duplicates allowed

# Character replacement mapping (NO underscores, just removal)
char_map = str.maketrans({
    "õ": "6", "ä": "a", "ö": "o", "ü": "u",
    "Õ": "6", "Ä": "A", "Ö": "O", "Ü": "U",
    '"': '',  # Remove double quotes
    "'": '',  # Remove single quotes
    "-": '',  # Remove hyphens
    "/": '',  # Remove slashes
    ".": '',  # Remove dots
})

def clean_item_name(item):
    """Cleans item names by removing special characters and spaces."""
    item = item.strip().translate(char_map)  # Replace special characters
    item = re.sub(r'[\s.\-"/]+', '', item)  # Remove spaces, dots, slashes, quotes
    return item.strip()  # Final strip for safety

def process_csv_for_apriori_with_duplicates(input_csv, output_csv):
    """Processes CSV file, adjusting customer IDs when they reset and allowing duplicate items."""
    transactions = {}
    current_offset = 0
    last_customer_id = 0

    try:
        with open(input_csv, "r", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            next(reader)  # Skip header

            for row in reader:
                if len(row) < 2 or not row[1].strip():
                    continue  # Skip empty rows

                try:
                    customer_id = int(row[0])
                except ValueError:
                    print(f"Skipping invalid row: {row}")
                    continue

                # If the customer ID decreases, it's a reset; increment offset
                if customer_id < last_customer_id:
                    current_offset += 100

                adjusted_customer_id = customer_id + current_offset
                item = clean_item_name(row[1])  # Clean item name

                if adjusted_customer_id not in transactions:
                    transactions[adjusted_customer_id] = []

                transactions[adjusted_customer_id].append(item)  # Allow duplicates

                last_customer_id = customer_id

        # Write Apriori-ready transactions to output file
        with open(output_csv, "w", encoding="utf-8", newline="") as outfile:
            for customer_id, items in transactions.items():
                cleaned_items = [clean_item_name(item) for item in items]  # Extra cleaning
                cleaned_items = [item for item in cleaned_items if item]  # Remove empty strings
                cleaned_line = f"{customer_id}," + ",".join(cleaned_items)  # Build line manually
                cleaned_line = cleaned_line.strip().rstrip(',')  # Remove trailing spaces/commas
                outfile.write(cleaned_line + "\n")  # Write line to file

        print(f"✅ Apriori-compatible data saved to '{output_csv}' with NO weird characters.")

    except Exception as e:
        print(f"❌ Error processing file '{input_csv}': {e}")

# Run the script
process_csv_for_apriori_with_duplicates(input_csv, output_csv)
