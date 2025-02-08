from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, conint, validator
from typing import List, Optional, Annotated
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums for predefined options


class EmploymentStatus(str, Enum):
    ANY = "Any"
    EMPLOYED = "Employed"
    UNEMPLOYED = "Unemployed"
    STUDENT = "Student"
    RETIRED = "Retired"


class MaritalStatus(str, Enum):
    ANY = "Any"
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"


class OccupationType(str, Enum):
    ANY = "Any"
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    EDUCATION = "Education"
    FINANCE = "Finance"
    CREATIVE_ARTS = "Creative Arts"


class ProductCategory(str, Enum):
    ELECTRONICS = "Electronics"
    FASHION = "Fashion"
    HOME_LIVING = "Home & Living"
    OTHER = "Other"

# Pydantic models


class AgeRange(BaseModel):
    min: conint(ge=13, le=100)
    max: conint(ge=13, le=100)

    @validator('max')
    def max_greater_than_min(cls, v, values):
        if 'min' in values and v <= values['min']:
            raise ValueError('Max age must be greater than min age')
        return v


class DemographicDetails(BaseModel):
    student: bool
    parent: bool
    homeowner: bool


class BrandDetails(BaseModel):
    description: str
    primary_color: str
    secondary_color: str
    tagline: str


class ProductInfo(BaseModel):
    name: str
    description: str
    category: ProductCategory
    custom_category: Optional[str] = None
    target_emotions: List[str]

    @validator('custom_category', always=True)
    def validate_custom_category(cls, v, values):
        if values.get('category') == ProductCategory.OTHER and not v:
            raise ValueError(
                'Custom category required when "Other" is selected')
        return v


class TargetAudience(BaseModel):
    age_range: AgeRange
    employment_status: EmploymentStatus
    marital_status: MaritalStatus
    occupation: OccupationType
    mbti_type: str
    interests: List[str]
    demographics: DemographicDetails
    location: str


@app.post("/generate-ad/")
async def generate_ad_campaign(
    brand_details: Annotated[BrandDetails, Form()],
    product_info: Annotated[ProductInfo, Form()],
    target_audience: Annotated[TargetAudience, Form()],
    logo: UploadFile = File(None),
    product_images: List[UploadFile] = File([]),
):
    # Process files
    logo_content = await logo.read() if logo else None
    product_images_content = [await image.read() for image in product_images]

    return {
        "brand_details": brand_details.dict(),
        "product_info": product_info.dict(),
        "target_audience": target_audience.dict(),
        "logo_size": len(logo_content) if logo_content else 0,
        "product_images_count": len(product_images_content)
    }
