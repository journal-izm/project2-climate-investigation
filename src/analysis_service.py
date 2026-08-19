import pandas as pd


def build_analysis(data):
    if data.empty:
        raise ValueError("분석할 데이터가 없습니다.")
    yearly = data.groupby("year", as_index=False).agg(
        mean_temperature=("avg_temperature", "mean"),
        heatwave_days=("heatwave_days", "mean"),
        precipitation_mm=("precipitation_mm", "mean"),
    ).sort_values("year")
    if len(yearly) > 1:
        slope = float(yearly["mean_temperature"].corr(yearly["year"]) * yearly["mean_temperature"].std() / yearly["year"].std())
    else:
        slope = 0.0
    first_temperature = yearly.iloc[0]["mean_temperature"]
    last_temperature = yearly.iloc[-1]["mean_temperature"]
    change = last_temperature - first_temperature
    return {
        "yearly_summary": yearly.round(2),
        "temperature_by_year": yearly[["year", "mean_temperature"]],
        "heatwave_by_year": yearly[["year", "heatwave_days"]],
        "precipitation_by_year": yearly[["year", "precipitation_mm"]],
        "overall_mean_temperature": float(data["avg_temperature"].mean()),
        "overall_mean_heatwave_days": float(data["heatwave_days"].mean()),
        "average_annual_precipitation": float(yearly["precipitation_mm"].mean()),
        "temperature_trend_per_year": slope,
        "temperature_change": float(change),
        "heatwave_change": float(yearly.iloc[-1]["heatwave_days"] - yearly.iloc[0]["heatwave_days"]),
        "precipitation_change": float(yearly.iloc[-1]["precipitation_mm"] - yearly.iloc[0]["precipitation_mm"]),
        "summary": "평균기온은 시작 연도 대비 마지막 연도에 %.2f°C 변했고, 폭염일수는 %.1f일 변했습니다." % (change, yearly.iloc[-1]["heatwave_days"] - yearly.iloc[0]["heatwave_days"]),
    }