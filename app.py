from flask import Flask, jsonify, request
import subprocess
import netifaces as ni


app = Flask(__name__)

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr.decode('utf-8').strip()}"

@app.route('/network_info', methods=['GET'])
def get_network_info():
    ip_addr_output = execute_command("ip addr")
    ip_neigh_output = execute_command("ip neigh")
    return jsonify({
        'ip_addr': ip_addr_output,
        'ip_neigh': ip_neigh_output
    })

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
    host = request.args.get('host', '169.254.131.3')  # Default host to ping
    print(f"Received ping request for host: {host}")
    result = execute_ping(host)
    return jsonify({'ping_result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

