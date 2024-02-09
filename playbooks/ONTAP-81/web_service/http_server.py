from flask import Flask, render_template, request, url_for
import requests
import random
from collections import defaultdict
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree,QuotaRule,QuotaReport

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
            if qtree.post(poll=True):
                quota = QuotaRule.from_dict(quotaobj)
                if quota.post(poll=True):
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
        quotaReport = list(QuotaReport.get_collection(
            fields='*',
            type='tree',
            **{'svm.name': 'ntap-svm01-nas'}))
    except NetAppRestError as error:
        quotaReport = []
        print("Exception caught :" + str(error))

    print(list(quotaReport))

    # Initialize a dictionary to store the volume distribution per SVM
    quota_distribution_count = defaultdict(int)
    quota_distribution_space = defaultdict(int)

    for quota in quotaReport:
        # Add the size of each volume to the total size for its SVM
        if quota.space.hard_limit is not None:
            quota_distribution_count[quota.volume.name] += 1
            quota_distribution_space[quota.volume.name] += quota.space.hard_limit

    # Convert the distribution dictionary to a list of tuples and sort it by SVM name
    quota_distribution_count = sorted(quota_distribution_count.items())
    quota_distribution_space = sorted(quota_distribution_space.items())

    # Generate a list of random RGB colors
    colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(quota_distribution_count))]

    return render_template('service_overview.html',
                           quotaReport=quotaReport,
                           quota_distribution_space=quota_distribution_space,
                           quota_distribution_count=quota_distribution_count,
                           colors=colors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)