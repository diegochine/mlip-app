import numpy as np

def calculate_psi(expected, actual, buckets=10):
    """
    Calculate the Population Stability Index (PSI) between two distributions.
    
    Parameters:
    - expected: 1D numpy array (reference distribution)
    - actual: 1D numpy array (current distribution)
    - buckets: number of buckets to use
    
    Returns:
    - psi: calculated PSI value
    """
    # Define bucket breakpoints based on expected percentiles
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    expected_counts, _ = np.histogram(expected, bins=breakpoints)
    actual_counts, _ = np.histogram(actual, bins=breakpoints)

    # Convert counts to percentages and avoid division by zero
    expected_percents = expected_counts / np.sum(expected_counts)
    actual_percents = actual_counts / np.sum(actual_counts)
    expected_percents = np.where(expected_percents == 0, 0.0001, expected_percents)
    actual_percents = np.where(actual_percents == 0, 0.0001, actual_percents)
    
    psi = np.sum((expected_percents - actual_percents) * np.log(expected_percents / actual_percents))
    return psi

def detect_drift(expected_data, actual_data, threshold=0.1, buckets=10):
    """
    Detect drift by calculating the PSI between expected and actual data distributions.
    
    Parameters:
    - expected_data: 1D numpy array for the reference distribution.
    - actual_data: 1D numpy array for the current distribution.
    - threshold: PSI threshold above which drift is flagged.
    - buckets: number of buckets for the histogram.
    
    Returns:
    - drift_detected: Boolean indicating if drift is detected.
    - psi_value: The computed PSI value.
    """
    psi_value = calculate_psi(expected_data, actual_data, buckets=buckets)
    drift_detected = psi_value > threshold
    return drift_detected, psi_value

def alert_if_drift(expected_data, actual_data, threshold=0.1, buckets=10):
    """
    Checks for drift and simulates an alert if drift is detected.
    In production, this could be integrated with email or Slack notifications.
    
    Returns:
    - drift_detected: Boolean indicating if drift is detected.
    - psi_value: The computed PSI value.
    """
    drift_detected, psi_value = detect_drift(expected_data, actual_data, threshold, buckets)
    if drift_detected:
        import logging
        logging.warning(f"Drift detected! PSI value: {psi_value:.4f}")
    return drift_detected, psi_value
