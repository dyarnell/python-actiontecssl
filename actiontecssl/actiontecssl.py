import socket
import ssl
import sys
import logging

log = logging.getLogger(__name__)

CR = b'\r'
LF = b'\n'
CRLF = CR + LF

IFSTAT_FIELDS = '''
    rx_bytes rx_packets rx_errs rx_drop rx_fifo rx_frame rx_compressed rx_multicast
    tx_bytes tx_packets tx_errs tx_drop tx_fifo tx_colls tx_carrier tx_compressed
    '''.split()

class ActiontecSSL(object):
    def __init__(self, password, host='192.168.1.1', port=992,
                 username='admin', timeout=1):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

    def connect(self):
        self.connection = None
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.settimeout(self.timeout)
            self.connection = ssl.wrap_socket(self.connection,
                                              ssl_version=ssl.PROTOCOL_SSLv23)
            self.connection.connect((self.host, self.port))
        except ssl.SSLError:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.settimeout(self.timeout)
            self.connection.connect((self.host, self.port))
        except Exception as e:
            sys.exit(e)
        # login, there is some garbage as the beginging of the connection
        garbage = self._recieve()
        self._send(self.username)
        username_out = self._recieve()
	log.debug(username_out)
        self._send(self.password)
        password_out = self._recieve()
        log.debug(password_out)
        # detect the current prompt
        self.prompt = password_out.split('\n')[-1]
        log.info('Finished setting up connection.')

    def _send(self, text):
        self.connection.send(text.encode() + CRLF)

    def _recieve(self, read_bytes=512):
        r = self.connection.recv(read_bytes)[:-2]
        log.debug(r)
        return r

    def run(self, cmd):
        if self.connection is not None:
             self._send(cmd)
             recv = self._recieve()
             while not recv.endswith(self.prompt):
                 recv += '\n' + self._recieve()
             return recv[:-len(self.prompt)]
        else:
             log.error('Connection not made for %s' % self.__class__.__name__)
             return None

    def ifstats(self):
        res = self.run('system cat /proc/net/dev')

        devices = {}
        for line in res.split('\n'):
            if ':' in line:
                iface, stats = [x.strip() for x in line.split(':')]
                devices[iface] = dict(zip(IFSTAT_FIELDS,
                    [int(x) for x in stats.split()]))

        return devices

    def loadavg(self):
        res = self.run('kernel cpu_load_avg')
        state = 0

        for line in res.split('\n'):
            if state == 0:
                if line.startswith('1 Min.'):
                    state = 1
            elif state == 1:
                loadavg = line.split()
                break

        return [float(x) for x in loadavg]

    def meminfo(self):
        res = self.run('kernel meminfo')
        meminfo = {}

        for line in res.split('\n'):
            if line.startswith('Memory info:'):
                pass
            elif ':' in line:
                k = line.split(':')[0]
                v = line.split(':')[1].split()[0]
                meminfo[k] = int(v)

        return meminfo

    def processes(self):
        res = self.run('kernel top')
        state = 0
        processes = []

        for line in res.split('\n'):
            if state == 0:
                if line.startswith('Command'):
                    state = 1
            elif state == 1:
                if len(line.split()) > 1:
                    processes.append(line.split()[0])

        return processes

    def cpus(self):
        res = self.run('system cat /proc/cpuinfo')

        cpus = []
        cpu = {}
        for line in res.split('\n'):
            if not ':' in line:
                continue
            elif ':' in line:
                k,v = [x.strip() for x in line.split(':')]
                if k == 'system type':
                    continue
                elif k == 'processor' and cpu:
                    cpus.append(cpu)
                    cpu = {}

                cpu[k] = v

        if cpu:
            cpus.append(cpu)

        return cpus

