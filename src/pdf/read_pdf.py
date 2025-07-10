import argparse
import re
from pathlib import Path

import pandas as pd
import pdfplumber


def extract_pdf_values():
    parser = argparse.ArgumentParser(
        description="Extract weather station data from PDF files."
    )
    parser.add_argument(
        "--pdf_dir", required=True, help="Path to the directory containing PDF files"
    )
    parser.add_argument(
        "--output_csv", required=True, help="Path to the output CSV file"
    )
    args = parser.parse_args()

    pdf_dir = Path(args.pdf_dir)
    output_csv = Path(args.output_csv)

    # Check if directory exists
    if not pdf_dir.exists() or not pdf_dir.is_dir():
        print(f"Error: Directory {pdf_dir} does not exist or is not a directory")
        return

    # Find all PDF files in the directory
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in directory {pdf_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files to process")

    # Define pattern to match each line - only extract ID and Type
    pattern = re.compile(
        r"(?P<ID>K[A-Z0-9]{3})?\s*"  # TODO - some station IDs are malformed in the source PDFS. E.g. - KCP..WolfCreekPass & etc...
        r".*?"  # Match everything in between
        r"(?P<Station_Type>AWOS-\dP?T?|ASOS)"  # TODO - Are there any other permutations in other states?
    )

    all_records = []

    # Process each PDF file
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        # We'll collect structured rows from here
        lines = []

        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    # Extract the raw text and split into lines
                    text = page.extract_text()
                    if text:
                        lines.extend(text.split("\n"))

            # Process lines from this PDF
            for line in lines:
                match = pattern.search(line)
                if match:
                    station_id = match.group("ID") or ""
                    station_type = match.group("Station_Type").strip()

                    # Only include records that have both ID and Type
                    if station_id and station_type:
                        all_records.append(
                            {
                                "Station_ID": station_id.strip(),
                                "Station_Type": station_type,
                                "Source_File": pdf_file.name,
                            }
                        )

        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
            continue

    # Create DataFrame from all records
    df_clean = pd.DataFrame(all_records)

    if df_clean.empty:
        print("No weather station data found in any PDF files")
        return

    # Remove duplicates based on Station_ID (keep first occurrence)
    df_clean = df_clean.drop_duplicates(subset=["Station_ID"], keep="first")

    print(f"Total records found: {len(df_clean)}")
    print(df_clean.head())

    # Save to CSV
    df_clean.to_csv(output_csv, index=False)
    print(f"Results saved to: {output_csv}")


if __name__ == "__main__":
    extract_pdf_values()
