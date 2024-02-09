from flask import Flask, render_template, request, url_for
import requests
import random
from collections import defaultdict
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree,QuotaRule

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def request_services():
    svm = "ntap-svm01-nas"
    url = 'https://cluster1.demo.netapp.com/api/storage/volumes?svm.name='+svm+'&name=ontap_81_*'
    auth = ('admin', 'Netapp1!')
    response = requests.get(url, auth=auth, verify=False)
    data = response.json()
    departments = [{'name': volume['name'], 'uuid': volume['uuid']} for volume in data['records']]

    message = None  # Initialize the message

    if request.method == 'POST':
        department_name = request.form.get('volName')
        share_name = request.form.get('shareName')
        share_size_gib = int(request.form.get('shareSize'))  # Get the size in GiB

        # Convert the size to bytes
        share_size_bytes = share_size_gib * 1024**3

        # Make the API call
        config.CONNECTION = HostConnection(
            'cluster1.demo.netapp.com',
            username='admin',
            password='Netapp1!',
            verify=False
        )

        qtreeobj = {}
        qtreeobj['svm'] = {'name': svm}
        qtreeobj['volume'] = {'name': department_name}
        qtreeobj['name'] = share_name
        qtreeobj['security_style'] = 'ntfs'
        quotaobj = {}
        quotaobj['svm'] = {'name': svm}
        quotaobj['volume'] = {'name': department_name}
        quotaobj['qtree'] = {'name': share_name}
        quotaobj['type'] = "tree"
        quotaobj['space'] = {"hard_limit": share_size_bytes,
                             "soft_limit": share_size_bytes * 4 // 5}
        
        try:
            qtree = Qtree.from_dict(qtreeobj)
            quota = QuotaRule.from_dict(quotaobj)
            if qtree.post(poll=True) & quota.post(poll=True):
                message = "Share %s created Successfully" % qtree.name
        except NetAppRestError as error:
            message = "Exception caught :" + str(error)

    return render_template('index.html', departments=departments, message=message)

@app.route('/service_overview', methods=['GET'])
def list_services():
    config.CONNECTION = HostConnection(
        'cluster1.demo.netapp.com',
        username='admin',
        password='Netapp1!',
        verify=False
    )

    try:
        volumes = list(Volume.get_collection(
            fields='*',
            name='!*_root',
            **{'svm.name': '!*_ad'}))
    except NetAppRestError as error:
        volumes_list = []
        print("Exception caught :" + str(error))

    # Initialize a dictionary to store the volume distribution per SVM
    svm_distribution = defaultdict(int)

    for volume in volumes:
        # Add the size of each volume to the total size for its SVM
        svm_distribution[volume.svm.name] += volume.size

    # Convert the distribution dictionary to a list of tuples and sort it by SVM name
    svm_distribution = sorted(svm_distribution.items())

    # Generate a list of random RGB colors
    colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(svm_distribution))]

    return render_template('service_overview.html', volumes=volumes, svm_distribution=svm_distribution, colors=colors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)