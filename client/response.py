from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class StreamEventType(str, Enum):
    TEXT_DELTA = "text_delta"
    MESSAGE_COMPLETE = "message_complete"
    ERROR = "error"


@dataclass
class TextDelta:
    content: str



@dataclass
class TokenUsage:
    #user input token count
    prompt_tokens: int = 0
    #agent reponse token count
    completion_tokens: int = 0
    total_tokens: int = 0
    cached_tokens:int = 0
    


@dataclass
class StreamEvent:
    type: StreamEventType #catetory stream event type
    #message content from agent response
    text_delta: TextDelta | None = None
    error: str | None = None
    finish_reason: str | None = None
    usage: TokenUsage | None = None
    
    
