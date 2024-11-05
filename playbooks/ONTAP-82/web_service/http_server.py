#!/usr/bin/env python3
from flask import Flask, request, render_template, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

# In-memory storage for demonstration purposes
received_data_bluecorp = []
event_summary_bluecorp = {}
received_data_astrainc = []
event_summary_astrainc = {}
received_data_polarisltd = []
event_summary_polarisltd = {}

# Namespace for xml parsing
namespaces = {'ns0': 'http://www.netapp.com/filer/admin'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ntap_svm_bluecorp', methods=['POST'])
def receive_data_bluecorp():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        root = ET.fromstring(xml_data)  # Parse the XML data
        received_data_bluecorp.append(ET.tostring(root, encoding='utf8', method='xml'))

        # count volume event occurances
        vol_element = root.find('.//ns0:parameter[ns0:name="volumeName"]/ns0:value', namespaces)
        # Extract the text from the volumeName element if it exists
        if vol_element is not None:
            vol_name = vol_element.text
            # Increment the count for this volume in the dictionary
            event_summary_bluecorp[vol_name] = event_summary_bluecorp.get(vol_name, 0) + 1

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415

@app.route('/ntap_svm_astrainc', methods=['POST'])
def receive_data_astrainc():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        root = ET.fromstring(xml_data)  # Parse the XML data
        received_data_astrainc.append(ET.tostring(root, encoding='utf8', method='xml'))

        # count volume event occurances
        vol_element = root.find('.//ns0:parameter[ns0:name="volumeName"]/ns0:value', namespaces)
        # Extract the text from the volumeName element if it exists
        if vol_element is not None:
            vol_name = vol_element.text
            # Increment the count for this volume in the dictionary
            event_summary_astrainc[vol_name] = event_summary_astrainc.get(vol_name, 0) + 1

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415
    
@app.route('/ntap_svm_polarisltd', methods=['POST'])
def receive_data_polarisltd():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        root = ET.fromstring(xml_data)  # Parse the XML data
        received_data_polarisltd.append(ET.tostring(root, encoding='utf8', method='xml'))

        # count volume event occurances
        vol_element = root.find('.//ns0:parameter[ns0:name="volumeName"]/ns0:value', namespaces)
        # Extract the text from the volumeName element if it exists
        if vol_element is not None:
            vol_name = vol_element.text
            # Increment the count for this volume in the dictionary
            event_summary_polarisltd[vol_name] = event_summary_polarisltd.get(vol_name, 0) + 1

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415

@app.route('/show_events_bluecorp')
def show_data_bluecorp():
    # Pass the event summary along with the received data to the template
    return render_template('data.html', data=[data.decode('utf8') for data in received_data_bluecorp], summary=event_summary_bluecorp)

@app.route('/show_events_astrainc')
def show_data_astrainc():
    # Pass the event summary along with the received data to the template
    return render_template('data.html', data=[data.decode('utf8') for data in received_data_astrainc], summary=event_summary_astrainc)

@app.route('/show_events_polarisltd')
def show_data_polarisltd():
    # Pass the event summary along with the received data to the template
    return render_template('data.html', data=[data.decode('utf8') for data in received_data_polarisltd], summary=event_summary_polarisltd)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)