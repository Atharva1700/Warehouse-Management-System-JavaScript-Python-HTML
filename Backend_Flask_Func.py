from flask import Flask, render_template, request, jsonify, send_file
import barcode
from barcode.writer import ImageWriter
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
BARCODE_FOLDER = 'barcodes'
if not os.path.exists(BARCODE_FOLDER):
    os.makedirs(BARCODE_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-barcode', methods=['POST'])
def generate_barcode():
    try:
        data = request.json
        sku = data.get('sku')
        barcode_type = data.get('type', 'code128')
        
        # Validate SKU
        if not sku:
            return jsonify({'error': 'SKU is required'}), 400
        
        # Generate barcode
        barcode_class = barcode.get_barcode_class(barcode_type)
        barcode_instance = barcode_class(sku, writer=ImageWriter())
        
        # Save barcode
        filename = f"{sku}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filepath = os.path.join(BARCODE_FOLDER, filename)
        barcode_instance.save(filepath)
        
        return jsonify({
            'success': True,
            'sku': sku,
            'filepath': f"{filename}.png",
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-barcode/<filename>')
def get_barcode(filename):
    filepath = os.path.join(BARCODE_FOLDER, filename)
    return send_file(filepath, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, port=5000)