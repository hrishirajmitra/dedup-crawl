

# Configuration field names
FIELD_SINGLE = "field"
FIELD_LEFT = "field_left"
FIELD_RIGHT = "field_right"

# Comparison methods
METHOD_STRING = "string"
METHOD_EXACT = "exact"

# Comparison configuration keys
KEY_METHOD = "method"
KEY_LABEL = "label"
KEY_THRESHOLD = "threshold"
KEY_STRING_METHOD = "string_method"

# Default values
DEFAULT_STRING_ALGO = "jarowinkler"

# Indexing configuration
SORTING_WINDOW_SIZE = "window_size"  # Config key for window size
NAME_1_FIELD = "name_1"
NAME_2_FIELD = "name_2"

# Data fields
FIELD_REC_ID = "rec_id"
FIELD_UNNAMED_0 = "Unnamed: 0"
FIELD_GIVEN_NAME = "given_name"
FIELD_SURNAME = "surname"
FIELD_STREET_NUMBER = "street_number"
FIELD_ADDRESS_1 = "address_1"
FIELD_ADDRESS_2 = "address_2"
FIELD_SUBURB = "suburb"
FIELD_POSTCODE = "postcode"
FIELD_STATE = "state"
FIELD_DATE_OF_BIRTH = "date_of_birth"
FIELD_SOC_SEC_ID = "soc_sec_id"

# Canonical name fields
NAME_1_FIELD = "name_1"
NAME_2_FIELD = "name_2"

# Fields to clean during preprocessing
FIELDS_TO_CLEAN = [
    FIELD_GIVEN_NAME,
    FIELD_SURNAME,
    FIELD_STREET_NUMBER,
    FIELD_ADDRESS_1,
    FIELD_ADDRESS_2,
    FIELD_SUBURB,
    FIELD_POSTCODE,
    FIELD_STATE,
    FIELD_DATE_OF_BIRTH,
    FIELD_SOC_SEC_ID
]