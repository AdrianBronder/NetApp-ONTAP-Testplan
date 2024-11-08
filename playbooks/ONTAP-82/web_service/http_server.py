#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus
from ldap3 import Server, Connection, ALL
import xml.etree.ElementTree as ET
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration for LDAP
app.config['LDAP_HOST'] = 'ldap://dc1.demo.netapp.com'
app.config['LDAP_BASE_DN'] = 'dc=demo,dc=netapp,dc=com'
app.config['LDAP_USER_DN'] = 'cn=Users'
app.config['LDAP_USER_RDN_ATTR'] = 'cn'
app.config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'
app.config['LDAP_GROUP_MEMBERS_ATTR'] = 'member'
app.config['LDAP_BIND_USER_DN'] = 'Administrator@demo.netapp.com'
app.config['LDAP_BIND_USER_PASSWORD'] = 'Netapp1!'
app.config['LDAP_USER_SEARCH_SCOPE'] = 'SUBTREE'
app.config['LDAP_GROUP_SEARCH_BASE'] = 'dc=demo,dc=netapp,dc=com'
app.config['LDAP_GROUP_SEARCH_FILTER'] = '(objectclass=group)'
app.config['LDAP_GROUP_SEARCH_SCOPE'] = 'SUBTREE'
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key

# Initialize the LDAP3 Login Manager
ldap_manager = LDAP3LoginManager(app)

# In-memory storage for demonstration purposes
received_data_bluecorp = []
received_data_astrainc = []
received_data_polarisltd = []

# Namespace for XML parsing
namespaces = {'ns0': 'http://www.netapp.com/filer/admin'}

# Define a function to convert XML to JSON
def xml_to_json(xml_data):
    root = ET.fromstring(xml_data)
    json_data = {
        'cluster_uuid': root.find('.//ns0:cluster-uuid', namespaces).text,
        'node_uuid': root.find('.//ns0:node-uuid', namespaces).text,
        'node': root.find('.//ns0:node', namespaces).text,
        'message_name': root.find('.//ns0:message-name', namespaces).text,
        'version': root.find('.//ns0:version', namespaces).text,
        'parameters': [
            {
                'name': param.find('ns0:name', namespaces).text,
                'value': param.find('ns0:value', namespaces).text
            }
            for param in root.findall('.//ns0:parameter', namespaces)
        ]
    }
    return json_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ntap_svm_bluecorp', methods=['POST'])
def receive_data_bluecorp():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        json_data = xml_to_json(xml_data)  # Convert XML to JSON
        received_data_bluecorp.append(json_data)  # Store JSON data

        # Log the received data
        logger.info(f"Received data for Bluecorp: {json_data}")

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415

@app.route('/ntap_svm_astrainc', methods=['POST'])
def receive_data_astrainc():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        json_data = xml_to_json(xml_data)  # Convert XML to JSON
        received_data_astrainc.append(json_data)  # Store JSON data

        # Log the received data
        logger.info(f"Received data for Astrainc: {json_data}")

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415

@app.route('/ntap_svm_polarisltd', methods=['POST'])
def receive_data_polarisltd():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        json_data = xml_to_json(xml_data)  # Convert XML to JSON
        received_data_polarisltd.append(json_data)  # Store JSON data

        # Log the received data
        logger.info(f"Received data for Polaris Ltd: {json_data}")

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415

@app.route('/show_events_bluecorp')
def show_data_bluecorp():
    return render_template('data.html', data=received_data_bluecorp)

@app.route('/show_events_astrainc')
def show_data_astrainc():
    return render_template('data.html', data=received_data_astrainc)

@app.route('/show_events_polarisltd')
def show_data_polarisltd():
    return render_template('data.html', data=received_data_polarisltd)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
