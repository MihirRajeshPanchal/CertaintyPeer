from certaintypeer.models.graph import MetaReview
from certaintypeer.constants.graph import REVIEW_NODE, RATING_NODE, CONFIDENCE_NODE, RATING_SCORE_NODE, CONFIDENCE_SCORE_NODE
from certaintypeer.constants.certaintypeer import driver, estimator

import re

def clean_text(text: str) -> str:
    """Remove all special characters from the text."""
    return re.sub(r'[^A-Za-z0-9 ]', '', text)

def extract_first_number(text: str) -> int:
    """Extract the first numeric value from the given text."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

def add_reviews(meta_review_request: MetaReview):
    

    with driver.session() as session:
        for review_data in meta_review_request.reviews:

            cleaned_review = clean_text(review_data.review)
            cleaned_rating = clean_text(review_data.rating)
            cleaned_confidence = clean_text(review_data.confidence)

            rating_score = extract_first_number(review_data.rating)
            confidence_score = extract_first_number(review_data.confidence)

            certainty_score = estimator.predict(cleaned_review)[0]

            review_query = f"""
            CREATE (review: {REVIEW_NODE} {{review: '{cleaned_review}', certainty: {certainty_score}}})
            CREATE (rating: {RATING_NODE} {{rating: '{cleaned_rating}'}})
            CREATE (confidence: {CONFIDENCE_NODE} {{confidence: '{cleaned_confidence}'}})
            MERGE (rating_score: {RATING_SCORE_NODE} {{value: {rating_score}}})
            MERGE (confidence_score: {CONFIDENCE_SCORE_NODE} {{value: {confidence_score}}})
            CREATE (review)-[:HAS_RATING]->(rating)
            CREATE (review)-[:HAS_CONFIDENCE]->(confidence)
            MERGE (rating)-[:HAS_RATING_SCORE]->(rating_score)  
            MERGE (confidence)-[:HAS_CONFIDENCE_SCORE]->(confidence_score) 
            """
            session.run(review_query)

        return {"reviews_count": len(meta_review_request.reviews)}
