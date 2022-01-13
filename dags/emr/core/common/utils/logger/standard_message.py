class StandardMessage:
    # Core service
    INFO_START_SERVICE = "Service Started at PORT: {port} on PID: {pid}"
    ERROR_UNHANDLED_EXCEPTION = "Unhandled exception:\n{error}"
    CRITICAL_RECEIVE_SIGINT = "Receive SIGINT, service has been stopped"
    CRITICAL_STOP_SERVICE = "Service has been stopped, reason: {reason}"

    # Request
    DEBUG_REQUEST_URL = "Request {method} {url} {headers} {body}"
    ERROR_REQUEST_URL = "Request {method} {url}\n{error}"

    INFO_RESPONSE_URL = "Response {method} {url} {status}"
    DEBUG_RESPONSE_URL = "Response {method} {url} {status} {response}"
    WARNING_RESPONSE_URL = "Response {method} {url} {status} {response}"

    # Adapter
    ERROR_ADAPTER_URL_NOT_FOUND = "Adapter URL not found, key: {key}"

    # MongoDB
    INFO_MONGODB_CONNECTED = "Connected to MongoDB server"
    ERROR_MONGODB_MISSING_SETTING = "MongoDB setting is missing, key: {key}"
    ERROR_MONGODB_COLLECTION_TYPE = "Mongo collection must be str, received {type}"
    ERROR_MONGODB_DATA_TYPE = "Mongo insert data must be dict/list of dicts, received {type}"
    ERROR_MONGODB_DATA_LIST_TYPE = "Mongo insert data with list, all elements must be dict, received {type}"
    ERROR_MONGODB_QUERY_TYPE = "Mongo query must be dict, received {type}"
    ERROR_MONGODB_NONE_SETTING = "Cannot find key: mongodb in settings"
    ERROR_MONGODB_CONNECTION_REFUSE = "Cannot connect to MongoDB server"

    # Falcon Middleware
    INFO_API_REQUEST = "API Request: {ip} {method} {scheme} {path}"
    DEBUG_API_REQUEST = "API Request: {ip} {method} {scheme} {path} {headers} {body}"

    INFO_API_RESPONSE = "API Response: {ip} {method} {scheme} {path} {status}"
    DEBUG_API_RESPONSE = "API Response: {ip} {method} {scheme} {path} {status} {response}"

    WARNING_API_REQUEST_AUTH_REQUIRED = "API Request: headers: Authorization is required"
    WARNING_API_REQUEST_AUTH_INVALID_TOKEN = "API Request: Invalid access token"
    ERROR_SETTING_MISSING = "Missing key: {key} in main settings"
    ERROR_API_REQUEST_AUTH = "Cannot connect to oauth provider"

    # File Manager
    INFO_TRY_WRITE_FILE = "File Manager: trying write file: {path}"
    INFO_TRY_READ_FILE = "File Manager: trying read file: {path}"
    INFO_WRITE_FILE_COMPLETE = "File Manager: write file: {path} complete"
    INFO_READ_FILE_COMPLETE = "File Manager: read file: {path} complete"
    ERROR_PATH_NOT_EXIST = "File Manager: path: {path} is not exist"
    ERROR_WRITE_FILE_NOT_SUPPORT_TYPE = "File Manager: not support data type: {type}"
    ERROR_WRITE_FILE = "File Manager: cannot write file, reason:\n{tb}"
    ERROR_READ_FILE = "File Manager: cannot read file, reason:\n{tb}"

    # API
    DEBUG_API_CALL = "API: {api_name}  Method: {api_method} is being called."

    WARNING_API_DATA_NOT_FOUND = "Can't find data with these arguments, method: {method} on {url}"
    WARNING_API_MODE_NOT_IMPLEMENT = "{method} method not support on this site"

    ERROR_API_MODE_NOT_FOUND = "Can't find method: {method} on {url}"
    ERROR_API_HEADER = "{arg_name}={arg_value} are not support"
    ERROR_API_VALIDATION = "`{arg_name}` is not valid"
    ERROR_API_UNHANDLED_EXCEPTION = "API unhandled exception {type}: {error}"
    ERROR_API_TRACEBACK_EXCEPTION = "API traceback exception {traceback}"

    # Data service
    DEBUG_RETRY_FUNCTION_CALL = "Retry function call when {error} key: {text}."

    INFO_START_SERVICE_CALL = "Call service: {service}"
    INFO_SUCCESS_SERVICE_GET_DATA_FROM_DAO = "Service: {service} get data from: {dao} success"
    INFO_SUCCESS_TRANSFORMED_DATA = "Service: {service} transform data success"

    WARNING_METHOD_NOT_IMPLEMENT = "`{method}` method not implement"
    WARNING_DATA_NOT_FOUND = "Receive empty result set from: {from_module}"
    WARNING_UNHANDLED_EXCEPTION = "Warning unhandled exception type {type}: {error}"

    ERROR_HEADER_REQUIRED = "`{header_name}` Header(s) is required"
    ERROR_ARG_WRONG_FORMAT = "`{arg_name}` is wrong format"
    ERROR_ARGS_REQUIRED = "`{arg_name}` argument(s) is required"
    ERROR_NON_ROUTEABLE_ADDRESS = "Error non routable address."
    ERROR_BU_CODE_NOT_FOUND = "Error bu_code not found."
    ERROR_UNRELATED_HN_EN = "Error `hn` and `en` are not related."
    ERROR_INVALID_JSON_FORMAT = "Error invalid json format."


    # QUERY
    INFO_QUERY_CALL = "Call QUERY: {module}.{method}"
    INFO_QUERY_CALL_SUCCESS = "QUERY: {class}.{method} execute successful"

    WARNING_QUERY_METHOD_IMPLEMENT = "`{method}` method not implement"

    ERROR_QUERY_UNHANDLED_EXCEPTION = "QUERY: {class} Error unhandled exception type {type}: {error}"
    ERROR_QUERY_TIMEOUT_EXCEPTION = "Call QUERY: {module}.{method} Error timeout exception"
