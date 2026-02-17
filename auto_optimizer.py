#!/usr/bin/env python3
"""
Otimizador Automático de Pesos e Contra-pesos - Protocolo Severino
Ajusta automaticamente parâmetros do sistema baseado em performance
"""
import time
import json
import logging
import sqlite3
from datetime import datetime, timedelta
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - AUTO_OPTIMIZER - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_optimizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AutoOptimizer")

class AutoOptimizer:
    def __init__(self):
        self.db_path = 'sniper_brain.db'
        self.config_file = 'optimizer_config.json'
        self.load_config()
        
        # Métricas de performance
        self.performance_history = []
        self.max_history_size = 100
        
    def load_config(self):
        """Carregar ou criar configuração padrão"""
        default_config = {
            # Pesos para decisões do brain
            'brain_weights': {
                'pattern_confidence': 0.3,
                'market_context': 0.2,
                'historical_success': 0.25,
                'risk_adjustment': 0.15,
                'volume_signal': 0.1
            },
            
            # Limiares de confiança
            'confidence_thresholds': {
                'high_confidence': 0.75,
                'medium_confidence': 0.55,
                'low_confidence': 0.35
            },
            
            # Ajustes de risco
            'risk_adjustments': {
                'max_position_size': 0.05,  # 5% do capital por trade
                'stop_loss_multiplier': 1.5,
                'take_profit_multiplier': 2.0,
                'volatility_adjustment': 0.8
            },
            
            # Parâmetros de aprendizado
            'learning_params': {
                'learning_rate': 0.001,
                'discount_factor': 0.95,
                'exploration_rate': 0.1,
                'batch_size': 64,
                'memory_size': 10000
            },
            
            # Otimização automática
            'auto_optimize': True,
            'optimize_interval_hours': 6,
            'last_optimization': 0
        }
        
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
                logger.info("✅ Configuração carregada")
        except:
            self.config = default_config
            self.save_config()
            logger.info("✅ Configuração padrão criada")
    
    def save_config(self):
        """Salvar configuração atual"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info("💾 Configuração salva")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar configuração: {e}")
    
    def calculate_performance_metrics(self, hours_back=24):
        """Calcular métricas de performance recentes"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = int((time.time() - hours_back * 3600))
            
            # Buscar trades recentes
            cursor.execute('''
                SELECT trade_result, reward, pnl_real, confidence
                FROM raw_samples 
                WHERE trade_result IS NOT NULL 
                AND created_at > ?
                ORDER BY created_at DESC
            ''', (cutoff_time,))
            
            trades = cursor.fetchall()
            conn.close()
            
            if not trades:
                logger.warning(f"⚠️  Nenhum trade encontrado nas últimas {hours_back}h")
                return None
            
            # Calcular métricas
            total_trades = len(trades)
            wins = sum(1 for t in trades if t[0] == 'WIN')
            losses = sum(1 for t in trades if t[0] == 'LOSS')
            break_even = sum(1 for t in trades if t[0] == 'BREAKEVEN')
            
            win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
            avg_reward = np.mean([t[1] for t in trades if t[1] is not None]) if trades else 0
            total_pnl = sum(t[2] for t in trades if t[2] is not None)
            avg_confidence = np.mean([t[3] for t in trades if t[3] is not None and t[3] > 0]) if trades else 0
            
            metrics = {
                'timestamp': int(time.time()),
                'period_hours': hours_back,
                'total_trades': total_trades,
                'wins': wins,
                'losses': losses,
                'break_even': break_even,
                'win_rate': win_rate,
                'avg_reward': avg_reward,
                'total_pnl': total_pnl,
                'avg_confidence': avg_confidence,
                'sharpe_ratio': self.calculate_sharpe_ratio(trades),
                'max_drawdown': self.calculate_max_drawdown(trades)
            }
            
            # Adicionar ao histórico
            self.performance_history.append(metrics)
            if len(self.performance_history) > self.max_history_size:
                self.performance_history.pop(0)
            
            logger.info(f"📈 Performance ({hours_back}h): "
                       f"Win Rate: {win_rate:.1f}% | "
                       f"Avg Reward: {avg_reward:.3f} | "
                       f"Trades: {total_trades}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Erro ao calcular métricas: {e}")
            return None
    
    def calculate_sharpe_ratio(self, trades):
        """Calcular Sharpe Ratio simplificado"""
        try:
            rewards = [t[1] for t in trades if t[1] is not None]
            if len(rewards) < 2:
                return 0
            
            avg_reward = np.mean(rewards)
            std_reward = np.std(rewards)
            
            if std_reward == 0:
                return 0
            
            # Sharpe Ratio anualizado (assumindo 365 trades/ano)
            sharpe = (avg_reward / std_reward) * np.sqrt(365)
            return float(sharpe)
        except:
            return 0
    
    def calculate_max_drawdown(self, trades):
        """Calcular máximo drawdown"""
        try:
            pnls = [t[2] for t in trades if t[2] is not None]
            if not pnls:
                return 0
            
            cumulative = np.cumsum(pnls)
            peak = np.maximum.accumulate(cumulative)
            drawdown = (cumulative - peak) / (peak + 1e-10)  # Evitar divisão por zero
            
            max_drawdown = np.min(drawdown) * 100  # Em percentual
            return float(max_drawdown)
        except:
            return 0
    
    def optimize_weights(self, performance_metrics):
        """Otimizar pesos automaticamente baseado em performance"""
        if not performance_metrics:
            logger.warning("⚠️  Sem métricas para otimização")
            return False
        
        try:
            win_rate = performance_metrics['win_rate']
            sharpe_ratio = performance_metrics['sharpe_ratio']
            max_drawdown = abs(performance_metrics['max_drawdown'])
            
            logger.info(f"🔧 Otimizando pesos: "
                       f"WR: {win_rate:.1f}% | "
                       f"Sharpe: {sharpe_ratio:.2f} | "
                       f"DD: {max_drawdown:.1f}%")
            
            # Ajustar pesos baseado em performance
            weights = self.config['brain_weights'].copy()
            
            # Se win rate está baixo, dar mais peso ao contexto de mercado
            if win_rate < 40:
                weights['market_context'] = min(0.3, weights['market_context'] * 1.2)
                weights['risk_adjustment'] = min(0.25, weights['risk_adjustment'] * 1.1)
                logger.info("   📉 Win rate baixa → ↑ Peso contexto mercado e risco")
            
            # Se Sharpe ratio está bom, manter confiança no padrão
            if sharpe_ratio > 1.0:
                weights['pattern_confidence'] = min(0.4, weights['pattern_confidence'] * 1.1)
                logger.info("   📈 Sharpe bom → ↑ Peso confiança padrão")
            
            # Se drawdown está alto, aumentar ajuste de risco
            if max_drawdown > 20:
                weights['risk_adjustment'] = min(0.3, weights['risk_adjustment'] * 1.3)
                weights['pattern_confidence'] = max(0.2, weights['pattern_confidence'] * 0.9)
                logger.info("   ⚠️  Drawdown alto → ↑ Peso risco, ↓ Peso confiança")
            
            # Normalizar pesos para soma = 1
            total = sum(weights.values())
            weights = {k: v/total for k, v in weights.items()}
            
            # Atualizar configuração
            self.config['brain_weights'] = weights
            self.config['last_optimization'] = int(time.time())
            
            # Ajustar limiares de confiança
            self.adjust_confidence_thresholds(performance_metrics)
            
            # Ajustar parâmetros de aprendizado
            self.adjust_learning_params(performance_metrics)
            
            self.save_config()
            
            logger.info(f"✅ Pesos otimizados: {weights}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na otimização: {e}")
            return False
    
    def adjust_confidence_thresholds(self, metrics):
        """Ajustar limiares de confiança automaticamente"""
        win_rate = metrics['win_rate']
        avg_confidence = metrics['avg_confidence']
        
        thresholds = self.config['confidence_thresholds'].copy()
        
        # Se win rate alta mas confiança média baixa, ajustar limiares
        if win_rate > 60 and avg_confidence < 0.6:
            thresholds['high_confidence'] = max(0.65, thresholds['high_confidence'] * 0.95)
            thresholds['medium_confidence'] = max(0.45, thresholds['medium_confidence'] * 0.95)
            logger.info("   🎯 Ajustando limiares: WR alta + Conf baixa → ↓ Limiares")
        
        # Se win rate baixa mas confiança alta, aumentar limiares
        elif win_rate < 40 and avg_confidence > 0.7:
            thresholds['high_confidence'] = min(0.85, thresholds['high_confidence'] * 1.05)
            thresholds['medium_confidence'] = min(0.65, thresholds['medium_confidence'] * 1.05)
            logger.info("   🎯 Ajustando limiares: WR baixa + Conf alta → ↑ Limiares")
        
        self.config['confidence_thresholds'] = thresholds
    
    def adjust_learning_params(self, metrics):
        """Ajustar parâmetros de aprendizado"""
        win_rate = metrics['win_rate']
        sharpe_ratio = metrics['sharpe_ratio']
        
        params = self.config['learning_params'].copy()
        
        # Se performance está boa, reduzir exploration (exploit mais)
        if win_rate > 55 and sharpe_ratio > 0.5:
            params['exploration_rate'] = max(0.05, params['exploration_rate'] * 0.9)
            logger.info("   🧠 Performance boa → ↓ Exploration rate")
        
        # Se performance está ruim, aumentar exploration (explore mais)
        elif win_rate < 35 or sharpe_ratio < 0:
            params['exploration_rate'] = min(0.3, params['exploration_rate'] * 1.2)
            params['learning_rate'] = min(0.01, params['learning_rate'] * 1.1)
            logger.info("   🧠 Performance ruim → ↑ Exploration e Learning rate")
        
        # Ajustar batch size baseado no número de trades
        if metrics['total_trades'] > 50:
            params['batch_size'] = min(128, params['batch_size'] * 1.5)
        
        self.config['learning_params'] = params
    
    def optimize_risk_parameters(self):
        """Otimizar parâmetros de risco"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Analisar performance de diferentes tamanhos de posição
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN pnl_real > 2 THEN 'large_win'
                        WHEN pnl_real > 0 THEN 'small_win'
                        WHEN pnl_real < -2 THEN 'large_loss'
                        ELSE 'small_loss'
                    END as pnl_category,
                    COUNT(*) as count
                FROM raw_samples 
                WHERE pnl_real IS NOT NULL
                GROUP BY pnl_category
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            # Calcular proporções
            categories = {cat: count for cat, count in results}
            total = sum(categories.values())
            
            if total == 0:
                return
            
            # Se muitas perdas grandes, reduzir tamanho de posição
            large_loss_ratio = categories.get('large_loss', 0) / total
            if large_loss_ratio > 0.3:  # Mais de 30% são perdas grandes
                self.config['risk_adjustments']['max_position_size'] *= 0.8
                logger.info(f"   ⚠️  Muitas perdas grandes ({large_loss_ratio:.0%}) → ↓ Tamanho posição")
            
            # Se muitas vitórias pequenas, aumentar take profit
            small_win_ratio = categories.get('small_win', 0) / total
            if small_win_ratio > 0.4:  # Mais de 40% são vitórias pequenas
                self.config['risk_adjustments']['take_profit_multiplier'] *= 1.1
                logger.info(f"   📈 Muitas vitórias pequenas ({small_win_ratio:.0%}) → ↑ Take profit")
            
            self.save_config()
            
        except Exception as e:
            logger.error(f"❌ Erro ao otimizar risco: {e}")
    
    def run_continuous_optimization(self, interval_hours=6):
        """Executar otimização contínua"""
        logger.info(f"🚀 Iniciando otimização contínua (intervalo: {interval_hours}h)")
        
        while True:
            try:
                # Verificar se está habilitado
                if not self.config.get('auto_optimize', True):
                    logger.info("ℹ️  Otimização automática desabilitada")
                    time.sleep(interval_hours * 3600)
                    continue
                
                # Verificar intervalo
                last_opt = self.config.get('last_optimization', 0)
                time_since_last = time.time() - last_opt
                
                if time_since_last < interval_hours * 3600:
                    sleep_time = interval_hours * 3600 - time_since_last
                    logger.info(f"⏳ Próxima otimização em {sleep_time/3600:.1f}h")
                    time.sleep(min(sleep_time, 3600))  # Máximo 1 hora
                    continue
                
                # Executar otimização
                logger.info("🔄 Executando ciclo de otimização...")
                
                # 1. Calcular métricas
                metrics = self.calculate_performance_metrics(hours_back=48)
                
                # 2. Otimizar pesos
                if metrics:
                    self.optimize_weights(metrics)
                    
                    # 3. Otimizar parâmetros de risco
                    self.optimize_risk_parameters()
                    
                    # 4. Logar resultados
                    self.log_optimization_results(metrics)
                else:
                    logger.warning("⚠️  Sem métricas para otimização")
                
                # Aguardar próximo ciclo
                logger.info(f"✅ Ciclo de otimização completo. Próximo em {interval_hours}h")
                time.sleep(interval_hours * 3600)
                
            except KeyboardInterrupt:
                logger.info("🛑 Otimização interrompida pelo usuário")
                break
            except Exception as e:
                logger.error(f"❌ Erro no ciclo de otimização: {e}")
                time.sleep(3600)  # Esperar 1h antes de retry
    
    def log_optimization_results(self, metrics):
        """Logar resultados da otimização"""
        try:
            results = {
                'timestamp': int(time.time()),
                'metrics': metrics,
                'config': self.config,
                'performance_history': self.performance_history[-10:]  # Últimas 10 entradas
            }
            
            with open('optimization_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info("💾 Resultados da otimização salvos")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resultados: {e}")

def main():
    """Função principal"""
    print("⚙️
