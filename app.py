from flask import Flask, jsonify
import subprocess

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

