import stripe
from datetime import datetime, timedelta
from core.logger import setup_logger

logger = setup_logger(__name__)

class StripeAnalyzer:
    def __init__(self, api_key, exposure_hours=24):
        self.api_key = api_key
        stripe.api_key = api_key
        self.exposure_hours = exposure_hours
    
    def get_transactions_in_window(self):
        try:
            time_threshold = int((datetime.now() - timedelta(hours=self.exposure_hours)).timestamp())
            
            charges = stripe.Charge.list(
                created={'gte': time_threshold},
                limit=100
            )
            
            refunds = stripe.Refund.list(
                created={'gte': time_threshold},
                limit=100
            )
            
            logger.info(f"Found {len(charges.data)} charges and {len(refunds.data)} refunds")
            
            return charges.data, refunds.data
        
        except stripe.error.AuthenticationError:
            logger.error("Invalid Stripe API key")
            return None, None
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            return None, None
    
    def analyze_key(self):
        logger.info(f"Analyzing key exposure (window: {self.exposure_hours}h)...")
        
        charges, refunds = self.get_transactions_in_window()
        
        if charges is None:
            return None
        
        total_fraud = sum([c.amount_refunded for c in charges if c.amount_refunded > 0])
        
        fraud_alerts = []
        
        # Check for refund anomalies
        if len(refunds) > 0:
            fraud_alerts.append({
                'type': 'refunds_detected',
                'severity': 'HIGH',
                'description': f'{len(refunds)} refunds detected during exposure window'
            })
        
        # Check for charge spike
        if len(charges) > 50:
            fraud_alerts.append({
                'type': 'charge_spike',
                'severity': 'CRITICAL',
                'description': f'Unusual charge spike: {len(charges)} charges'
            })
        
        result = {
            'exposure_window_hours': self.exposure_hours,
            'charges_count': len(charges),
            'refunds_count': len(refunds),
            'total_fraud_amount': total_fraud / 100,
            'fraud_alerts': fraud_alerts,
            'high_risk': len(fraud_alerts) > 0
        }
        
        return result

def analyze_exposed_key(api_key, exposure_hours=24):
    analyzer = StripeAnalyzer(api_key, exposure_hours)
    return analyzer.analyze_key()
