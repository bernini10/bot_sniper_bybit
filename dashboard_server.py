from flask import Flask, render_template, jsonify
import json
import os
import ccxt
import time
from datetime import datetime
from lib_utils import JsonManager

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configs
WATCHLIST_FILE = os.path.join(BASE_DIR, 'watchlist.json')
HISTORY_FILE = os.path.join(BASE_DIR, 'trades_history.json')
watchlist_mgr = JsonManager(WATCHLIST_FILE)

def get_secrets():
    secrets = {}
    try:
        path_env = os.path.join(BASE_DIR, '.env')
        if os.path.exists(path_env):
            with open(path_env, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, val = line.strip().split('=', 1)
                        secrets[key] = val
    except: pass
    return secrets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    secrets = get_secrets()
    data = {
        'equity': 0, 'available': 0, 'pnl_today': 0, 
        'open_positions': []
    }
    
    if secrets.get('BYBIT_API_KEY'):
        try:
            exchange = ccxt.bybit({
                'apiKey': secrets['BYBIT_API_KEY'],
                'secret': secrets['BYBIT_SECRET'],
                'options': {'defaultType': 'linear'}
            })
            bal = exchange.fetch_balance()
            data['equity'] = bal['USDT']['total']
            data['available'] = bal['USDT']['free']
            
            # Posições Abertas
            positions = exchange.fetch_positions()
            for p in positions:
                if float(p['contracts']) > 0:
                    data['open_positions'].append({
                        'symbol': p['symbol'],
                        'side': p['side'],
                        'size': float(p['contracts']),
                        'entry': float(p['entryPrice']),
                        'pnl': float(p['unrealisedPnl']),
                        'leverage': p['leverage']
                    })
        except Exception as e:
            print(f"Erro API: {e}")
            
    return jsonify(data)

@app.route('/api/watchlist')
def get_watchlist():
    wl = watchlist_mgr.read()
    if not wl: return jsonify([])
    
    # Adicionar preço atual para calcular distancia
    secrets = get_secrets()
    if secrets.get('BYBIT_API_KEY'):
        try:
            exchange = ccxt.bybit({'apiKey': secrets['BYBIT_API_KEY'], 'secret': secrets['BYBIT_SECRET']})
            # Fetch tickers for all symbols in watchlist
            if wl.get('pares'):
                symbols = [p['symbol'] for p in wl['pares']]
                # Optimization: fetch all needed tickers at once if possible, or loop
                # Bybit v5 supports multiple tickers? fetchTickers(['BTC/USDT', ...])
                try:
                    tickers = exchange.fetch_tickers(symbols)
                    for p in wl['pares']:
                        sym = p['symbol']
                        if sym in tickers:
                            p['current_price'] = tickers[sym]['last']
                            # Calc % distance
                            dist = abs(p['current_price'] - p['neckline']) / p['current_price'] * 100
                            p['dist_pct'] = round(dist, 2)
                except: pass
        except: pass
            
    return jsonify(wl.get('pares', []))

@app.route('/api/history')
def get_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                return jsonify(json.load(f))
    except: pass
    return jsonify([])

@app.route('/api/logs')
def get_logs():
    # Lê as ultimas 50 linhas combinadas
    log_data = []
    files = ['scanner_bybit.log', 'monitor_bybit.log', 'executor_bybit.log']
    
    for log_file in files:
        path = os.path.join(BASE_DIR, log_file)
        if os.path.exists(path):
            with open(path, 'r') as f:
                lines = f.readlines()[-20:] # Ultimas 20 de cada
                for line in lines:
                    log_data.append(f"[{log_file.split('_')[0].upper()}] {line.strip()}")
    
    return jsonify(log_data)

if __name__ == '__main__':
    # Roda na porta 8080 para evitar conflitos
    app.run(host='0.0.0.0', port=8080)
