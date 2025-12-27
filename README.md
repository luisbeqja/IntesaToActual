# Intesa to Actual

A simple tool to convert Intesa SanPaolo bank CSV/XLSX exports into a format compatible with [Actual Budget](https://actualbudget.org).

## Features

- Web UI with drag-and-drop file upload
- Supports both CSV and XLSX file formats
- Automatic column mapping from Italian to English
- Instant download of converted file
- CLI support for batch processing

## Installation

```bash
# Clone the repository
cd IntesaToActual

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Web Interface

Start the web server:

```bash
python app.py
```

Open your browser to [http://localhost:5000](http://localhost:5000) and upload your CSV or XLSX file.

### Command Line

```bash
# Output to stdout
python converter.py input.csv

# Save to file (works with both CSV and XLSX)
python converter.py input.xlsx output.csv
```

## Column Mapping

| Intesa SanPaolo (Input) | Actual Budget (Output) |
|-------------------------|------------------------|
| Data                    | Date                   |
| Operazione              | Payee                  |
| Dettagli                | Notes                  |
| Importo                 | Amount                 |
| —                       | Account (= "Intesa SanPaolo") |
| —                       | Category (empty)       |
| —                       | Split_Amount (empty)   |
| —                       | Cleared (empty)        |

## How It Works

1. The converter skips the metadata rows at the top of Intesa SanPaolo exports
2. Finds the header row containing transaction data
3. Maps the Italian column names to the Actual Budget format
4. Outputs a clean CSV ready for import

## License

MIT
