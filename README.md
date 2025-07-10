# PDF Verification

This project provides tools to extract data from FAA-provided ASOS/AWOS PDFs.

## Installation

1. Install [uv](https://github.com/astral-sh/uv):

    ```sh
    curl -Ls https://astral.sh/uv/install.sh | sh
    ```

## Running the PDF Script

To run the `extract_pdfs` script defined in `pyproject.toml`, use:

```sh
uv run extract_pdfs --pdf_dir path/to/pdfs/ --output_csv output.csv
```

Refer to `pyproject.toml` for script details.

## Getting a PDF

1. Visit: https://www.faa.gov/air_traffic/weather/asos
2. select the state you're interested in on the map
3. download as PDF
4. select "specific sheets from this view"
5. unselect "Map Layer"
6. choose "Weather Station Table"
7. then download.

## Warnings

1. The data in the PDFs appears to be incomplete or malformed in some cases. E.g. Station ID's are truncated like `KCP..` for the Wolf Creek Pass station in Colorado.
2. This has only been tested on Colorado data. There may be data permutations in other States or Territories that this doesn't properly handle.

Until the data source improves, the data will need to be manually verified.

Ideally, the FAA would provide this data in a clean format. If not, we could try to set up a webscraper frontend to fetch the PDFs & extract the data on a regular interval.
