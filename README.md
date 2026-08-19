# Climate Investigation

기후 데이터 분석, 시각화, OpenAI 탐사기사 생성, 데이터 기반 팩트체크를 제공하는 Streamlit 앱입니다.

## 실행

```powershell
cd project2-climate-investigation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

`OPENAI_API_KEY`가 없거나 API 호출에 실패해도 샘플 데이터와 로컬 초안으로 앱을 사용할 수 있습니다. 자체 CSV를 사용하려면 `data/climate_data.csv`를 만들고 다음 컬럼을 포함하세요: `date`, `year`, `region`, `avg_temperature`, `heatwave_days`, `precipitation_mm`.

생성된 기사는 `articles/investigation_article.md`, 팩트체크 결과는 `reports/fact_check_report.md`와 JSON 파일로 저장됩니다.