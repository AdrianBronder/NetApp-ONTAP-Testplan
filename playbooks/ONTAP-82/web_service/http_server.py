#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus
#from ldap3 import Server, Connection, ALL
from datetime import datetime
import xml.etree.ElementTree as ET
import logging, os, re, yaml
from collections import defaultdict
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree,QuotaRule,QuotaReport,CifsShare
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.vars.manager import VariableManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set Paths
project_root_path                  = os.path.join(os.path.dirname(__file__), '../../..')
project_root_path                  = os.path.normpath(project_root_path)
inventory_path                     = project_root_path+'/inventories/labondemand_latest'
vars_path                          = project_root_path+'/vars/labondemand_latest'
# Import Ansible inventory information
with open(project_root_path+'/init/init_helper/vaultfile.txt', 'rb') as vault_password_file:
    vault_password = vault_password_file.read().strip()
secret                             = VaultSecret(vault_password)
vault                              = VaultLib(secrets=[(None, secret)])
dataloader                         = DataLoader()
dataloader.set_vault_secrets(vault.secrets)

# Load inventory vars
ansible_inventory                  = InventoryManager(loader=dataloader, sources=[os.path.normpath(inventory_path)])
ansible_inventory_vars             = VariableManager(loader=dataloader, inventory=ansible_inventory)
cluster1_vars                      = ansible_inventory_vars.get_vars(host=ansible_inventory.get_hosts(pattern='ontap')[0], include_hostvars=True)

# Load vars
def load_vars_from_files(vars_path, dataloader):
    vars_data = {}
    for filename in os.listdir(vars_path):
        file_path = os.path.join(vars_path, filename)
        if os.path.isfile(file_path) and filename.endswith(('.yml', '.yaml')):
            file_vars = dataloader.load_from_file(file_path)
            vars_data.update(file_vars)
    return vars_data

# Load variables from files in vars_path
ansible_file_vars = load_vars_from_files(vars_path, dataloader)

# Configuration for LDAP
app.config['LDAP_HOST']                = ansible_file_vars['ontap_80_ldap_host']
app.config['LDAP_BASE_DN']             = ansible_file_vars['ontap_80_base_dn']
app.config['LDAP_USER_DN']             = ansible_file_vars['ontap_80_user_dn']
app.config['LDAP_USER_RDN_ATTR']       = ansible_file_vars['ontap_80_user_rdn_attr']
app.config['LDAP_USER_LOGIN_ATTR']     = ansible_file_vars['ontap_80_user_login_attr']
app.config['LDAP_BIND_USER_DN']        = ansible_file_vars['ontap_80_bind_user_dn']
app.config['LDAP_BIND_USER_PASSWORD']  = ansible_file_vars['ontap_80_bind_user_pw']
app.config['LDAP_USER_SEARCH_SCOPE']   = ansible_file_vars['ontap_80_user_search_scope']
app.config['LDAP_GROUP_SEARCH_BASE']   = ansible_file_vars['ontap_80_group_search_base']
app.config['LDAP_GROUP_SEARCH_FILTER'] = ansible_file_vars['ontap_80_group_search_filter']
app.config['LDAP_GROUP_SEARCH_SCOPE']  = ansible_file_vars['ontap_80_group_search_scope']
app.config['LDAP_GROUP_MEMBERS_ATTR']  = ansible_file_vars['ontap_80_group_members_attr']
app.config['SECRET_KEY']               = ansible_file_vars['ontap_80_secret_key']

# Initialize the LDAP3 Login Manager
ldap_manager = LDAP3LoginManager(app)

# In-memory storage for demonstration purposes
received_data_bluecorp = []
event_summary_bluecorp = {}
received_data_astrainc = []
event_summary_astrainc = {}
received_data_polarisltd = []
event_summary_polarisltd = {}

# Namespace for XML parsing
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
            logger.info(f"User {username} authenticated successfully with groups: {user_groups_list}")
            
            if 'operators' in session['groups']:
                return redirect(url_for('ransomware_events_operator'))
            else:
                return redirect(url_for('ransomware_events'))
        else:
            logger.info(f"Login failed for user {username}")
            # Authentication failed, show login form again with an error
            return render_template('login.html', error='Login failed, try again.')
    # GET request, show the login form
    return render_template('login.html')

@app.route('/ransomware_events')
def ransomware_events():
    if 'username' not in session:
        return redirect(url_for('login'))
    elif 'operators' in session['groups']:
        return redirect(url_for('ransomware_events_operator'))

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

    # Sort event data in reverse order based on timestamp
    event_data_sorted = sorted(event_data, key=lambda x: x['timestamp'], reverse=True)

    logger.info(f"User {session['username']} belongs to company: {company_name}")
    # Render a template with the appropriate data and group memberships
    return render_template('ransomware_events.html',
                           data=event_data_sorted,
                           summary=summary_data,
                           company=company_name)

@app.route('/ransomware_events_operator')
def ransomware_events_operator():
    if 'username' not in session:
        return redirect(url_for('login'))
    if not 'operators' in session['groups']:
        return redirect(url_for('ransomware_events'))
    
    # Merge received data from all companies
    all_received_data = received_data_bluecorp + received_data_astrainc + received_data_polarisltd

    # Sort event data in reverse order based on timestamp
    event_data_sorted = sorted(all_received_data, key=lambda x: x['timestamp'], reverse=True)

    # Create a detailed summary of events by company and volume
    detailed_summary = {
        'Blue Corp': dict(event_summary_bluecorp),
        'Astra Inc': dict(event_summary_astrainc),
        'Polaris Ltd': dict(event_summary_polarisltd)
    }

    # Render a template with the appropriate data and summary
    return render_template('ransomware_events_operator.html',
                           data=event_data_sorted,
                           summary={
                               'Blue Corp': len(received_data_bluecorp),
                               'Astra Inc': len(received_data_astrainc),
                               'Polaris Ltd': len(received_data_polarisltd)
                           },
                           detailed_summary=detailed_summary)

@app.route('/ntap_svm_bluecorp', methods=['POST'])
def receive_data_bluecorp():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        root = ET.fromstring(xml_data)  # Parse the XML data

        timestamp = int(root.find('.//ns0:time', namespaces).text)
        readable_timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Extract details from the XML
        event_details = {
            'company': 'Blue Corp',  # adding custom customer name to the event array
            'timestamp': readable_timestamp,
            'seq_num': root.find('.//ns0:seq-num', namespaces).text,
            'cluster_uuid': root.find('.//ns0:cluster-uuid', namespaces).text,
            'node_uuid': root.find('.//ns0:node-uuid', namespaces).text,
            'node': root.find('.//ns0:node', namespaces).text,
            'message_name': root.find('.//ns0:message-name', namespaces).text,
            'event': root.find('.//ns0:event', namespaces).text,
            'volume_name': root.find('.//ns0:parameter[ns0:name="volumeName"]/ns0:value', namespaces).text,
            'vserver_name': root.find('.//ns0:parameter[ns0:name="vserverName"]/ns0:value', namespaces).text,
        }

        received_data_bluecorp.append(event_details)

        # Count volume event occurrences (correct "bugy" names ending with numbers in round brackets)
        vol_name = re.sub(r'\s*\(\d+\)$', '', event_details['volume_name'])
        event_summary_bluecorp[vol_name] = event_summary_bluecorp.get(vol_name, 0) + 1

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415

@app.route('/ntap_svm_astrainc', methods=['POST'])
def receive_data_astrainc():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        root = ET.fromstring(xml_data)  # Parse the XML data

        timestamp = int(root.find('.//ns0:time', namespaces).text)
        readable_timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Extract details from the XML
        event_details = {
            'company': 'Astra Inc',  # adding custom customer name to the event array
            'timestamp': readable_timestamp,
            'seq_num': root.find('.//ns0:seq-num', namespaces).text,
            'cluster_uuid': root.find('.//ns0:cluster-uuid', namespaces).text,
            'node_uuid': root.find('.//ns0:node-uuid', namespaces).text,
            'node': root.find('.//ns0:node', namespaces).text,
            'message_name': root.find('.//ns0:message-name', namespaces).text,
            'event': root.find('.//ns0:event', namespaces).text,
            'volume_name': root.find('.//ns0:parameter[ns0:name="volumeName"]/ns0:value', namespaces).text,
            'vserver_name': root.find('.//ns0:parameter[ns0:name="vserverName"]/ns0:value', namespaces).text,
        }

        received_data_astrainc.append(event_details)

        # Count volume event occurrences (correct "bugy" names ending with numbers in round brackets)
        vol_name = re.sub(r'\s*\(\d+\)$', '', event_details['volume_name'])
        event_summary_astrainc[vol_name] = event_summary_astrainc.get(vol_name, 0) + 1

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415
    
@app.route('/ntap_svm_polarisltd', methods=['POST'])
def receive_data_polarisltd():
    if request.headers['Content-Type'] == 'application/xml':
        xml_data = request.data  # Get the raw XML data
        root = ET.fromstring(xml_data)  # Parse the XML data

        timestamp = int(root.find('.//ns0:time', namespaces).text)
        readable_timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Extract details from the XML
        event_details = {
            'company': 'Polaris Ltd',  # adding custom customer name to the event array
            'timestamp': readable_timestamp,
            'seq_num': root.find('.//ns0:seq-num', namespaces).text,
            'cluster_uuid': root.find('.//ns0:cluster-uuid', namespaces).text,
            'node_uuid': root.find('.//ns0:node-uuid', namespaces).text,
            'node': root.find('.//ns0:node', namespaces).text,
            'message_name': root.find('.//ns0:message-name', namespaces).text,
            'event': root.find('.//ns0:event', namespaces).text,
            'volume_name': root.find('.//ns0:parameter[ns0:name="volumeName"]/ns0:value', namespaces).text,
            'vserver_name': root.find('.//ns0:parameter[ns0:name="vserverName"]/ns0:value', namespaces).text,
        }

        received_data_polarisltd.append(event_details)

        # Count volume event occurrences (correct "bugy" names ending with numbers in round brackets)
        vol_name = re.sub(r'\s*\(\d+\)$', '', event_details['volume_name'])
        event_summary_polarisltd[vol_name] = event_summary_polarisltd.get(vol_name, 0) + 1

        return jsonify(success=True)  # Acknowledge the receipt
    else:
        return jsonify(error="Unsupported Media Type"), 415

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)