import os 
import logging



LOG_DIR = os.path.join(os.path.dirname(__file__),"logs")
# ensure folder is created
os.makedirs(LOG_DIR, exist_ok=True)

# Configure basic logging for HTTP requests
LOG_FILE = os.path.join(LOG_DIR, "app.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_logger():
    return logger