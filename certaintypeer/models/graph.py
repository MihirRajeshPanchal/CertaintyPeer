from pydantic import BaseModel
from typing import List, Optional

class Review(BaseModel):
    review: str  
    rating: str  
    confidence: str 

class MetaReview(BaseModel):
    id: str  
    metaReview: str  
    reviews: List[Review]  

class Rating(BaseModel):
    rating: str  
    id: str  

class Confidence(BaseModel):
    confidence: str  
    id: str  

class MetaReviewRequest(BaseModel):
    id: str  
    metaReview: str  
    reviews: List[Review]  

class ReviewRequest(BaseModel):
    review: str  
    rating: str  
    confidence: str  
