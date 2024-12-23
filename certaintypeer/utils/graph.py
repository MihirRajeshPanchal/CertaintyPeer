from certaintypeer.models.graph import MetaReviewRequest
from certaintypeer.constants.graph import META_REVIEW_NODE, REVIEW_NODE, RATING_NODE, CONFIDENCE_NODE
from certaintypeer.constants.certaintypeer import driver
import re

def clean_text(text: str) -> str:
    """Remove all special characters from the text."""
    return re.sub(r'[^A-Za-z0-9 ]', '', text)

def add_meta_review_and_reviews(meta_review_request: MetaReviewRequest):
    with driver.session() as session:
        
        meta_review_query = f"""
        MERGE (meta: {META_REVIEW_NODE} {{id: '{meta_review_request.id}', metaReview: '{clean_text(meta_review_request.metaReview)}'}})
        WITH meta
        """
        
        for review_data in meta_review_request.reviews:
            review_query = meta_review_query + f"""
            CREATE (review: {REVIEW_NODE} {{review: '{clean_text(review_data.review)}'}})
            CREATE (rating: {RATING_NODE} {{rating: '{clean_text(review_data.rating)}'}})
            CREATE (confidence: {CONFIDENCE_NODE} {{confidence: '{clean_text(review_data.confidence)}'}})
            CREATE (meta)-[:CONTAINS]->(review)
            CREATE (review)-[:HAS_RATING]->(rating)
            CREATE (review)-[:HAS_CONFIDENCE]->(confidence)
            """
            session.run(review_query)

        return {"meta_review_id": meta_review_request.id, "reviews_count": len(meta_review_request.reviews)}