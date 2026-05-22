# -*- coding: utf-8 -*-
from typing import List
from feedback import Feedback
from constants import CATEGORY_KEYWORDS
from text_analyzer import classify_sentiment, TextAnalyzer


def _contains_any(text: str, keywords: List[str]) -> bool:
    return TextAnalyzer._contains_any(text, keywords)


def filter_feedbacks(
    data_list: List[Feedback],
    sentiment_filter: str,
    keyword_filter: str,
) -> List[Feedback]:
    # Sentiment filtering (B-01: same rules as TextAnalyzer.sent)
    if sentiment_filter != "전체":
        tmp_filtered = []
        for item in data_list:
            if classify_sentiment(item.text) == sentiment_filter:
                tmp_filtered.append(item)
    else:
        tmp_filtered = list(data_list)

    # Keyword (category) filtering
    if keyword_filter != "전체":
        final_filtered = []
        if keyword_filter in CATEGORY_KEYWORDS:
            cat_map = CATEGORY_KEYWORDS[keyword_filter]
            for item in tmp_filtered:
                txt = item.text
                for sub_key, sub_keywords in cat_map.items():
                    if sub_key == "main":
                        continue
                    if _contains_any(txt, sub_keywords):
                        final_filtered.append(item)
                        break
    else:
        final_filtered = tmp_filtered

    for fb in final_filtered:
        print(fb.text)

    return final_filtered
