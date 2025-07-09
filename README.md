# PDF Verification

This project provides tools for PDF verification.

## Installation

1. Install [uv](https://github.com/astral-sh/uv):

    ```sh
    curl -Ls https://astral.sh/uv/install.sh | sh
    ```

## Running the PDF Script

To run the `pdf` script defined in `pyproject.toml`, use:

```sh
uv pip run pdf --pdf_path ./path/to/gnarly_data.pdf
```

Refer to `pyproject.toml` for script details.

## Getting a PDF

Visit: https://www.faa.gov/air_traffic/weather/asos, select the state you're interested in, download as PDF, select "specific sheets from this view", unselect "Map Layer", choose "Weather Station Table", then download.
