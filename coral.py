#!/usr/bin/env python3

# Coral - Backend for Storehaus, a web-based CC:Tweaked inventory management system.

import flask, flask_sock, threading, random, os, json, time

app = flask.Flask(__name__)
sock = flask_sock.Sock(app)

DB = {
    'clusters': {
        "testing": {
            "nodes": {
                
            }
        }
    }
}
JOIN_KEY = '$f$cbfe$$afa$ef$'
def generateStorageID():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))

@sock.route('/fishConnect')
def fishConnect(ws):
    ws.send('0')

    cluster = ws.receive()
    if cluster not in DB['clusters']:
        ws.send('-1')
        ws.close()
        return
    ws.send('2')

    node = ws.receive()
    if node not in DB["clusters"]["nodes"] and node != '8':
        ws.send('-2')
        ws.close()
        return

    if r == '8':
        ws.send('9')
        r = ws.receive()
        if r != JOIN_KEY:
            ws.send('-8')
            ws.close()
            return
        storageID = generateStorageID()
        DB["clusters"][cluster]["nodes"][storageID] = {
            "ws": ws,
            "lastPing": time.time(),
            "inventories": {}
        }
        ws.send(storageID)
    ws.send('3')
    while True:
        c = ws.receive()
        cj = {}
        try:
            cj = json.loads(c)
        except:
            ws.send('-3')
            ws.close()
            return
        if cj['type'] == 'IndexInventories':
            DB["clusters"][cluster]["nodes"][node]["inventories"] = cj['inventories']
            ws.send('4')
        elif cj['type'] == "UpdateInv":
            DB["clusters"][cluster]["nodes"][node]["inventories"][cj['invID']] = cj['inv']
            ws.send('4')
        elif cj['type'] == "Ping":
            DB["clusters"][cluster]["nodes"][node]["lastPing"] = time.time()
            ws.send('4')
        else:
            ws.send('?')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7567)
