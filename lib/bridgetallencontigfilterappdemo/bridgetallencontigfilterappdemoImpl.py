# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from Bio import SeqIO
from installed_clients.AssemblyUtilClient import AssemblyUtil

from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class bridgetallencontigfilterappdemo:
    '''
    Module Name:
    bridgetallencontigfilterappdemo

    Module Description:
    A KBase module: bridgetallencontigfilterappdemo
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:bridgetallen/NEWcontigfilterdemo.git"
    GIT_COMMIT_HASH = "a60e335cf5dbf63c7e7f06670267146d64ac3526"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_bridgetallencontigfilterappdemo(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_bridgetallencontigfilterappdemo
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
                                                'workspace_name': params['workspace_name']})
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_bridgetallencontigfilterappdemo

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_bridgetallencontigfilterappdemo return value ' +
                             'output is not type dict as required.')
    # return the results
    return [output]

    def run_bridgetallenContigFilter_max(self, ctx, params):
        """
        A variation of the contig filter that filters by both minimum and maximum contig length.
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_bridgetallencontigfilterappdemo_max
        required_params = ['workspace_name', 'assembly_ref', 'min_length', 'max_length']
        for param in required_params:
            if param not in params:
                raise ValueError(f"Missing required parameter: {param}")

        assembly_util = AssemblyUtil(self.callback_url)
        fasta_file = assembly_util.get_assembly_as_fasta({'ref': params['assembly_ref']})
        print(fasta_file)

        # Parse the downloaded file in FASTA format
        parsed_assembly = SeqIO.parse(fasta_file['path'], 'fasta')
        min_length = params['min_length']
        max_length = params['max_length']

        # Keep a list of contigs greater than min_length
        good_contigs = []
        # total contigs regardless of length
        n_total = 0
        # total contigs over the min_length
        n_remaining = 0
        for record in parsed_assembly:
            n_total += 1
            if len(record.seq) >= min_length and len(record.seq) <= max_length:
                good_contigs.append(record)
                n_remaining += 1
        output = {
            'n_total': n_total,
            'n_remaining': n_remaining
        }
        # Underneath your loop that filters contigs:
        # Create a file to hold the filtered data
        workspace_name = params['workspace_name']
        filtered_path = os.path.join(self.shared_folder, 'filtered.fasta')
        SeqIO.write(good_contigs, filtered_path, 'fasta')
        # Upload the filtered data to the workspace
        new_ref = assembly_util.save_assembly_from_fasta({
            'file': {'path': filtered_path},
            'workspace_name': workspace_name,
            'assembly_name': fasta_file['assembly_name']
        })
        output = {
            'n_total': n_total,
            'n_remaining': n_remaining,
            'filtered_assembly_ref': new_ref
        }
        # Create an output summary message for the report
        text_message = "".join([
            'Filtered assembly to ',
            str(n_remaining),
            ' contigs out of ',
            str(n_total)
        ])
        # Data for creating the report, referencing the assembly we uploaded
        report_data = {
            'objects_created': [
                {'ref': new_ref, 'description': 'Filtered contigs'}
            ],
            'text_message': text_message
        }
        # Initialize the report
        kbase_report = KBaseReport(self.callback_url)
        report = kbase_report.create({
            'report': report_data,
            'workspace_name': workspace_name
        })
        # Return the report reference and name in our results
        output = {
            'report_ref': report['ref'],
            'report_name': report['name'],
            'n_total': n_total,
            'n_remaining': n_remaining,
            'filtered_assembly_ref': new_ref
        }
        #END run_{username}ContigFilter_max

        for name in ['min_length', 'max_length', 'assembly_ref', 'workspace_name']:
            if name not in params:
                raise ValueError(f'Parameter "{name}" is required but missing')

        if not isinstance(params['min_length'], int) or params['min_length'] < 0:
            raise ValueError('Min length must be a non-negative integer')

        if not isinstance(params['max_length'], int) or params['max_length'] < 0:
            raise ValueError('Max length must be a non-negative integer')

        if not isinstance(params['assembly_ref'], str) or not params['assembly_ref']:
            raise ValueError('Pass in a valid assembly reference string')

        print("Running run_bridgetallenContigFilter_max with", params)

        output = {
            'n_total': n_total,
            'n_remaining': n_remaining
        }

        #END run_bridgetallencontigfilterappdemo_max
        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_bridgetallencontigfilterappdemo_max return value '
                             'output is not type dict as required.')

        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {
            'state': "OK",
            'message': "",
            'version': self.VERSION,
            'git_url': self.GIT_URL,
            'git_commit_hash': self.GIT_COMMIT_HASH
        }
        #END_STATUS
        return [returnVal]

