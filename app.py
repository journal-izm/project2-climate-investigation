# Climate Investigation Project
import os

import streamlit as st

from src.analysis_service import build_analysis
from src.article_service import generate_article, save_article
from src.data_service import load_climate_data
from src.factcheck_service import fact_check_article, save_fact_check


st.set_page_config(page_title="Climate Investigation", page_icon="🌍", layout="wide")
st.title("Climate Investigation")
st.caption("기후 데이터 분석부터 AI 탐사기사와 데이터 기반 팩트체크까지")

try:
	climate_df = load_climate_data()
	analysis = build_analysis(climate_df)
except Exception as error:
	st.error("기후 데이터를 불러오지 못했습니다: %s" % error)
	st.stop()

with st.sidebar:
	st.header("분석 조건")
	regions = sorted(climate_df["region"].dropna().unique().tolist())
	selected_region = st.selectbox("지역", ["전체"] + regions)
	filtered_df = climate_df if selected_region == "전체" else climate_df[climate_df["region"] == selected_region]
	filtered_analysis = build_analysis(filtered_df)
	st.write("관측 기간: %s ~ %s" % (climate_df["date"].min().date(), climate_df["date"].max().date()))

st.subheader("핵심 분석값")
metric_columns = st.columns(4)
metric_columns[0].metric("평균기온", "%.1f °C" % filtered_analysis["overall_mean_temperature"])
metric_columns[1].metric("폭염일수 평균", "%.1f일" % filtered_analysis["overall_mean_heatwave_days"])
metric_columns[2].metric("연평균 강수량", "%.1f mm" % filtered_analysis["average_annual_precipitation"])
metric_columns[3].metric("기온 추세", "%+.2f °C/년" % filtered_analysis["temperature_trend_per_year"])

tab_analysis, tab_article, tab_factcheck = st.tabs(["데이터 분석", "AI 탐사기사", "팩트체크"])
with tab_analysis:
	st.subheader("연도별 추세")
	chart_columns = st.columns(3)
	chart_columns[0].line_chart(filtered_analysis["temperature_by_year"].set_index("year")["mean_temperature"])
	chart_columns[0].caption("평균기온 (°C)")
	chart_columns[1].bar_chart(filtered_analysis["heatwave_by_year"].set_index("year")["heatwave_days"])
	chart_columns[1].caption("폭염일수")
	chart_columns[2].bar_chart(filtered_analysis["precipitation_by_year"].set_index("year")["precipitation_mm"])
	chart_columns[2].caption("연강수량 (mm)")
	st.dataframe(filtered_analysis["yearly_summary"], use_container_width=True, hide_index=True)
	st.info("분석 근거: %s" % filtered_analysis["summary"])

with tab_article:
	st.subheader("AI 탐사기사")
	if st.button("기사 생성", type="primary"):
		with st.spinner("기사 작성 중..."):
			article, message = generate_article(filtered_analysis, selected_region)
		st.session_state["article"] = article
		save_article(article)
		st.success(message)
	article = st.session_state.get("article")
	if article:
		st.markdown(article)
		st.download_button("기사 다운로드", article, "climate_investigation_article.md")
	else:
		st.info("분석 결과를 바탕으로 기사를 생성하세요.")

with tab_factcheck:
	st.subheader("기사와 실제 분석 결과 비교")
	article = st.session_state.get("article")
	if not article:
		st.info("먼저 AI 탐사기사 탭에서 기사를 생성하세요.")
	elif st.button("팩트체크 실행", type="primary"):
		with st.spinner("기사의 주장을 분석 결과와 대조 중..."):
			result = fact_check_article(article, filtered_analysis)
		st.session_state["factcheck"] = result
		save_fact_check(result)
	result = st.session_state.get("factcheck")
	if result:
		st.metric("판정", result["status"])
		st.write(result["reason"])
		for claim in result["claims"]:
			with st.expander("[%s] %s" % (claim["status"], claim["claim"])):
				st.write(claim["evidence"])
				st.write(claim["explanation"])

st.caption("저장 위치: %s, %s" % (os.path.join("articles", "investigation_article.md"), os.path.join("reports", "fact_check_report.md")))
# Climate Investigation Project\n\nprint('Climate Investigation project initialized.')\n
