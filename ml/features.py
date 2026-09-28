"""
Authoritative feature definitions and schema constants for the Crop Yield Prediction ML pipeline based on the real FAO & World Bank dataset.
"""

# Feature Groups
CATEGORICAL_FEATURES = ["Area", "Item"]
NUMERICAL_FEATURES = [
    "Year",
    "average_rain_fall_mm_per_year",
    "pesticides_tonnes",
    "avg_temp",
]

# All Input Features
INPUT_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES

# Target Variable Definitions
RAW_TARGET_VARIABLE = "hg/ha_yield"  # Target in original dataset (hectograms / hectare)
TARGET_VARIABLE = "yield_tons_per_ha"  # Standardized target (tons / hectare = hg/ha / 10000.0)
TARGET_UNIT = "tons/hectare"

# Valid Crop Categories (from FAO dataset `Item` column)
SUPPORTED_CROPS = [
    "Maize",
    "Potatoes",
    "Rice, paddy",
    "Sorghum",
    "Soybeans",
    "Wheat",
    "Cassava",
    "Sweet potatoes",
    "Plantains and others",
    "Yams",
]

# Supported Countries (101 unique countries from FAO dataset `Area` column)
SUPPORTED_COUNTRIES = [
    "Albania", "Algeria", "Angola", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Belarus", "Belgium", "Botswana",
    "Brazil", "Bulgaria", "Burkina Faso", "Burundi", "Cameroon", "Canada", "Central African Republic",
    "Chile", "Colombia", "Croatia", "Denmark", "Dominican Republic", "Ecuador", "Egypt",
    "El Salvador", "Eritrea", "Estonia", "Ethiopia", "Finland", "France", "Germany",
    "Ghana", "Greece", "Guatemala", "Guinea", "Guyana", "Haiti", "Honduras",
    "Hungary", "India", "Indonesia", "Iraq", "Ireland", "Italy", "Jamaica",
    "Japan", "Kazakhstan", "Kenya", "Latvia", "Lebanon", "Lesotho", "Lithuania",
    "Libya", "Madagascar", "Malawi", "Malaysia", "Mali", "Mauritania", "Mauritius",
    "Mexico", "Morocco", "Mozambique", "Namibia", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "Norway", "Pakistan", "Papua New Guinea", "Peru",
    "Poland", "Portugal", "Qatar", "Romania", "Rwanda", "Saudi Arabia", "Senegal",
    "Slovenia", "South Africa", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
    "Switzerland", "Tajikistan", "Thailand", "Tunisia", "Turkey", "Uganda", "Ukraine",
    "United Kingdom", "United States", "Uruguay", "Zambia", "Zimbabwe"
]

# Empirical Feature Ranges (from real dataset)
FEATURE_RANGES = {
    "Year": {"min": 1990, "max": 2013, "unit": "year"},
    "average_rain_fall_mm_per_year": {"min": 51.0, "max": 3240.0, "unit": "mm/year"},
    "pesticides_tonnes": {"min": 0.04, "max": 367778.0, "unit": "tonnes"},
    "avg_temp": {"min": 1.3, "max": 30.65, "unit": "°C"},
}
