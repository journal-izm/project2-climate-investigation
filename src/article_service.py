import os

from dotenv import load_dotenv

load_dotenv()


def _prompt(analysis, region):
    return """기후 데이터 탐사기사 작성. 지역: %s
분석값: 평균기온 %.2f°C, 기온 변화 %.2f°C, 연평균 강수량 %.2fmm, 폭염일수 변화 %.1f일.
수치를 임의로 추가하지 말고 제목, 리드, 본문, 데이터 근거와 한계를 포함한 한국어 기사로 작성하라.""" % (region, analysis["overall_mean_temperature"], analysis["temperature_change"], analysis["average_annual_precipitation"], analysis["heatwave_change"])


def generate_article(analysis, region="전체"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_article(analysis, region), "OPENAI_API_KEY가 없어 분석 근거 기반 초안으로 표시했습니다."
    try:
        from openai import OpenAI
        response = OpenAI(api_key=api_key).chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "system", "content": "너는 데이터 저널리스트다."}, {"role": "user", "content": _prompt(analysis, region)}],
            temperature=0.3,
        )
        return response.choices[0].message.content, "OpenAI가 기사를 생성했습니다."
    except Exception as error:
        return _fallback_article(analysis, region), "OpenAI 오류로 로컬 근거 기반 초안을 표시했습니다: %s" % error


def _fallback_article(analysis, region):
    return "# %s 기후 변화, 데이터가 보여주는 추세\n\n%s 지역의 분석 기간 평균기온은 %.2f°C이며, 시작 연도와 마지막 연도 사이 %.2f°C 변했습니다. 같은 기간 폭염일수 평균은 %.1f일 변했고 연평균 강수량은 %.2fmm였습니다. 이 결과는 제공된 관측 데이터의 평균값에 근거하며, 원인과 미래 예측을 의미하지 않습니다." % (region, region, analysis["overall_mean_temperature"], analysis["temperature_change"], analysis["heatwave_change"], analysis["average_annual_precipitation"])


def save_article(article, path=os.path.join("articles", "investigation_article.md")):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(article)