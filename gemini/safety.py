from pydantic import BaseModel

class SafetySetting(BaseModel):
    category: str
    threshold: str

# Mapping of safety settings thresholds
SAFETY_THRESHOLDS = {
    "Block none": "BLOCK_NONE",
    "Block few": "BLOCK_ONLY_HIGH",
    "Block some": "BLOCK_MEDIUM_AND_ABOVE",
    "Block most": "BLOCK_LOW_AND_ABOVE",
    "HARM_BLOCK_THRESHOLD_UNSPECIFIED": "Threshold is unspecified, block using default threshold"
}
