class StatusCodeModel:
    code = None
    message = None

    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.status = "{code} {message}".format(code=self.code, message=self.message)

    def __eq__(self, other):
        try:
            return self.code == other.code
        except AttributeError:
            return self.code == other

    def __str__(self):
        return self.status

    def __repr__(self):
        return self.status


class StatusCode:
    CONTINUE = StatusCodeModel(100, "Continue")
    SWITCHING_PROTOCOLS = StatusCodeModel(101, "Switching Protocols")
    PROCESSING = StatusCodeModel(102, "Processing")

    OK = StatusCodeModel(200, "OK")
    Created = StatusCodeModel(201, "Created")
    Accepted = StatusCodeModel(202, "Accepted")
    NON_AUTHORITATIVE_INFORMATION = StatusCodeModel(203, "Non-Authoritative Information")
    NO_CONTENT = StatusCodeModel(204, "No Content")
    RESET_CONTENT = StatusCodeModel(205, "Reset Content")
    PARTIAL_CONTENT = StatusCodeModel(206, "Partial Content")
    MULTI_STATUS = StatusCodeModel(207, "Multi-Status")
    ALREADY_REPORTED = StatusCodeModel(208, "Already Reported")
    IM_USED = StatusCodeModel(226, "IM Used")
    EMPTY_CONTENT = StatusCodeModel(291, "Empty Content")

    MULTIPLE_CHOICES = StatusCodeModel(300, "Multiple Choices")
    MOVED_PERMANENTLY = StatusCodeModel(301, "Moved Permanently")
    FOUND = StatusCodeModel(302, "Found")
    SEE_OTHER = StatusCodeModel(303, "See Other")
    NOT_MODIFIED = StatusCodeModel(304, "Not Modified")
    USE_PROXY = StatusCodeModel(305, "Use Proxy")
    TEMPORARY_REDIRECT = StatusCodeModel(307, "Temporary Redirect")
    PERMANENT_REDIRECT = StatusCodeModel(308, "Permanent Redirect")

    BAD_REQUEST = StatusCodeModel(400, "Bad Request")
    UNAUTHORIZED = StatusCodeModel(401, "Unauthorized")
    PAYMENT_REQUIRED = StatusCodeModel(402, "Payment Required")
    FORBIDDEN = StatusCodeModel(403, "Forbidden")
    NOT_FOUND = StatusCodeModel(404, "Not Found")
    METHOD_NOT_ALLOWED = StatusCodeModel(405, "Method Not Allowed")
    NOT_ACCEPTABLE = StatusCodeModel(406, "Not Acceptable")
    PROXY_AUTHENTICATION_REQUIRED = StatusCodeModel(407, "Proxy Authentication Required")
    REQUEST_TIME_OUT = StatusCodeModel(408, "Request Time-out")
    CONFLICT = StatusCodeModel(409, "Conflict")
    GONE = StatusCodeModel(410, "Gone")
    LENGTH_REQUIRED = StatusCodeModel(411, "Length Required")
    PRECONDITION_FAILED = StatusCodeModel(412, "Precondition Failed")
    PAYLOAD_TOO_LARGE = StatusCodeModel(413, "Payload Too Large")
    URI_TOO_LONG = StatusCodeModel(414, "URI Too Long")
    UNSUPPORTED_MEDIA_TYPE = StatusCodeModel(415, "Unsupported Media Type")
    RANGE_NOT_SATISFIABLE = StatusCodeModel(416, "Range Not Satisfiable")
    EXPECTATION_FAILED = StatusCodeModel(417, "Expectation Failed")
    I_AM_A_TEAPOT = StatusCodeModel(418, "I'm a teapot")
    UNPROCESSABLE_ENTITY = StatusCodeModel(422, "Unprocessable Entity")
    LOCKED = StatusCodeModel(423, "Locked")
    FAILED_DEPENDENCY = StatusCodeModel(424, "Failed Dependency")
    UPGRADE_REQUIRED = StatusCodeModel(426, "Upgrade Required")
    PRECONDITION_REQUIRED = StatusCodeModel(428, "Precondition Required")
    TOO_MANY_REQUESTS = StatusCodeModel(429, "Too Many Requests")
    REQUEST_HEADER_FIELDS_TOO_LARGE = StatusCodeModel(431, "Request Header Fields Too Large")
    UNAVAILABLE_FOR_LEGAL_REASONS = StatusCodeModel(451, "Unavailable For Legal Reasons")

    INTERNAL_SERVER_ERROR = StatusCodeModel(500, "Internal Server Error")
    NOT_IMPLEMENTED = StatusCodeModel(501, "Not Implemented")
    BAD_GATEWAY = StatusCodeModel(502, "Bad Gateway")
    SERVICE_UNAVAILABLE = StatusCodeModel(503, "Service Unavailable")
    GATEWAY_TIMEOUT = StatusCodeModel(504, "Gateway Timeout")
    HTTP_VERSION_NOT_SUPPORTED = StatusCodeModel(505, "HTTP Version Not Supported")
    INSUFFICIENT_STORAGE = StatusCodeModel(507, "Insufficient Storage")
    LOOP_DETECTED = StatusCodeModel(508, "Loop Detected")
    NETWORK_AUTHENTICATION_REQUIRED = StatusCodeModel(511, "Network Authentication Required")

    @staticmethod
    def find_by_code(code):
        for variable in vars(StatusCode):
            model = getattr(StatusCode, variable)
            if isinstance(model, StatusCodeModel):
                if model.code == code:
                    return model
        return None
