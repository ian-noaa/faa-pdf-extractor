import pdfplumber
import pandas as pd
import argparse
import re

def extract_pdf_values():
    parser = argparse.ArgumentParser(description="Extract weather station data from a PDF.")
    parser.add_argument("--pdf_path", required=True, help="Path to the PDF file")
    args = parser.parse_args()

    pdf_path = args.pdf_path

    # We'll collect structured rows from here
    lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract the raw text and split into lines
            text = page.extract_text()
            if text:
                lines.extend(text.split('\n'))

    # Display first 30 lines to analyze structure and line joining needs
    # print(lines[:30])

    # Define pattern to match each line
    pattern = re.compile(
        r"(?P<ID>K[A-Z0-9]{3})?\s*"
        r"(?P<LocationCountyState>.*?)\s+"
        r"Colorado\s+"
        r"(?P<Frequency>[A-Z\-\/.\d\s]+)\s+"
        r"\((?P<AreaCode>\d{3})\)\s(?P<PhoneNumber>\d{3}-\d{4})\s+"
        r"(?P<Type>AWOS-\dP?T?|ASOS)"
    )

    records = []

    for line in lines:
        match = pattern.search(line)
        if match:
            id_ = match.group("ID") or ""
            loc_county_state = match.group("LocationCountyState").strip()
            # Split into location and county by assuming last two words before 'Colorado' are county
            parts = loc_county_state.split()
            if len(parts) >= 2:
                county = parts[-1]
                location = " ".join(parts[:-1])
            else:
                location = loc_county_state
                county = ""

            # Assemble the row
            records.append({
                "ID": id_.strip(),
                "Location": location.strip(),
                "County": county.strip(),
                "State": "Colorado",
                "Frequency": match.group("Frequency").strip(),
                "Phone": f"({match.group('AreaCode')}) {match.group('PhoneNumber')}",
                "Type": match.group("Type").strip()
            })

    # Create DataFrame
    df_clean = pd.DataFrame(records)
    print(df_clean)

if __name__ == "__main__":
    extract_pdf_values()
