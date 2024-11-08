#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus
from ldap3 import Server, Connection, ALL
import xml.etree.ElementTree as ET
import logging

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration for LDAP
app.config['LDAP_HOST']                = 'ldap://dc1.demo.netapp.com'  # e.g., 'ldap://your-ad-domain.com'
app.config['LDAP_BASE_DN']             = 'dc=demo,dc=netapp,dc=com'  # Base DN of your directory
app.config['LDAP_USER_DN']             = 'cn=Users'  # DN of users, e.g., 'ou=People'
app.config['LDAP_USER_RDN_ATTR']       = 'cn'  # The attribute to use for RDN
app.config['LDAP_USER_LOGIN_ATTR']     = 'sAMAccountName'  # Attribute for logging in
app.config['LDAP_GROUP_MEMBERS_ATTR']  = 'member'
app.config['LDAP_BIND_USER_DN']        = 'Administrator@demo.netapp.com'  # The DN to bind with for authentication
app.config['LDAP_BIND_USER_PASSWORD']  = 'Netapp1!'  # The password to bind with
app.config['LDAP_USER_SEARCH_SCOPE']   = 'SUBTREE'
app.config['LDAP_GROUP_SEARCH_BASE']   = 'dc=demo,dc=netapp,dc=com'  # Base DN for group search
app.config['LDAP_GROUP_SEARCH_FILTER'] = '(objectclass=group)'  # Filter for group search
app.config['LDAP_GROUP_SEARCH_SCOPE']  = 'SUBTREE'  # Scope for group search
app.config['SECRET_KEY']               = 'ThisIsMySuperSecretKey'  # Replace with a real secret key

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
            return redirect(url_for('ransomware_events'))
        else:
            # Authentication failed, show login form again with an error
            return render_template('login.html', error='Login failed, try again.')
    # GET request, show the login form
    return render_template('login.html')

# Define a route to show data based on user groups
@app.route('/ransomware_events')
def ransomware_events():
    if 'username' not in session:
        return redirect(url_for('login'))
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
    else:
        event_data = []
        summary_data = {}
    # Render a template with the appropriate data and group memberships
    return render_template('ransomware_events.html',
                            data=[data.decode('utf8') for data in event_data],
                            summary=summary_data,
                            company=company_name)

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

# Define a logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)