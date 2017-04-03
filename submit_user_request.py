import httplib
import urllib
import json

constraints = {'max_airmass' : 1.6}

# this selects any telescope on the 1 meter network
location = {
            'telescope_class':'1m0',
}

proposal = {
    'proposal_id'   : 'LCOSchedulerTest',
    'user_id'       : 'zwalker@lcogt.net',
    'password'      : 'password',
}

molecule = {
      # Required fields
    'exposure_time'   : 60.0,  # Exposure time, in secs
    'exposure_count'  : 10,  # The number of consecutive exposures
    'filter'          : 'ip',  # The generic filter name
    # Optional fields. Defaults are as below.
    # fill_window should be defined as True on a maximum of one molecule per request, or you should receive an error when scheduling
    'fill_window'     : False, # set to True to cause this molecule to fill its window (or all windows of a cadence) with exposures, calculating exposure_count for you
    'type'            : 'EXPOSE',  # The type of the molecule
    'ag_name'         : '',  # '' to let it resolve; same as instrument_name for self-guiding
    'ag_mode'         : 'Optional',
    'instrument_name' : '1M0-SCICAM-SINISTRO',  # This resolves to the main science camera on the scheduled resource
    'bin_x'           : 2,  # Your binning choice. Right now these need to be the same.
    'bin_y'           : 2,
    'defocus'         : 0.0  # Mechanism movement of M2, or how much focal plane has moved (mm)
    }

# define the target
target = {
          'name'              : "Test Target",
          'ra'                : 12.0,  # RA (degrees)
          'dec'               : 34.4,  # Dec (Degrees)
          'epoch'             : 2000,
    }

# this is the actual window
window = {
          'start' : "2014-12-24T22:00:00",  # str(datetime)
          'end' : "2014-12-24T23:00:00",  # str(datetime)
    }

request = {
    "constraints" : constraints,
    "location" : location,
    "molecules" : [molecule],
    "observation_note" : "",
    "observation_type" : "NORMAL",
    "target" : target,
    "type" : "request",
    "windows" : [window],
    }

user_request = {
    "operator" : "single",
    "requests" : [request],
    # ipp_value is an optional field that acts as a multiplier to your proposal base priority.
    "ipp_value": 1.0,
    "type" : "compound_request"
    }

json_user_request = json.dumps(user_request)
params = urllib.urlencode({'username': proposal['user_id'],
                           'password': proposal['password'],
                           'proposal': proposal['proposal_id'],
                           'request_data' : json_user_request})
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn = httplib.HTTPSConnection("lcogt.net")
conn.request("POST", "/observe/service/request/submit", params, headers)
conn_response = conn.getresponse()

# The status can tell you if sending the request failed or not. 200 or 203 would mean success, 400 or anything else fail
status_code = conn_response.status

# If the status was a failure, the response text is a reason why it failed
# If the status was a success, the response text is tracking number of the submitted request
response = conn_response.read()

response = json.loads(response)
print response

if status_code == 200:
    try:
        print "http://lcogt.net/observe/request/" + response['id']
    except KeyError:
        print response['error']
