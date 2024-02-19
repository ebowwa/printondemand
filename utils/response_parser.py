from pydantic import BaseModel
from typing import Dict, List

class SectionCounts(BaseModel):
    Design_Title: int = 0
    Brand_Name: int = 0
    Product_Features: int = 0
    Feature_Bullet_2: int = 0
    Product_Description: int = 0

def parse_response_and_count_characters(response_text: str) -> Dict[str, int]:
    sections = ["Design Title:", "Brand Name:", "Product Features:","Feature Bullet 1:", "Feature Bullet 2:", "Product Description:"]
    seo_exclusions = ["SEO Tip:", "SEO Strategy:"]  
    section_counts = SectionCounts()  # Using Pydantic model for initialization

    current_section: str = ''

    for line in response_text.split('\n'):
        line = line.strip()  
        if any(line.startswith(section) for section in sections):
            current_section = line.split(':')[0].replace(' ', '_') + ":"  
        elif current_section and not any(line.startswith(exclusion) for exclusion in seo_exclusions):
            # Increment count in Pydantic model by attribute name
            setattr(section_counts, current_section[:-1], getattr(section_counts, current_section[:-1]) + len(line) + 1)

    # Convert Pydantic model to dictionary for return
    return section_counts.dict()