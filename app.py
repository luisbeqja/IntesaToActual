"""
Flask web application for CSV conversion.
"""

import io
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from converter import transform_csv

app = Flask(__name__)
app.secret_key = 'intesa-to-actual-secret-key'

ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload and return the transformed file."""
    # Check if file was uploaded
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Validate file extension
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a CSV file.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Transform the CSV
        result = transform_csv(file)
        
        # Create output filename
        original_name = file.filename.rsplit('.', 1)[0]
        output_filename = f"{original_name}_converted.csv"
        
        # Return the transformed file as download
        output_buffer = io.BytesIO(result.encode('utf-8'))
        output_buffer.seek(0)
        
        return send_file(
            output_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name=output_filename
        )
    
    except ValueError as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An unexpected error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
