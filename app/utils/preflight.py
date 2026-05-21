import os
from app.utils.config_manager import config
from app.utils.logging_service import ErrorCategory, log_error, log_info


def validate_preflight():
    """Validate startup requirements. Returns (success, errors_list)."""
    errors = []
    
    # Check config loaded successfully
    if config.get_errors():
        errors.extend(config.get_errors())
    
    # Check Flask secret exists
    secret = config.get('flask.secret_key')
    if not secret:
        msg = log_error(ErrorCategory.CONFIG_ERROR, "Flask secret_key missing from config.json")
        errors.append(msg)
    
    # Check OpenAI API key file path exists
    api_key_file = config.get('openai.api_key_file')
    if not api_key_file:
        msg = log_error(ErrorCategory.API_KEY_ERROR, "openai.api_key_file path missing from config.json")
        errors.append(msg)
    elif not os.path.exists(api_key_file):
        msg = log_error(ErrorCategory.API_KEY_ERROR, f"OpenAI API key file not found: {api_key_file}")
        errors.append(msg)
    else:
        try:
            with open(api_key_file, 'r', encoding='utf-8') as fh:
                key = fh.read().strip()
                if not key:
                    msg = log_error(ErrorCategory.API_KEY_ERROR, f"OpenAI API key file is empty: {api_key_file}")
                    errors.append(msg)
                else:
                    log_info(f"OpenAI API key loaded from {api_key_file}")
        except Exception as e:
            msg = log_error(ErrorCategory.API_KEY_ERROR, f"Failed to read API key file", e)
            errors.append(msg)
    
    # Check data folder exists
    data_folder = config.get('data.folder', 'data')
    data_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), data_folder)
    if not os.path.exists(data_path):
        try:
            os.makedirs(data_path, exist_ok=True)
            log_info(f"Data folder created: {data_path}")
        except Exception as e:
            msg = log_error(ErrorCategory.STORAGE_ERROR, f"Failed to create data folder", e)
            errors.append(msg)
    
    # Check uploads folder exists
    uploads_folder = config.get('upload.folder', 'uploads')
    uploads_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), uploads_folder)
    if not os.path.exists(uploads_path):
        try:
            os.makedirs(uploads_path, exist_ok=True)
            log_info(f"Uploads folder created: {uploads_path}")
        except Exception as e:
            msg = log_error(ErrorCategory.STORAGE_ERROR, f"Failed to create uploads folder", e)
            errors.append(msg)
    
    # Check logs folder exists
    logs_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'logs')
    if not os.path.exists(logs_path):
        try:
            os.makedirs(logs_path, exist_ok=True)
            log_info(f"Logs folder created: {logs_path}")
        except Exception as e:
            msg = log_error(ErrorCategory.STORAGE_ERROR, f"Failed to create logs folder", e)
            errors.append(msg)
    
    success = len(errors) == 0
    if success:
        log_info("Preflight validation passed")
    else:
        log_error(ErrorCategory.CONFIG_ERROR, f"Preflight validation failed with {len(errors)} error(s)")
    
    return success, errors
