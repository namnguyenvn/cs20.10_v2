import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from django.conf import settings
from urllib.parse import urlparse

from django.core import paginator
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse, Http404
from django.core.paginator import InvalidPage, Paginator,  EmptyPage, PageNotAnInteger
from django.core import serializers
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
# Rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes


from blockchain.blockchain import Blockchain

from api.serializers import *

from iotupdate.models import *

blockchain = Blockchain()

node_identifier = str(uuid4()).replace('-', '')


class TransactionAPIView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            index = blockchain.new_transaction(
                request.data['device'], request.data['version'], request.data['hash'])
            return JsonResponse({'message': f'Update block added {index}'}, status=201)
        else:
            return JsonResponse({'message': serializer.errors}, status=400)


class MineAPIView(APIView):
    def get(self, request):
        node_address = request.query_params.get('node_address')
        print(node_address)
        last_block = blockchain.last_block
        # last_proof = last_block['proof']
        # proof = blockchain.proof_of_work(last_block)
        proof = blockchain.proof_of_authentication(node_address)

        # blockchain.new_transaction(
        #     device=None,
        #     version=None,
        #     data=None
        # )

        if proof is not None:
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(proof, previous_hash)

            return JsonResponse({
                'message': 'New block mined',
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
            }, status=200)
        return JsonResponse({
            'error': 'invalid proof'
        }, status=400)


class FullChainAPIView(APIView):
    def get(self, request):
        return JsonResponse({
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }, status=200)


class NodeRegisterAPIView(APIView):
    def post(self, request):
        nodes = request.data['nodes']

        if nodes is None:
            return JsonResponse({'message': 'Invalid Node List'}, status=400)

        trusted_hosts = settings.TRUSTED_HOSTS

        for node in nodes:
            for trusted_host in trusted_hosts:
                parsed_url = urlparse(node)
                if str(parsed_url.netloc) == trusted_host:
                    blockchain.register_node(node)

        return JsonResponse({
            'message': 'New nodes added',
            'total_nodes': list(blockchain.nodes)
        }, status=201)


class NodeResolveAPIView(APIView):
    def get(self, request):
        replaced = blockchain.resolve_conflicts()

        if replaced:
            return JsonResponse({
                                'message': 'Chain replaced',
                                'new_chain': blockchain.chain
                                }, status=200)
        else:
            return JsonResponse({
                                'message': 'Chain is authoritative',
                                'chain': blockchain.chain
                                }, status=200)


class DeviceTempAPIView(APIView):
    def post(self, request):
        try:
            device_id = request.data['device_ip']
            temp = request.data['temp']
            timestamp = request.data['timestamp']
            device = Device.objects.get(ip=device_id)
            device_temp = DeviceTemp.objects.create(
                device=device,
                temp=temp,
                timestamp=timestamp
            )
            return JsonResponse({'message': DeviceTempSerializer(device_temp).data}, status=201)
        except Device.DoesNotExist as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)


class CentralServerCommandAPIView(APIView):
    def get(self, request):
        try:
            # get device IP
            device_ip = request.query_params.get('device_ip')
            device = Device.objects.get(ip=device_ip)
            device_serializer = DeviceSerializer(device)
            return JsonResponse({
                'message': 'Rollback',
                'rollback': True,
                'device': device_serializer.data
            }, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)


class RollbackLogAPIView(APIView):
    def post(self, request):
        try:
            type = request.data['type']
            detail = request.data['detail']
            time_execution = request.data['time_execution']
            rollback_log = RollbackLog.objects.create(
                type=type,
                detail=detail,
                time_execution=time_execution
            )
            return JsonResponse({'log': RollbackLogSerializer(rollback_log).data}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
