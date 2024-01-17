from flask import Flask, jsonify, request
import subprocess
import netifaces as ni

app = Flask(__name__)

@app.route('/network_info', methods=['GET'])
def get_network_info():
    # Assuming 'eth0' as the primary interface
    interface = 'eth0'
    print(f"Fetching network info for interface: {interface}")
    try:
        mac_address = ni.ifaddresses(interface)[ni.AF_LINK][0]['addr']
        ip_address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        print(f"MAC: {mac_address}, IP: {ip_address}")
        return jsonify({'mac_address': mac_address, 'ip_address': ip_address})
    except KeyError:
        error_message = 'Unable to fetch network information'
        print(error_message)
        return jsonify({'error': error_message}), 500

def execute_ping(host):
    print(f"Pinging {host}...")
    try:
        output = subprocess.check_output(["ping", "-c", "1", host], stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"Ping output: {output}")
        return output
    except subprocess.CalledProcessError as e:
        error_message = f"Ping failed: {e.output}"
        print(error_message)
        return error_message

@app.route('/ping', methods=['GET'])
def ping():
    hosts = request.args.get('hosts', '169.254.130.1')  # Default hosts to ping
    results = {}
    for host in hosts.split(','):
        print(f"Received ping request for host: {host}")
        results[host] = execute_ping(host)
    return jsonify(results)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=80)
