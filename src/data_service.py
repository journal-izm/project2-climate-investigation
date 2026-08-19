import os

import pandas as pd


DATA_PATH = os.path.join("data", "climate_data.csv")
REQUIRED_COLUMNS = ["date", "year", "region", "avg_temperature", "heatwave_days", "precipitation_mm"]


def create_sample_data(path=DATA_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rows = []
    for year in range(2015, 2025):
        for region_index, region in enumerate(["서울", "부산", "대구"]):
            rows.append({
                "date": "%d-07-15" % year,
                "year": year,
                "region": region,
                "avg_temperature": round(13.8 + (year - 2015) * 0.08 + region_index * 0.4, 2),
                "heatwave_days": 8 + (year - 2015) // 2 + region_index * 2,
                "precipitation_mm": 1350 - (year - 2015) * 12 + region_index * 85,
            })
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")


def load_climate_data(path=DATA_PATH):
    if not os.path.exists(path):
        create_sample_data(path)
    data = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError("필수 컬럼이 없습니다: %s" % ", ".join(missing))
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["year"] = pd.to_numeric(data["year"], errors="coerce").fillna(data["date"].dt.year)
    data["region"] = data["region"].astype(str).str.strip()
    for column in ["avg_temperature", "heatwave_days", "precipitation_mm"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=REQUIRED_COLUMNS).copy()
    data["year"] = data["year"].astype(int)
    return data.sort_values(["date", "region"]).reset_index(drop=True)