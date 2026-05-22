# -*- coding: utf-8 -*-
"""Build canonical Golden Master snapshot string from domain scenarios."""
from __future__ import annotations

from feedback import Feedback
from filters import filter_feedbacks
from text_analyzer import TextAnalyzer, classify_sentiment

ANCHOR_TEXT = "배송이 너무 늦어요. 화가 납니다."
NEUTRAL_THREE_TEXTS = [
    "보통이에요",
    "괜찮아요",
    "특별한 불만 없음",
]
CATEGORY_MAIN_TEXT = "품질"


def _fmt_counts(data: dict) -> str:
    return ",".join(f"{key}={data[key]}" for key in sorted(data.keys()))


def capture_golden_master_output() -> str:
    lines: list[str] = []
    analyzer = TextAnalyzer()

    lines.append("=== GOLDEN_MASTER v1 ===")
    lines.append("encoding: utf-8")
    lines.append("scope: domain_sent_kw_filter")
    lines.append("")

    anchor = [Feedback(ANCHOR_TEXT)]
    lines.append("[anchor_prd]")
    lines.append(f"input={ANCHOR_TEXT}")
    lines.append(f"classify_sentiment={classify_sentiment(ANCHOR_TEXT)}")
    lines.append(f"sent={_fmt_counts(analyzer.sent(anchor))}")
    lines.append(f"kw={_fmt_counts(analyzer.kw(anchor))}")
    neg_ship = filter_feedbacks(anchor, "부정", "배송")
    lines.append(f"filter_negative_shipping_count={len(neg_ship)}")
    lines.append(
        "filter_negative_shipping_texts="
        + "|".join(item.text for item in neg_ship)
    )
    neg_all = filter_feedbacks(anchor, "부정", "전체")
    lines.append(f"filter_negative_all_count={len(neg_all)}")
    lines.append("")

    neutral = [Feedback(text) for text in NEUTRAL_THREE_TEXTS]
    lines.append("[neutral_three]")
    for index, text in enumerate(NEUTRAL_THREE_TEXTS, start=1):
        lines.append(f"line{index}={text}|sentiment={classify_sentiment(text)}")
    lines.append(f"sent={_fmt_counts(analyzer.sent(neutral))}")
    neutral_filtered = filter_feedbacks(neutral, "중립", "전체")
    lines.append(f"filter_neutral_count={len(neutral_filtered)}")
    lines.append("")

    quality = [Feedback(CATEGORY_MAIN_TEXT)]
    lines.append("[category_main_only]")
    lines.append(f"input={CATEGORY_MAIN_TEXT}")
    lines.append(f"kw={_fmt_counts(analyzer.kw(quality))}")
    quality_filtered = filter_feedbacks(quality, "전체", "품질")
    lines.append(f"filter_quality_count={len(quality_filtered)}")
    lines.append("")

    return "\n".join(lines) + "\n"
