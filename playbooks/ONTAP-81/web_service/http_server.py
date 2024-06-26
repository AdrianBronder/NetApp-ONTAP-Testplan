#!/usr/bin/env python3

import requests, random, os, ansible
from flask import Flask, render_template, request, url_for
from collections import defaultdict
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree,QuotaRule,QuotaReport,CifsShare
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.vault import VaultLib, VaultSecret
from ansible.vars.manager import VariableManager

app = Flask(__name__)

# Request page
@app.route('/', methods=['GET', 'POST'])
def request_services():
    # Fetch departments for drop down selection
    url = ('https://' +
          cluster +
          '.demo.netapp.com/api/storage/volumes?svm.name=' +
          svm +
          '&name=ontap_81_*')
    auth = (ontap_group_data['ontap_admin_user'], ontap_group_data['ontap_admin_password'])
    response = requests.get(url, auth=auth, verify=False)
    data = response.json()
    departments = [{'name': volume['name'], 'uuid': volume['uuid']} for volume in data['records']]

    message = None

    # Process a request
    if request.method == 'POST':
        # Get forms data
        vol_name = request.form.get('volName')
        share_name = request.form.get('shareName')
        share_size_gib = int(request.form.get('shareSize'))

        # Convert data
        share_size_bytes = share_size_gib * 1024**3
        department_name = vol_name.replace('ontap_81_','')

        # Establish connection to storage cluster
        config.CONNECTION = HostConnection(
            cluster+'.demo.netapp.com',
            username=ontap_group_data['ontap_admin_user'],
            password=ontap_group_data['ontap_admin_password'],
            verify=False
        )

        # Define Qtree object
        qtreeobj                       = {}
        qtreeobj['svm']                = {'name': svm}
        qtreeobj['volume']             = {'name': vol_name}
        qtreeobj['name']               = share_name
        qtreeobj['security_style']     = 'ntfs'
        # Define Quota object
        quotaobj                       = {}
        quotaobj['svm']                = {'name': svm}
        quotaobj['volume']             = {'name': vol_name}
        quotaobj['qtree']              = {'name': share_name}
        quotaobj['type']               = "tree"
        quotaobj['space']              = {"hard_limit": share_size_bytes,
                                          "soft_limit": share_size_bytes * 4 // 5}
        # Define Share object
        shareobj                       = {}
        shareobj['svm']                = {'name': svm}
        shareobj['name']               = department_name + '_' + share_name
        shareobj['path']               = '/'+ vol_name +'/'+share_name
        shareobj['show_snapshot']      = True
        shareobj['change_notify']      = True
        shareobj['oplocks']            = True
        shareobj['unix_symlink']       = "local"

        # Execute the API calls
        try:
            qtree = Qtree.from_dict(qtreeobj)
            if qtree.post(poll=True):
                quota = QuotaRule.from_dict(quotaobj)
                if quota.post(poll=True):
                    share = CifsShare.from_dict(shareobj)
                    if share.post(poll=True):
                        message = ("Share created Successfully! Access via: \r\n" + 
                                   "\\\\" + svm + ".demo.netapp.com" + "\\" + share.name)
        except NetAppRestError as error:
            message = "Exception caught :" + str(error)
       
    return render_template('index.html', departments=departments, message=message)

# Service overview page
@app.route('/service_overview', methods=['GET'])
def list_services():
    # Establish connection to storage cluster
    config.CONNECTION = HostConnection(
        'cluster1.demo.netapp.com',
        username=ontap_group_data['ontap_admin_user'],
        password=ontap_group_data['ontap_admin_password'],
        verify=False
    )

    # Get quota information
    try:
        quotaReport = list(QuotaReport.get_collection(
            fields='*',
            type='tree',
            **{'svm.name': 'ntap-svm01-nas'}))
    except NetAppRestError as error:
        quotaReport = []
        print("Exception caught :" + str(error))

    # Initialize lists and dictionaries
    quota_distribution_count = defaultdict(int)
    quota_distribution_space = defaultdict(int)
    quotaReport_sanitized = []

    # Filter on qtrees only with quota set
    for quota in quotaReport:
        hard_limit = getattr(quota.space, 'hard_limit', None)
        if hard_limit is not None:
            quotaReport_sanitized.append(quota)
            quota_distribution_count[quota.volume.name.replace('ontap_81_','')] += 1
            quota_distribution_space[quota.volume.name.replace('ontap_81_','')] += quota.space.hard_limit / 1024**3
    quota_distribution_count = sorted(quota_distribution_count.items())
    quota_distribution_space = sorted(quota_distribution_space.items())

    # Generate a list of random RGB colors
    colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(quota_distribution_count))]

    # Build page with quota data
    return render_template('service_overview.html',
                           quotaReport=quotaReport_sanitized,
                           quota_distribution_space=quota_distribution_space,
                           quota_distribution_count=quota_distribution_count,
                           colors=colors)

# helper to merge decrypted vars with other vars
def replace_vars(data, vault_data):
    for key, value in data.items():
        if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
            vault_key = value[2:-2].strip()  # Remove '{{' and '}}' and strip whitespace
            if vault_key in vault_data:
                data[key] = vault_data[vault_key]
        elif isinstance(value, dict):
            replace_vars(value, vault_data)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    replace_vars(item, vault_data)


if __name__ == '__main__':
    # Set Paths
    project_root_path                  = os.path.join(os.path.dirname(__file__), '../../..')
    project_root_path                  = os.path.normpath(project_root_path)
    inventory_path                     = project_root_path+'/inventories/labondemand_latest'

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

    # Load group vars for ONTAP
    ontap_group_data                   = dataloader.load_from_file(inventory_path+'/group_vars/ontap/vars.yml')
    ontap_group_data_vault             = dataloader.load_from_file(inventory_path+'/group_vars/ontap/vault.yml')
    replace_vars(ontap_group_data, ontap_group_data_vault)

    # Set global standard variables
    cluster                            = str(ansible_inventory.get_hosts(pattern='primary_storage_clusters')[0])
    svm                                = "ntap-svm01-nas"

    app.run(host='0.0.0.0', port=80, debug=True)