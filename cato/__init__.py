from mcdreforged.api.all import *

from subprocess import Popen, PIPE, STDOUT
from http.server import HTTPServer, BaseHTTPRequestHandler
import traceback
import urllib
import socket
import time
import json
import re


default_config = {
    'token': None,
    'name': 'A Minecraft Server',
    'port': 25565
}

HELP_MESSAGE = '''
------ MCDR BOT ------
命令帮助如下:
§7!!cato id§r: 获取 ID
§7!!cato code§r: 获取联机码
§7!!cato token §b<token>§r：更换 token
见配置文件以了解更多设置
'''.strip()

Prefix = '!!cato'


class HttpHandler(BaseHTTPRequestHandler):
    def _response(self, path, args):
        global id, config
        code=200
        rtv=None
        try:
            if path == '/':
                rtv = 'Cato 已启动'
            elif path == '/id':
                rtv = str(id)
            elif path == '/code':
                rtv = str(id) + '#' + str(50000)
            else:
                code = 404
                rtv = '404'
        except Exception as e:
            rtv = '服务器错误：' + str(e) + '\n' + traceback.format_exc()
        self.send_response(code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(rtv.encode("utf-8"))

    def do_GET(self):
        path, args = urllib.parse.splitquery(self.path)
        self._response(path, args)


@new_thread
def StartCato(server, Token, Port):
    global proc, config
    GetID = False
    command = 'plugins/cato -token ' + str(Token)
    proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True)
    MonitorCato(server, Token, Port)
    try:
        for line in iter(proc.stdout.readline, b''):
            output = str(line, encoding='utf-8')
            msg = output.split('\"')
            if len(msg) > 3:
                if re.match('Initialization complete: id', msg[3]) and not GetID:
                    global id
                    id = msg[3].split('(')[1].split(')')[0].split(':')[0]
                    GetID = True
                    server.logger.info('Cato Start!')
                    server.logger.info('Link ID: ' + str(id))
                    server.logger.info('Link Code: ' + str(id) + '#' + str(50000))
                    proc.stdin.write(str('ufw net open 127.0.0.1:26666\n').encode("utf-8"))
                    proc.stdin.write(str('ufw net open 127.0.0.1:50000\n').encode("utf-8"))
                    proc.stdin.write(str('ufw net open 127.0.0.1:' + str(Port) + '\n').encode("utf-8"))
                if re.match('Reconnecting to main net try', msg[3]):
                    GetID = False
                if re.match('Connection request from peer id', msg[3]):
                    server.logger.info('ID: ' + str(msg[3].split('(')[1].split(')')[0]) + ' try to connect. IP:' + str(msg[3].split('(')[2].split(')')[0]))
    except Exception as e:
        server.logger.error('Cato Start Error')
        server.logger.error(traceback.print_exc())
        proc.kill()
        StartCato(server, Token, Port)


@new_thread
def MonitorCato(server, Token, Port):
    global proc
    proc.wait()
    proc.kill()
    server.logger.error('Cato Stop!')
    server.logger.error('Wait 3 second to Start Cato!')
    time.sleep(3)
    if proc.returncode != None and proc.returncode != -9:
        StartCato(server, Token, Port)


@new_thread
def StartMultiplayerServer(server):
    global s
    s = socket.socket()
    s.bind(('127.0.0.1', 50000))
    s.listen(200)
    server.logger.info('Start Multiplayer Server in 127.0.0.1:50000')
    while True:
        client, addr = s.accept()
        HandleClient(server, client)
        server.logger.info('Try Connect')


@new_thread
def HandleClient(server, client):
    global config
    msg = str(client.recv(256), encoding='utf-8')
    if 'handshake' in msg:
        data = {
            'type': 'handshake'
        }
        client.send(str(json.dumps(data) + '\r\n').encode("utf-8"))
        server.logger.info('Handshake')
    if 'join' in msg:
        data = {
            'sessionName': config['name'],
            'port': config['port'],
            'type': 'join'
        }
        client.send(str(json.dumps(data) + '\r\n').encode("utf-8"))
        server.logger.info('Accept Request')
    while True:
        try:
            msg = str(client.recv(64), encoding='utf-8')
            if 'keepalive' in msg:
                t = int(time.time() * 1000)
                data = {
                    'timestamp': t,
                    'type': 'keepalive'
                }
                client.send(str(json.dumps(data) + '\r\n').encode("utf-8"))
        except Exception:
            client.close()


@new_thread
def StartAPI(server):
    global httpd
    httpd = HTTPServer(('127.0.0.1', 26666), HttpHandler)
    server.logger.info('API is listenning in: http://127.0.0.1:26666')
    httpd.serve_forever()


def send_help(source: CommandSource):
    source.reply(HELP_MESSAGE)


def GetID(source: CommandSource):
    global id
    source.reply(RText('Link ID: ', RColor.red) + RText(str(id), RColor.gold).h('Cato 联机 ID').c(action=RAction.suggest_command, value=str(id)))


def GetCode(source: CommandSource):
    global id, config
    code = str(id) + '#' + str(50000)
    source.reply(RText('Link code: ', RColor.red) + RText(code, RColor.gold).h('联机码').c(action=RAction.copy_to_clipboard, value=code))


def ChangeToken(source: CommandSource, token):
    global config, port, proc
    if source.get_permission_level() >= 3:
        if token == None or token == 'new' or token == '':
            config['token'] = ''
        else:
            config['token'] = token
        source.get_server().as_plugin_server_interface().save_config_simple(config=config, file_name='config.json')
        proc.kill()
        StartCato(source.get_server(), token, port)
        source.reply('Token has changed to ' + token)
    else:
        source.reply('No Permission')


def on_server_startup(server: ServerInterface):
    global id, config
    StartMultiplayerServer(server)
    server.logger.info('API is listenning in: http://127.0.0.1:26666')
    server.logger.info('Link ID: ' + str(id))
    server.logger.info('Link Code: ' + str(id) + '#' + str(50000))


def on_load(server: PluginServerInterface, prev_module):
    global config, port
    config = server.load_config_simple(file_name='config.json', default_config=default_config)
    port = config['port']
    server.register_help_message(Prefix, 'Cato 联机相关指令')
    server.register_command(
        Literal(Prefix).
        runs(send_help).
        then(Literal('id').runs(GetID)).
        then(Literal('code').runs(GetCode)).
        then(Literal('token').
            then(Text('token').runs(lambda src, ctx: ChangeToken(src, ctx['token'])))
        )
    )

    if config['token'] == None or config['token'] == 'new' or config['token'] == '':
        StartCato(server, 'new', port)
    else:
        StartCato(server, config['token'], port)
    StartAPI(server)


def on_unload(server: ServerInterface):
    global proc, httpd, s
    httpd.server_close()
    proc.kill()
    server.logger.info('All Stop!')
