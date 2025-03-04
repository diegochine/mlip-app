def process_data(data):
    """
    Performs basic preprocessing on the data.
    For example, this function drops rows with missing values.
    """
    processed_data = data.dropna()
    return processed_data
