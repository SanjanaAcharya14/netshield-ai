import numpy as np
from sklearn.ensemble import IsolationForest

class TrafficAnomalyDetector:
    def __init__(self):
        # Initialize an Isolation Forest model for anomaly detection
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
        self._bootstrap_dummy_model()

    def _bootstrap_dummy_model(self):
        """
        Trains the model on initial synthetic normal baseline traffic 
        so it can start making real-time predictions immediately.
        Features: [packet_length, packets_per_sec, port_number]
        """
        # Normal traffic baseline: small sizes (60-1500 bytes), low rate (1-20 pkts/s)
        normal_data = np.random.normal(loc=[500, 10, 80], scale=[200, 5, 20], size=(100, 3))
        
        # Anomaly traffic baseline: huge sizes/rates (e.g., DoS/port scan spikes)
        anomaly_data = np.random.uniform(low=[1400, 200, 1], high=[1500, 1000, 65535], size=(10, 3))
        
        X_train = np.vstack([normal_data, anomaly_data])
        self.model.fit(X_train)
        self.is_trained = True

    def predict(self, packet_length, packet_rate=1, port=80):
        """
        Predicts if a network stream feature vector is Normal (1) or Anomaly (-1).
        """
        features = np.array([[packet_length, packet_rate, port]])
        prediction = self.model.predict(features)[0]
        
        # IsolationForest outputs -1 for anomaly, 1 for normal
        is_anomaly = True if prediction == -1 else False
        return {
            "is_anomaly": is_anomaly,
            "status": "SUSPICIOUS" if is_anomaly else "NORMAL",
            "score": float(self.model.decision_function(features)[0])
        }

if __name__ == "__main__":
    detector = TrafficAnomalyDetector()
    
    # Test normal traffic (100 byte packet)
    print("Normal Traffic Test:", detector.predict(packet_length=100, packet_rate=5, port=443))
    
    # Test anomalous traffic spike (1500 byte packets at huge rate)
    print("Anomaly Spike Test:", detector.predict(packet_length=1500, packet_rate=800, port=80))