# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:

"""Main module."""
import csv
import os
import os.path
import logging
import requests
import json
import time
from dotmap import DotMap
import behavioral_signals_swagger_client as swagger_client
from datetime import datetime
from dateutil.parser import parse
from . import cliargs
from . import utils
from .utils import die
from .service import Caller

opts = {}


# -- collect results for all pids
def get_results_for_pid_list(pid_file, output_dir, level="call"):
    service = Caller(opts=opts)
    missing_pids = []

    # Iterate over all ids until they're all fetched or discarded
    pending_pids = list(utils.words(pid_file))
    while len(pending_pids) > 0:
        pid = pending_pids.pop(0)

        status = None
        resp = service.GetInfo(pid, poll=True)
        # -- success?
        if resp.status == 2:
            logging.debug("Processing status for pid {}: {}. Downloading results.".format(pid, resp.status))
            if level == "call":
                service.GetResults(pid, output_dir=output_dir, dest=resp.source)
            elif level == "frames":
                service.GetFrameResults(pid, output_dir=output_dir, dest=resp.source)
            elif level == "asr":
                service.GetASRResults(pid, output_dir=output_dir, dest=resp.source)
            elif level == "features":
                service.GetFeaturesResults(pid, output_dir=output_dir, dest=resp.source)
        elif resp.status == -1:
            logging.warning("Retrying job with pid: {}. Processing status: {}".format(pid, resp.status))
            pending_pids += [pid]
        else:
            logging.warning("Problem with pid: {}. Processing status: {}. Reason: {}".format(pid, resp.status, resp.statusmsg))
            missing_pids += [pid]
        time.sleep(5)

    return missing_pids


# -- for a user URI
def get_user_uri():
    return '{}/client/{}'.format(opts.apiurl, opts.apiid)


def get_process_audio_uri():
    return '{}/process/audio'.format(get_user_uri())


# -- submit one audio file
def submit_single_file(files, data):
    headers = {'X-Auth-Token': opts.apitoken, 'Accept': "application/json"}

    # Validate if number of channels and call direction are correct
    if 'channels' not in data or (data['channels'] != 1
                                  and data['channels'] != 2):
        data['channels'] = 1
        logging.warn('Set value for channels to default')

    if 'calldirection' not in data or (data['calldirection'] != '1'
                                       and data['calldirection'] != '2'):
        data['calldirection'] = '1'
        logging.warn('Set value for call direction to default')

    showRequest(data, files, headers)
    response = requests.post(get_process_audio_uri(),
                             params=data, files=files, headers=headers)
    showResponse(response)
    return response


def showRequest(data, files, headers):
    logging.debug("sending a post request")
    logging.debug("\t %12s: %s", 'headers', headers)
    logging.debug("\t %12s: %s", 'data', data)
    logging.debug("\t %12s: %s", 'files', files)

# -- log the response in logging.debug
def showResponse(response):
    logging.debug('api response:')
    logging.debug('\t%12s: %s', 'status', response.status_code)
    logging.debug('\t%12s: %s', 'reason', response.reason)


def submit_single_file_no_params(file_name):
    # Default data values
    data = {'channels': '1', 'calldirection': '1'}
    try:
        files = {'file': open(file_name, 'rb')}
    except FileNotFoundError:
        logging.warning("File '{}' does not exist.".format(file_name))
        return ''
    return submit_single_file(files, data)


def submit_file_list(file_list):
    with open(file_list, 'r') as l:
        for line in l:
            file_name = line.rstrip()
            logging.debug('Submitting {}'.format(file_name))
            r = submit_single_file_no_params(file_name)
            logging.debug(r.url)
            logging.debug(r.text)


def convert_iso_datetime_format(calltime):
    """
    Convert datetime string to ISO datetime string
    """
    service_datetime_fmt = '%m/%d/%Y %H:%M:%S'

    if calltime is None:
        return calltime

    try:
        calltime = parse(calltime)
        calltime = calltime.strftime(service_datetime_fmt)
    except ValueError:
        return None
    else:
        return calltime


def submit_csv_file(csv_file, pid_file, tag=None, nchannels=1):
    data_fields = ['channels', 'calldirection', 'agentId',
                   'agentTeam', 'campaignId', 'calltype', 'calltime', 'timezone',
                   'ANI', 'tag', 'meta', 'predictionmode', 'tasks']
    n_failures = 0

    with open(csv_file, 'r') as f:
        with open(pid_file, 'w') as p:
            reader = csv.reader(f, delimiter=",", quotechar="'")
            for row in reader:
                if not row:
                    logging.warning("Skipping empty lines included in '{}' file".format(f))
                    continue
                file_name = row[0]
                data = {}
                n_data_values = len(row)
                if n_data_values > 1:
                    for idx, value in enumerate(row[1:]):
                        if value:
                            if data_fields[idx] == 'channels':
                                value = int(value)
                            elif data_fields[idx] == 'calltime':
                                value = convert_iso_datetime_format(value)

                            data[data_fields[idx]] = value
                            if data_fields[idx] == 'tag':
                                if tag is not None:
                                    data['tag'] += ',{}'.format(tag)

                # No ASR column at csv so default to asr=TRUE
                if 'predictionmode' not in data:  
                    data['predictionmode'] = 'full'

                # Backwards Compatible check
                # No TASKS column at csv so default to None
                if 'tasks' not in data:
                    data['tasks'] = None
                    logging.info("No Tasks value found. Tasks value set to None.")

                if 'tag' not in data and tag is not None:
                    data['tag'] = tag
                if 'channels' not in data:
                    data['channels'] = int(nchannels)
                try:
                    files = {'file': open(file_name, 'rb')}
                except FileNotFoundError:
                    logging.warning("Skipping line in '{}' file because '{}' file does not exist.".format(f, file_name))
                    continue
                r = submit_single_file(files, data)

                if r.status_code != 200:
                    n_failures += 1

                else:
                    j = json.loads(r.text)
                    p.write("{}\n".format(j['pid']))

    return n_failures

def get_user_details():
    headers = {'X-Auth-Token': opts.apitoken, 'Accept': "application/json"}
    r = requests.get(get_user_uri(), headers=headers)
    logging.debug(r.url)
    logging.debug(r.text)


def send_audio(args):
    logging.info('Using csv file: {}'.format(args.csvFile))

    n_failures = submit_csv_file(args.csvFile, args.pidFile,
                                 tag=args.tag, nchannels=args.nchannels)

    if n_failures == 0:
        logging.info("File uploading ran successfully.")
        return 0
    return 1


def poll_for_results(args, level="call"):
    if not os.path.exists(args.resultsDir):
        logging.warning("Creating new folder: {}".format(args.resultsDir))
        os.makedirs(args.resultsDir)
    missing_pids = get_results_for_pid_list(args.pidFile, args.resultsDir, level)
    if len(missing_pids) > 0:
        logging.info("No results for PIDs: {}".format(missing_pids))
        return 1
    else:
        logging.info("Results for all pids have been downloaded.")
        return 0


def get_results(args):
    return poll_for_results(args, level="call")


def get_results_frames(args):
    return poll_for_results(args, level="frames")


def get_results_asr(args):
    return poll_for_results(args, level="asr")


def get_results_features(args):
    return poll_for_results(args, level="features")


# -- dump the configuration file
def dump_config(opts):
    print("*** bsi-cli configuration")
    for key in sorted(opts.keys()):
        if key == 'func' : continue
        print("{:>16} : {}".format(key,opts[key]))
    print("***")
    return 0

def main():
    global opts
    # -- parse the command line args
    opts = cliargs.parse(
        get_results, get_results_frames, get_results_asr, get_results_features, send_audio, dump_config
    )
    opts = DotMap(opts, _dynamic=False)
    if opts.apiid == None:
        die("no BEST_API_ID/apiid was specified (env or config file)")
    if opts.apitoken == None:
        die("no BEST_API_TOKEN/apitoken was specified (env or config file)")

    # -- invoke the subcommand
    return opts.func(opts)

if __name__ == '__main__':
    main()
