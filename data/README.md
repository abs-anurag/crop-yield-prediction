# Dataset Documentation

## Dataset Information
- **Name**: FAOSTAT & World Bank Global Crop Yield Dataset
- **Direct Combined Dataset Reference**: [Kaggle Crop Yield Prediction Dataset](https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset) / [GitHub hajir-almahdi/Machine-Learning-Capstone-Project](https://github.com/hajir-almahdi/Machine-Learning-Capstone-Project)
- **Original Underlying Data Providers**:
  1. **Food and Agriculture Organization of the United Nations (FAOSTAT)**: Country-level crop yield metrics (`hg/ha_yield`) and pesticide consumption data (`pesticides_tonnes`).
  2. **World Bank Climate Data API**: Country-level average annual precipitation (`average_rain_fall_mm_per_year`) and average annual surface temperature (`avg_temp`).
- **License / Data Policy**:
  - FAOSTAT Open Data Policy (CC BY-3.0 IGO)
  - World Bank Open Data Terms of Use (CC BY 4.0)
- **Download Date**: 2026-09-28

---

## Dataset Schema & Features

| Column Name | Data Type | Role | Original Unit | Description |
|-------------|-----------|------|---------------|-------------|
| `Area` | String | Feature (Categorical) | - | Country / Region name (101 unique countries) |
| `Item` | String | Feature (Categorical) | - | Crop type (10 unique crops) |
| `Year` | Integer | Feature (Numerical) | Year | Year of observation (1990 - 2013) |
| `average_rain_fall_mm_per_year` | Float | Feature (Numerical) | mm/year | Average annual precipitation |
| `pesticides_tonnes` | Float | Feature (Numerical) | Tonnes | Total pesticide usage in tonnes |
| `avg_temp` | Float | Feature (Numerical) | °C | Average annual surface temperature |
| `hg/ha_yield` | Integer | Target Variable | hg/ha | Crop yield in hectograms per hectare |

---

## Target Variable & Unit Conversion
- **Original Field**: `hg/ha_yield` (hectograms / hectare)
- **Converted Field**: `yield_tons_per_ha` (metric tons / hectare)
- **Conversion Math**: $1 \text{ hectogram (hg)} = 100 \text{ grams} = 0.1 \text{ kg}$. Therefore $10,000 \text{ hg/ha} = 1,000 \text{ kg/ha} = 1 \text{ metric ton/hectare}$.
$$\text{yield (tons/ha)} = \frac{\text{hg/ha\_yield}}{10000.0}$$
- **Target Value Range**:
  - `hg/ha_yield`: 50 to 501,412 hg/ha
  - `yield_tons_per_ha`: 0.005 to 50.14 tons/ha (Mean: ~7.70 tons/ha)

---

## Dataset Statistics
- **Total Records**: 28,242 rows
- **Missing Values**: 0 across all columns
- **Duplicate Rows**: 0
- **Crops Included (10)**: `Maize`, `Potatoes`, `Rice, paddy`, `Sorghum`, `Soybeans`, `Wheat`, `Cassava`, `Sweet potatoes`, `Plantains and others`, `Yams`
- **Geographic Scope**: 101 countries worldwide
- **Time Period**: 1990 to 2013 (24 annual snapshots)

---

## Important Data Notes
- Features reflect real historical observations collected by international bodies (FAO & World Bank).
- `pesticides_tonnes` measures country-level pesticide consumption in tonnes.
- Features such as `soil_type`, `humidity`, or plot-level `area` are not present in this dataset and are not fabricated.