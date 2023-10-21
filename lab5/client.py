import argparse
import http.client

def send_get_request(host, port, path):
    connection = http.client.HTTPConnection(host, port)
    connection.request("GET", path)
    response = connection.getresponse()
    print(f"Response status: {response.status}")
    print(f"Response headers: {response.getheaders()}")
    body = response.read().decode()
    print(f"Response body: {body}")
    connection.close()

def send_post_request(host, port, path, data):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    connection = http.client.HTTPConnection(host, port)
    connection.request("POST", path, data, headers)
    response = connection.getresponse()
    print(f"Response status: {response.status}")
    print(f"Response headers: {response.getheaders()}")
    body = response.read().decode()
    print(f"Response body: {body}")
    connection.close()

def parse_args():
    parser = argparse.ArgumentParser(description='HTTP Client with command line arguments.')
    parser.add_argument('-H', '--host', required=True, help='Server host')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Server port')
    parser.add_argument('-P', '--path', default='/', help='Request path')
    parser.add_argument('-m', '--method', default='GET', help='HTTP method (GET or POST)')
    parser.add_argument('-d', '--data', help='Data to send in POST request')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    if args.method == 'GET':
        send_get_request(args.host, args.port, args.path)
    elif args.method == 'POST':
        if not args.data:
            print("Error: POST request requires data. Use the -d option.")
        else:
            send_post_request(args.host, args.port, args.path, args.data)
