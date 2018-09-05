#! /usr/bin/env python3

from concurrent import futures

import time


import grpc

import hoard_pb2
import hoard_pb2_grpc
import convert_wiki_to_protobuf

_ONE_DAY_IN_SECONDS = 60 * 60 * 24





class HoardListerServicer(hoard_pb2_grpc.HoardListerServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.db = convert_wiki_to_protobuf.read_hoard_database()

    def GetItemById(self, request, context):
        for item in self.db.items:
            if item.inventory_number == request.inventory_number:
                return item
        return context.abort(grpc.StatusCode.NOT_FOUND, 'Item not found')

    def ListItemsByOwner(self, request, context):
        for item in self.db.items:
            if item.owner != request.item_owner:
                continue

            new_item = hoard_pb2.Item()
            new_item.CopyFrom(item)
            del new_item.abilities[:]
            for idx, ab in enumerate(item.abilities):
                if ab.identified:
                    hoard_pb2.Item.Ability()
                    new_item.abilities.add(
                            function=ab.function,
                            url=ab.url,
                    )

            yield new_item

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hoard_pb2_grpc.add_HoardListerServicer_to_server(
        HoardListerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
