from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "Discord Bot Voltage - SlashCMD update, is sussefully online! \n Progress 100% \n latency: n/a"

def run():
    app.run(host="0.0.0.0", port=0000)
    
def keep_alive():
    server = Thread(target=run)
    server.start()