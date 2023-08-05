#!/usr/bin/env python3
import argparse
import collections
import json
import subprocess
import sys

version = '0.0.2'


class Docker:

    @staticmethod
    def inspect(container_ids):
        result = subprocess.run(
            ['docker', 'inspect', *container_ids],
            stdout=subprocess.PIPE,
            check=True
        )
        return json.loads(result.stdout.decode().strip())


class DockerCompose:

    @staticmethod
    def container_ids():
        result = subprocess.run(
            ['docker-compose', 'ps', '-aq'],
            stdout=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode().splitlines()


def host_ports(container_ids):
    tcp_ports = collections.defaultdict(dict)
    udp_ports = collections.defaultdict(dict)
    for container in Docker.inspect(container_ids):
        name = container['Config']['Labels']['com.docker.compose.service']

        for container_port, host_ports in container['NetworkSettings']['Ports'].items():
            port, protocol = container_port.split('/')
            port = int(port)
            if host_ports:
                host_port = int(host_ports[0]['HostPort'])
                if protocol == 'tcp':
                    tcp_ports[name][port] = host_port
                elif protocol == 'udp':
                    udp_ports[name][port] = host_port

    return dict(tcp_ports), dict(udp_ports)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=version)
    parser.parse_args()

    container_ids = DockerCompose.container_ids()
    if not container_ids:
        sys.stderr.write('error: no containers running')
        sys.exit(1)

    tcp_ports, udp_ports = host_ports(container_ids)

    env = []
    for service, ports in tcp_ports.items():
        service = service.upper().replace('-', '_')
        for container_port, host_port in ports.items():
            env.append(f'export {service}_TCP_{container_port}={host_port}')
    for service, ports in udp_ports.items():
        service = service.upper().replace('-', '_')
        for container_port, host_port in ports.items():
            env.append(f'export {service}_UDP_{container_port}={host_port}')

    print('\n'.join(sorted(env)))


if __name__ == '__main__':
    main()
