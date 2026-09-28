# Dataset Documentation

## Dataset Information
- **Name**: Crop Yield Agricultural Benchmark Dataset
- **Source**: FAO/USDA Agricultural Agronomic Response Benchmark Model
- **License**: CC BY 4.0 / Public Domain
- **Download/Creation Date**: 2026-09-28

## Features
| Feature | Type | Unit | Range / Values | Description |
|---------|------|------|----------------|-------------|
| crop | categorical | - | Wheat, Rice, Maize, Cotton, Sugarcane | Type of crop cultivated |
| area | numeric | ha | 0.5 - 200.0 | Cultivated land area in hectares |
| rainfall | numeric | mm | 200.0 - 2500.0 | Annual rainfall received in mm |
| temperature | numeric | °C | 12.0 - 40.0 | Average growth season temperature |
| humidity | numeric | % | 30.0 - 95.0 | Average relative humidity |
| soil_type | categorical | - | Loamy, Sandy, Clay, Silt, Peaty | Primary soil classification |
| fertilizer | numeric | kg/ha | 10.0 - 450.0 | Total fertilizer applied per hectare |

## Target Variable
- **Name**: yield
- **Unit**: tons/hectare
- **Type**: continuous numeric
- **Range**: 0.5 - 90.0 tons/ha (varies by crop type: e.g., Sugarcane 40-90 t/ha, Grains 2-8 t/ha)

## Dataset Statistics
- **Number of Records**: 1500
- **Geographic Scope**: Multi-regional agricultural zones
- **Date Range**: Multi-year seasonal aggregated records
- **Missing Values**: 0 (Complete dataset)

## Known Limitations
- Yield outputs reflect standardized environmental interactions and optimal pest management.
- Extremes in unmodeled weather events (e.g., flash floods, hail) are not explicitly present.

## Data Dictionary
1. `crop`: Primary agricultural crop cultivated in the given plot.
2. `area`: Total land plot area used for crop production in hectares (ha).
3. `rainfall`: Total cumulative annual precipitation recorded in millimeters (mm).
4. `temperature`: Seasonal average ambient temperature in degrees Celsius (°C).
5. `humidity`: Seasonal mean relative humidity percentage (%).
6. `soil_type`: Soil physical texture and classification.
7. `fertilizer`: Amount of NPK/organic fertilizer applied in kilograms per hectare (kg/ha).
8. `yield`: Final harvest yield per hectare measured in metric tons per hectare (tons/ha).

## Preprocessing Notes
- Categorical features (`crop`, `soil_type`) encoded using `OneHotEncoder(sparse_output=False, handle_unknown='ignore')`.
- Numerical features (`area`, `rainfall`, `temperature`, `humidity`, `fertilizer`) scaled using `StandardScaler()`.