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
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate the user
        response = ldap_manager.authenticate(username, password)
        if response.status == AuthenticationResponseStatus.success:
            user_dn = response.user_dn
            user_groups = response.user_groups  # Retrieve group information
            user_groups_list = [group['name'] for group in user_groups]
            session['username'] = user_dn
            session['groups'] = user_groups_list
            logger.debug(f"User {username} authenticated successfully with groups: {user_groups_list}")
            return redirect(url_for('ransomware_events'))
        else:
            logger.debug(f"Login failed for user {username}")
            # Authentication failed, show login form again with an error
            return render_template('login.html', error='Login failed, try again.')
    # GET request, show the login form
    return render_template('login.html')

@app.route('/ransomware_events')
def ransomware_events():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    company_name = "Unknown"
    event_data = []
    summary_data = {}

    # Determine what data to show based on group membership
    if 'bluecorp' in session['groups']:
        company_name = "Blue Corp"
        event_data = received_data_bluecorp
        summary_data = event_summary_bluecorp
    elif 'astrainc' in session['groups']:
        company_name = "Astra Inc"
        event_data = received_data_astrainc
        summary_data = event_summary_astrainc
    elif 'polarisltd' in session['groups']:
        company_name = "Polaris Ltd"
        event_data = received_data_polarisltd
        summary_data = event_summary_polarisltd

    logger.debug(f"User {session['username']} belongs to company: {company_name}")
    # Render a template with the appropriate data and group memberships
    return render_template('ransomware_events.html',
                           data=[data.decode('utf8') for data in event_data],
                           summary=summary_data,
                           company=company_name)

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
