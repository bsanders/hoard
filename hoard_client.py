#! /usr/bin/env python3

import sys

import grpc

import hoard_pb2
import hoard_pb2_grpc
import convert_wiki_to_protobuf


def itemById(id_num):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hoard_pb2_grpc.HoardListerStub(channel)
        try:
            item = stub.GetItemById(
                hoard_pb2.ItemIdLookup(campaign_name='Dalelands', inventory_number=id_num)
            )
            print(item)
        except grpc._channel._Rendezvous as e:
            print(e.details())
            return

def itemListByOwner(owner):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hoard_pb2_grpc.HoardListerStub(channel)
        try:
            owner_lookup = hoard_pb2.ItemOwnerLookup(campaign_name='Dalelands', item_owner=owner)
            for item in stub.ListItemsByOwner(owner_lookup):
                print(item)
        except grpc._channel._Rendezvous as e:
            print(e.details())
            return

def run():

    if not sys.argv:
        return

    id_num = name = None
    try:
        id_num = int(sys.argv[1])
        itemById(id_num)
    except ValueError:
        name = sys.argv[1]
        itemListByOwner(name)


if __name__ == '__main__':
    run()
