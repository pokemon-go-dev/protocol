#!/usr/bin/env python

from mitmproxy.models import decoded
import queue
import protocol
import subprocess
import argparse
import sys

# A map of request ids to FIFO data structures to keep track of request types
# becauses responses don't have an explicit type; the type is infered from the
# requested information.
requests = {};

def request(ctx, flow):
    if not flow.match("~d pgorelease.nianticlabs.com"):
        return

    with decoded(flow.request):
        req = protocol.RequestEnvelope()
        req.ParseFromString(flow.request.content)

        if req.id in requests:
            ctx.log("Duplicate Request", req.id)

        requests[req.id] = queue.Queue()
        for request in req.requests:
            messageName = toCamelCase(protocol.Method.Name(request.method))
            requests[req.id].put(messageName)

            if args.filter and messageName not in args.filter:
                continue

            if args.ignore and messageName in args.ignore:
                continue

            messageName += "Request"

            print("Request: (%s, %s)" % (messageName, request.method))
            if not request.payload:
                continue

            if args.always_raw:
                print("Request: Raw (type: %s) (name: %s)" %
                    (request.method, messageName))
                printRawMessage(request.payload)

            else:
                try:
                    MessageType = getattr(protocol, messageName)
                    Message = MessageType()
                    Message.ParseFromString(request.payload)
                    print(Message)

                except:
                    print("Request: Unknown Message (name: %s)" % messageName)
                    printRawMessage(request.payload)

def response(ctx, flow):
    if not flow.match("~d pgorelease.nianticlabs.com"):
        return

    with decoded(flow.response):
        resp = protocol.ResponseEnvelope()
        resp.ParseFromString(flow.response.content)

        i = -1
        while not requests[resp.id].empty():
            i += 1
            requestName = requests[resp.id].get()
            if args.filter and requestName not in args.filter:
                continue

            if args.ignore and requestName in args.ignore:
                continue

            request = requestName + "Response"

            print("Response: (%s)" % request)
            if not resp.responses[i]:
                continue

            if args.always_raw:
                print("Response: Unknown Message (name: %s)"
                    % request)
                printRawMessage(resp.responses[i])

            else:
                try:
                    MessageType = getattr(protocol, request)
                    Message = MessageType()
                    Message.ParseFromString(resp.responses[i])
                    print(Message)

                except:
                    print("Response: Unknown Message (name: %s)"
                        % request)
                    printRawMessage(resp.responses[i])

        del requests[resp.id]

def start(ctx, argv):
    global args
    parser = argparse.ArgumentParser(
        description="A tool for reverse engineering and viewing pokemon go messages."
    )
    rawGroup = parser.add_mutually_exclusive_group()
    rawGroup.add_argument("--no-raw",
        help="Disable printing raw messages",
        action='store_true',
        default=False
    )
    rawGroup.add_argument("--always-raw",
        help="Ignore proto files and decode as raw message",
        action='store_true',
        default=False
    )

    filterGroup = parser.add_mutually_exclusive_group()
    filterGroup.add_argument("--filter",
        help="Only request names specified with this flag will be shown",
        nargs="+",
        type=str,
    )
    filterGroup.add_argument("--ignore",
        help="Request names specified with this flag will be removed",
        nargs="+",
        type=str,
    )

    args = parser.parse_args(argv[1:])

# Conditionally prints a protobuf to stdout using protoc --decode-raw
def printRawMessage(encoded):
    if args.no_raw:
        return

    protoc = subprocess.Popen(
        ['protoc', '--decode_raw'],
        stdin=subprocess.PIPE, stdout=sys.stdout
    )
    protoc.communicate(input=encoded)

# Converts functions from snake case to upper camel case.
def toCamelCase(string):
    string = string.lower()
    pieces = string.split("_")
    return "".join(piece.title() for piece in pieces)

