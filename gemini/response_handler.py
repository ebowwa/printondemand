from typing import List, Optional

class FinishReason:
    FINISH_REASON_UNSPECIFIED = "UNSPECIFIED"
    STOP = "STOP"
    MAX_TOKENS = "MAX_TOKENS"
    SAFETY = "SAFETY"
    RECITATION = "RECITATION"
    OTHER = "OTHER"

class SafetyRating:
    def __init__(self, category: Optional[str] = None, probability: Optional[float] = None):
        self.category = category
        self.probability = probability

class GroundingPassageId:
    def __init__(self, passage_id: str, part_index: int):
        self.passage_id = passage_id
        self.part_index = part_index

class SemanticRetrieverChunk:
    def __init__(self, source: str, chunk: str):
        self.source = source
        self.chunk = chunk

class AttributionSourceId:
    def __init__(self, grounding_passage: Optional[GroundingPassageId] = None, semantic_retriever_chunk: Optional[SemanticRetrieverChunk] = None):
        self.grounding_passage = grounding_passage
        self.semantic_retriever_chunk = semantic_retriever_chunk

class GroundingAttribution:
    def __init__(self, source_id: AttributionSourceId, content: str):
        self.source_id = source_id
        self.content = content

class CitationSource:
    def __init__(self, start_index: int, end_index: int, uri: Optional[str] = None, license: Optional[str] = None):
        self.start_index = start_index
        self.end_index = end_index
        self.uri = uri
        self.license = license

class CitationMetadata:
    def __init__(self, citation_sources: List[CitationSource]):
        self.citation_sources = citation_sources if citation_sources is not None else []

class ResponseCandidate:
    def __init__(
        self, 
        content: str, 
        finish_reason: FinishReason, 
        safety_ratings: List[SafetyRating], 
        citation_metadata: CitationMetadata, 
        token_count: int, 
        grounding_attributions: List[GroundingAttribution], 
        index: int
    ):
        self.content = content
        self.finish_reason = finish_reason
        self.safety_ratings = safety_ratings if safety_ratings is not None else []
        self.citation_metadata = citation_metadata
        self.token_count = token_count
        self.grounding_attributions = grounding_attributions if grounding_attributions is not None else []
        self.index = index


