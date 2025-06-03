#!/usr/bin/env python3
"""
Quantitative Financial Analysis System - Complete Implementation
"""

import argparse
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Non-interactive backend

# Import all required components
from src.data.loader import FinancialDataLoader
from src.data.processor import DataProcessor
from src.analysis.indicators import TechnicalIndicators, IndicatorConfig
from src.analysis.metrics import FinancialMetrics
from src.trading.signals import SignalType, SignalGenerator, SignalConfig
from src.trading.backtesting import Backtester
from src.analysis.visualization import TradingVisualizer

def validate_directory(path: str) -> Path:
    """Ensure output directory exists"""
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj

class FinancialAnalysisSystem:
    """Complete financial analysis pipeline"""
    
    def __init__(self, args):
        self.args = args
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        validate_directory(self.args.output)
        self.data_loader = FinancialDataLoader(data_dir=self.args.data_dir)  # Initialize data loader
    
    def _load_data(self, ticker: str) -> pd.DataFrame:
        """Load data for a single ticker"""
        self.logger.info(f"Loading data for {ticker}")
        try:
            data = self.data_loader.load_from_csv(ticker)
            
            if data.empty:
                raise ValueError(f"Empty DataFrame loaded for {ticker}")
                
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in required_columns):
                missing = [col for col in required_columns if col not in data.columns]
                raise ValueError(f"Missing required columns: {missing}")
                
            self.logger.debug(f"Loaded data shape: {data.shape}")
            return data
            
        except Exception as e:
            self.logger.error(f"Data loading failed for {ticker}: {str(e)}")
            raise
       
    def _load_config(self) -> Dict[str, Any]:
        """Load and validate configuration file"""
        config_path = Path(self.args.config)
    
        if not config_path.exists():
           self.logger.error(f"Config file not found: {config_path}")
           raise FileNotFoundError(f"Config file {config_path} does not exist")
    
        try:
           with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
           if not config:
              raise ValueError("Empty configuration file")
            
           # Validate required sections with default values if missing
           required_sections = {
                'indicators': {
                   'enabled': True,
                   'parameters': {
                     'rsi_period': 14,
                     'ma_short': 20,
                     'ma_long': 50,
                     'bb_period': 20,
                     'bb_std': 2.0,
                     'macd_fast': 12,
                     'macd_slow': 26,
                     'macd_signal': 9,
                     'overbought': 70,
                     'oversold': 30
                    }
                },
                'signals': {
                    'enabled': {
                        'rsi': True,
                        'macd': True,
                        'moving_average': True
                    },
                    'parameters': {}
                },
                'backtesting': {
                    'initial_capital': 100000,
                    'commission': 0.001,
                    'risk_free_rate': 0.02
                }
            }
        
           # Merge defaults with loaded config
           for section, default in required_sections.items():
               if section not in config:
                   self.logger.warning(f"Missing section {section}, using defaults")
                   config[section] = default
               else:
                   # Merge parameters recursively
                   if isinstance(default, dict):
                        for key, val in default.items():
                            if key not in config[section]:
                                config[section][key] = val
                                self.logger.info(f"Using default {key} in {section}")
                
           self.logger.info(f"Loaded config from {config_path}")
           return config
        
        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML in config: {str(e)}")
            raise
        except Exception as e:
           self.logger.error(f"Config loading failed: {str(e)}")
           raise
    
    def _process_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Clean and process raw data"""
        self.logger.info("Processing raw data")
        try:
            processor = DataProcessor(raw_data)
            processed = processor.handle_missing_data().get_processed_data()
            
            if processed.empty:
                raise ValueError("Data processing resulted in empty DataFrame")
                
            self.logger.debug(f"Processed data columns: {list(processed.columns)}")
            return processed
            
        except Exception as e:
            self.logger.error(f"Data processing failed: {str(e)}")
            raise
    
    def _calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        self.logger.info("Calculating technical indicators")
        try:
            indicator_config = IndicatorConfig(
               enabled=self.config['indicators']['enabled'],
               parameters=self.config['indicators']['parameters']
            )
            calculator = TechnicalIndicators(data, indicator_config)
            return calculator.calculate_enabled_indicators()
        
        except Exception as e:
            self.logger.error(f"Indicator calculation failed: {str(e)}")
            raise
    
    def _generate_signals(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Generate trading signals"""
        self.logger.info("Generating trading signals")
        try:
           # Verify config structure
           if 'signals' not in self.config:
               raise ValueError("Missing 'signals' section in config")
            
           signal_config = SignalConfig(
               enabled=self.config['signals']['enabled'],
               parameters=self.config['signals']['parameters']
            )
        
           generator = SignalGenerator(data, signal_config)
           return generator.generate_all_signals()
        
        except Exception as e:
            self.logger.error(f"Signal generation failed: {str(e)}")
            raise
    
    def _calculate_metrics(self, data: pd.DataFrame, signals: Dict[str, Any]) -> Dict[str, float]:
        """Calculate performance metrics"""
        self.logger.info("Calculating performance metrics")
        try:
            returns = data['Close'].pct_change().dropna()
            metrics = FinancialMetrics(returns, risk_free_rate=self.config['backtesting'].get('risk_free_rate', 0.02))
            return metrics.calculate_all()
        except Exception as e:
            self.logger.error(f"Metrics calculation failed: {str(e)}")
            raise
    
    def _run_backtest(self, data: pd.DataFrame, signals: Dict[str, Any]) -> Dict[str, Any]:
        """Execute backtesting"""
        self.logger.info("Running backtest")
        try:
            # Convert SignalType enum to strings
            signal_mapping = {
                'BUY': 'BUY',
                'SELL': 'SELL',
                'STRONG_BUY': 'BUY',
                'STRONG_SELL': 'SELL',
                'NEUTRAL': 'NEUTRAL'
            }
        
            # Handle both enum and string signal types
            if isinstance(signals['primary'].iloc[0], SignalType):
                signal_series = signals['primary'].map(lambda x: signal_mapping[x.name])
            else:
                # Fallback if signals are already strings
                signal_series = signals['primary'].map(signal_mapping.get, na_action='ignore')
        
            backtester = Backtester(
                prices=data['Close'],
                signals=signal_series,
                config=self.config['backtesting']
            )
            return backtester.run()
        
        except Exception as e:
            self.logger.error(f"Backtesting failed: {str(e)}")
            raise
    
    def _visualize_results(self, ticker: str, data: pd.DataFrame,
                         signals: Dict[str, Any], metrics: Dict[str, float],
                         backtest: Dict[str, Any]):
        """Generate and save visualizations"""
        self.logger.info("Generating visualizations")
        try:
            visualizer = TradingVisualizer(
                style=self.config['visualization'].get('style', 'seaborn')
            )
            
            # Create output directories
            plot_dir = Path(self.args.output) / "plots" / ticker
            report_dir = Path(self.args.output) / "reports"
            plot_dir.mkdir(parents=True, exist_ok=True)
            report_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate and save dashboard
            fig = visualizer.create_dashboard(
                price_data=data,
                signals=signals,
                metrics=metrics,
                backtest=backtest,
                ticker=ticker
            )
            fig.savefig(plot_dir / f"{ticker}_dashboard.png")
            plt.close(fig)
            
            # Generate and save report
            visualizer.save_report(
                data=data,
                metrics=metrics,
                signals=signals,
                backtest=backtest,
                output_dir=str(report_dir),
                ticker=ticker
            )
            
        except Exception as e:
            self.logger.error(f"Visualization failed: {str(e)}")
            raise
    
    def run_pipeline(self):
        """Execute complete analysis pipeline"""
        results = {}
        
        for ticker in self.args.tickers:
            try:
                self.logger.info(f"\n{'='*40}\nProcessing {ticker}\n{'='*40}")
                
                # 1. Data Loading
                raw_data = self._load_data(ticker)
                
                # 2. Data Processing
                processed_data = self._process_data(raw_data)
                
                # 3. Technical Analysis
                tech_data = self._calculate_indicators(processed_data)
                
                # 4. Signal Generation
                signals = self._generate_signals(tech_data)
                
                # 5. Performance Metrics
                metrics = self._calculate_metrics(tech_data, signals)
                
                # 6. Backtesting
                backtest_results = self._run_backtest(tech_data, signals)
                
                # 7. Visualization
                self._visualize_results(
                    ticker,
                    tech_data,
                    signals,
                    metrics,
                    backtest_results
                )
                
                results[ticker] = {
                    'data': tech_data,
                    'signals': signals,
                    'metrics': metrics,
                    'backtest': backtest_results
                }
                
            except Exception as e:
                self.logger.error(f"Failed processing {ticker}: {str(e)}", exc_info=True)
                continue
                
        return results

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Quantitative Financial Analysis System')
    parser.add_argument('--tickers', nargs='+', required=True,
                      help='List of tickers to analyze (e.g. AAPL MSFT)')
    parser.add_argument('--config', type=str, default='configs/analysis.yaml',
                      help='Path to configuration file')
    parser.add_argument('--output', type=str, default='results',
                      help='Output directory for results')
    parser.add_argument('--data-dir', type=str, default='data/raw',
                      help='Directory containing raw data files')
    parser.add_argument('--verbose', action='store_true',
                      help='Enable verbose logging')
    return parser.parse_args()

def setup_logging(verbose: bool = False):
    """Configure logging"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def main():
    """Main execution function"""
    args = parse_arguments()
    setup_logging(args.verbose)
    
    try:
        analysis_system = FinancialAnalysisSystem(args)
        results = analysis_system.run_pipeline()
        
        logging.info("\n" + "="*50)
        logging.info("Analysis completed successfully!")
        logging.info(f"Results saved to: {args.output}")
        
        # Print summary metrics for each ticker
        for ticker, result in results.items():
            logging.info(f"\n{ticker} Performance Summary:")
            for metric, value in result['metrics'].items():
                logging.info(f"{metric:>20}: {value:.4f}")
                
        return 0
        
    except Exception as e:
        logging.error(f"System failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit(main())