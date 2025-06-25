# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from bridgetallencontigfilterappdemo.bridgetallencontigfilterappdemoImpl import bridgetallencontigfilterappdemo
from bridgetallencontigfilterappdemo.bridgetallencontigfilterappdemoServer import MethodContext
from bridgetallencontigfilterappdemo.authclient import KBaseAuth as _KBaseAuth

from installed_clients.baseclient import ServerError
from installed_clients.WorkspaceClient import Workspace


class bridgetallencontigfilterappdemoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('bridgetallencontigfilterappdemo'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
            'user_id': user_id,
            'provenance': [
                {'service': 'bridgetallencontigfilterappdemo',
                    'method': 'please_never_use_it_in_production',
                    'method_params': []
                    }],
                'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = bridgetallencontigfilterappdemo(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(), 'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass  # You can remove this when you add real test code

    def test_run_bridgetallencontigfilterappdemo_max(self):
        ref = "79/16/1"
        result = self.serviceImpl.run_bridgetallencontigfilterappdemo_max(self.ctx, {
            'workspace_name': self.wsName,
            'assembly_ref': ref,
            'min_length': 100,
            'max_length': 1000000
            })
    def test_invalid_params(self):
        impl = self.serviceImpl
        ctx = self.ctx
        ws = self.wsName
        # Missing assembly ref
        with self.assertRaises(ValueError):
            impl.run_bridgetallencontigfilterappdemo_max(ctx, {'workspace_name': ws,
                'min_length': 100, 'max_length': 1000000})
        # Missing min length
        with self.assertRaises(ValueError):
            impl.run_bridgetallencontigfilterappdemo_max(ctx, {'workspace_name': ws,
                'min_length': 100, 'max_length': 1000000})
        # Min length is negative
        with self.assertRaises(ServerError):
            impl.run_bridgetallencontigfilterappdemo_max(ctx, {'workspace_name': ws, 'assembly_ref': 'x',
                'min_length': -1, 'max_length': 1000000})
        # Min length is wrong type
        with self.assertRaises(ServerError):
            impl.run_bridgetallencontigfilterappdemo_max(ctx, {'workspace_name': ws, 'assembly_ref': 'x',
                'min_length': 'x', 'max_length': 1000000})
        # Assembly ref is wrong type
        with self.assertRaises(ServerError):
            impl.run_bridgetallencontigfilterappdemo_max(ctx, {'workspace_name': ws, 'assembly_ref': 1,
                'min_length': 1, 'max_length': 1000000})
        # TODO -- assert some things (later)

        ret = self.serviceImpl.run_bridgetallencontigfilterappdemo(self.ctx, {'workspace_name': self.wsName,
            'parameter_1': 'Hello World!'})
