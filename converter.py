"""
CSV Converter for Intesa SanPaolo bank exports to Actual Budget format.
"""

import csv
import io
from typing import TextIO, Union


# Number of metadata rows to skip in Intesa SanPaolo CSV exports
METADATA_ROWS_TO_SKIP = 19

# Input column names (Italian)
INPUT_COLUMNS = {
    'date': 'Data',
    'payee': 'Operazione',
    'notes': 'Dettagli',
    'amount': 'Importo',
}

# Output column names (English - Actual Budget format)
OUTPUT_COLUMNS = ['Account', 'Date', 'Payee', 'Notes', 'Category', 'Amount', 'Split_Amount', 'Cleared']

# Fixed account name for output
ACCOUNT_NAME = 'Intesa SanPaolo'


def transform_csv(input_file: Union[str, TextIO], output_file: Union[str, TextIO, None] = None) -> str:
    """
    Transform an Intesa SanPaolo CSV export to Actual Budget format.
    
    Args:
        input_file: Path to input CSV file or file-like object
        output_file: Path to output CSV file or file-like object (optional)
    
    Returns:
        The transformed CSV content as a string
    """
    # Handle input
    if isinstance(input_file, str):
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = input_file.read()
        if isinstance(content, bytes):
            content = content.decode('utf-8')
    
    # Split into lines and skip metadata rows
    lines = content.splitlines()
    
    # Find the header row (contains "Data,Operazione,Dettagli")
    header_row_index = None
    for i, line in enumerate(lines):
        if 'Data' in line and 'Operazione' in line and 'Dettagli' in line:
            header_row_index = i
            break
    
    if header_row_index is None:
        raise ValueError("Could not find header row in input CSV")
    
    # Parse CSV starting from header row
    csv_content = '\n'.join(lines[header_row_index:])
    reader = csv.DictReader(io.StringIO(csv_content))
    
    # Transform rows
    output_buffer = io.StringIO()
    writer = csv.DictWriter(output_buffer, fieldnames=OUTPUT_COLUMNS)
    writer.writeheader()
    
    for row in reader:
        output_row = {
            'Account': ACCOUNT_NAME,
            'Date': row.get(INPUT_COLUMNS['date'], ''),
            'Payee': row.get(INPUT_COLUMNS['payee'], ''),
            'Notes': row.get(INPUT_COLUMNS['notes'], ''),
            'Category': '',  # Left empty as per specification
            'Amount': row.get(INPUT_COLUMNS['amount'], ''),
            'Split_Amount': '',  # Left empty as per specification
            'Cleared': '',  # Left empty as per specification
        }
        writer.writerow(output_row)
    
    result = output_buffer.getvalue()
    
    # Write to output file if specified
    if output_file is not None:
        if isinstance(output_file, str):
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                f.write(result)
        else:
            output_file.write(result)
    
    return result


def main():
    """CLI entry point for the converter."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python converter.py <input.csv> [output.csv]")
        print("\nTransforms Intesa SanPaolo CSV exports to Actual Budget format.")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = transform_csv(input_path, output_path)
        
        if output_path:
            print(f"Converted successfully! Output saved to: {output_path}")
        else:
            print(result)
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
