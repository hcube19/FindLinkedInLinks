
# Handles input/output operations for CSV files

import pandas as pd
import logging
import config.config as config

# Load input data from the CSV file specified in config
def load_input_data():
    try:
        return pd.read_csv(config.CSV_PATH)
    except Exception as e:
        logging.error(f"Failed to read input CSV: {e}")
        return None

# Save the verified profiles to the output CSV file specified in config
def save_verified_profiles(profiles):
    try:
        out_df = pd.DataFrame(profiles)
        out_df.to_csv(config.OUTPUT_PATH, index=False)
        logging.info(f'Done! Verified profiles saved to {config.OUTPUT_PATH}')
    except Exception as e:
        logging.error(f"Failed to save results: {e}")
