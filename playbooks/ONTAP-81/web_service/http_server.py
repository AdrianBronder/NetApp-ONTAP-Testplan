from flask import Flask, render_template, request, url_for
import requests
import random
from collections import defaultdict
from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Volume

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def request_services():
    url = 'https://cluster1.demo.netapp.com/api/svm/svms?name=!*_ad'
    auth = ('admin', 'Netapp1!')
    response = requests.get(url, auth=auth, verify=False)
    data = response.json()
    svms = [{'name': svm['name'], 'uuid': svm['uuid']} for svm in data['records']]

    message = None  # Initialize the message

    if request.method == 'POST':
        selected_svm = request.form.get('svmUUID')
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

        volobj = {}
        volobj['svm'] = {'uuid': selected_svm}
        volobj['name'] = share_name
        volobj['size'] = share_size_bytes
        volobj['type'] = 'rw'
        volobj['style'] = 'flexvol'
        volobj['aggregates'] = [{'name': 'cluster1_01_aggr01'}]
        volobj['nas'] = {
            "export_policy":
            {
                "name": "default"
            },
            "path": "/"+share_name,
            "security_style": 'ntfs'
        }

        try:
            volume = Volume.from_dict(volobj)
            if volume.post(poll=True):
                message = "Volume %s created Successfully" % volume.name
        except NetAppRestError as error:
            message = "Exception caught :" + str(error)

    return render_template('index.html', svms=svms, message=message)

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