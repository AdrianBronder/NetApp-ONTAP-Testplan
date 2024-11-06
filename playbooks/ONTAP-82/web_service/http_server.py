#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Configuration for LDAP
app.config['LDAP_HOST'] = 'ldap://demo.netapp.com'  # e.g., 'ldap://your-ad-domain.com'
app.config['LDAP_BASE_DN'] = 'dc=demo,dc=netapp,dc=com'  # Base DN of your directory
app.config['LDAP_USER_DN'] = 'ou=Users'  # DN of users, e.g., 'ou=People'
app.config['LDAP_GROUP_DN'] = 'ou=Users'  # DN of groups, e.g., 'ou=Groups'
app.config['LDAP_USER_RDN_ATTR'] = 'cn'  # The attribute to use for RDN
app.config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'  # Attribute for logging in
app.config['LDAP_BIND_USER_DN'] = None  # The DN to bind with for authentication
app.config['LDAP_BIND_USER_PASSWORD'] = None  # The password to bind with

# Initialize the LDAP3 Login Manager
ldap_manager = LDAP3LoginManager(app)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate the user
        response = ldap_manager.authenticate(username, password)
        if response == AuthenticationResponseStatus.success:
            # User is authenticated, proceed to the protected area
            return redirect(url_for('protected_area'))
        else:
            # Authentication failed, show login form again with an error
            return render_template('login.html', error='Invalid credentials')
    # GET request, show the login form
    return render_template('login.html')

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