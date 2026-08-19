import json
import os
import re


def fact_check_article(article, analysis):
    claims = []
    checks = [
        ("평균기온", analysis["overall_mean_temperature"], "°C"),
        ("연평균 강수량", analysis["average_annual_precipitation"], "mm"),
    ]
    for label, value, unit in checks:
        label_position = article.find(label)
        nearby_text = article[label_position:label_position + 80] if label_position >= 0 else ""
        matches = re.findall(r"[-+]?\d+(?:[.,]\d+)?", nearby_text)
        if label_position < 0:
            status = "근거부족"
            explanation = "기사에서 검증 대상 주장을 확인할 수 없습니다."
        elif not matches:
            status = "근거부족"
            explanation = "주장은 있으나 비교할 숫자가 없습니다."
        else:
            mentioned_value = float(matches[0].replace(",", "."))
            status = "사실" if abs(mentioned_value - value) <= max(0.1, abs(value) * 0.02) else "불일치"
            explanation = "기사 수치가 분석값의 2% 이내입니다." if status == "사실" else "기사 수치가 분석값과 다릅니다."
        claims.append({"claim": "%s 수치" % label, "status": status, "evidence": "분석값: %.2f %s" % (value, unit), "explanation": explanation})
    statuses = [claim["status"] for claim in claims]
    status = "불일치" if "불일치" in statuses else ("근거부족" if "근거부족" in statuses else "사실")
    return {"status": status, "reason": "기사의 수치 주장을 계산된 분석 결과와 대조했습니다.", "claims": claims, "article": article}


def save_fact_check(result, path=os.path.join("reports", "fact_check_report.md")):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write("# 기후 탐사기사 팩트체크\n\n- 전체 판정: %s\n- %s\n\n" % (result["status"], result["reason"]))
        for claim in result["claims"]:
            file.write("## [%s] %s\n%s\n%s\n\n" % (claim["status"], claim["claim"], claim["evidence"], claim["explanation"]))
    with open(os.path.join(os.path.dirname(path), "fact_check_report.json"), "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)