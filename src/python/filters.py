# -*- coding: utf-8 -*-
from typing import List
from feedback import Feedback
from text_analyzer import classify_sentiment, matches_category


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

    # Keyword (category) filtering (B-02: same main-only rule as TextAnalyzer.kw)
    if keyword_filter != "전체":
        final_filtered = [
            item
            for item in tmp_filtered
            if matches_category(item.text, keyword_filter)
        ]
    else:
        final_filtered = tmp_filtered

    return final_filtered
