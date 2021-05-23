import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4


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

blockchain = Blockchain()

node_identifier = str(uuid4()).replace('-', '')


class TransactionAPIView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            index = blockchain.new_transaction(
                request.data['device'], request.data['version'], request.data['data'])
            return JsonResponse({'message': f'Update block added {index}'}, status=201)
        else:
            return JsonResponse({'message': serializer.errors}, status=400)


class MineAPIView(APIView):
    def get(self, request):
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        blockchain.new_transaction(
            device=None,
            version=None,
            data=None
        )

        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        return JsonResponse({
            'message': 'New block mined',
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }, status=200)


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

        for node in nodes:
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
