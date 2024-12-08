#!/usr/bin/env python3
import subprocess
import time
import sys
import os
import logging

def setup_logging():
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'infuse_frame_switch.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )
    return logging.getLogger()

def is_infuse_running():
    try:
        result = subprocess.run(['pgrep', '-x', 'Infuse'], capture_output=True)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error checking Infuse: {e}")
        return False

def switch_refresh_rate(hz):
    display_id = "012A6609-58A0-45FF-8F55-8538870D40BB"  # Your display ID
    cmd = f'displayplacer "id:{display_id} res:1920x1080 hz:{hz} color_depth:8 enabled:true scaling:on origin:(0,0) degree:0"'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Error switching refresh rate: {result.stderr}")
    except Exception as e:
        logger.error(f"Error running displayplacer: {e}")

def main():
    global logger
    logger = setup_logging()
    logger.info("Starting Infuse Frame Rate Switcher...")
    
    # Log environment information
    logger.info(f"Python path: {sys.executable}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"PATH: {os.environ.get('PATH')}")
    
    original_hz = 60
    current_hz = original_hz
    was_running = False
    
    try:
        while True:
            is_running = is_infuse_running()
            
            # Detect state changes immediately
            if is_running and not was_running:
                switch_refresh_rate(24)
                logger.info("Switched to 24Hz")
                current_hz = 24
            elif not is_running and was_running:
                switch_refresh_rate(original_hz)
                logger.info(f"Restored to {original_hz}Hz")
                current_hz = original_hz
            
            was_running = is_running
            time.sleep(0.01)  # Poll 100 times per second
            
    except KeyboardInterrupt:
        logger.info("Exiting...")
        switch_refresh_rate(original_hz)
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    main() 