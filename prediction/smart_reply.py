"""
Smart Reply Generator for Sentiment Analysis
Generates contextual replies based on review sentiment and content.
"""

def generate_ai_reply(review_text, sentiment: str) -> str:
    """
    Suggest a professional customer-service reply using review context and sentiment.

    Uses rule-based logic (keywords such as delay, quality, size for negative feedback).
    """
    if review_text is None:
        return ""
    review_text = str(review_text).strip()
    if not review_text:
        return ""

    s = (sentiment or "Neutral").strip()
    if s not in ("Positive", "Negative", "Neutral"):
        s = "Neutral"

    review_lower = review_text.lower()

    if s == "Positive":
        return _generate_positive_reply(review_text, review_lower)
    if s == "Negative":
        return _generate_negative_reply(review_text, review_lower)
    return _generate_neutral_reply(review_text, review_lower)


def generate_smart_reply(review_text: str, sentiment: str) -> str:
    """Backward-compatible alias for :func:`generate_ai_reply`."""
    return generate_ai_reply(review_text, sentiment)


def _generate_positive_reply(review_text: str, review_lower: str) -> str:
    """Generate professional reply for positive reviews."""

    if any(word in review_lower for word in ["thank", "appreciate", "grateful", "love"]):
        return (
            "Thank you sincerely for taking the time to share such kind words. "
            "We are delighted that you had a positive experience, and your feedback "
            "reinforces our commitment to quality. We look forward to serving you again."
        )

    if any(word in review_lower for word in ["best", "amazing", "excellent", "outstanding", "perfect"]):
        return (
            "Thank you for your excellent feedback. We are pleased that our product met "
            "your expectations at a high level. Reviews like yours help us continue to "
            "deliver consistently for every customer."
        )

    if any(word in review_lower for word in ["quality", "reliable", "durable", "worth"]):
        return (
            "Thank you for highlighting the quality you experienced. We take pride in "
            "building reliable products, and we are grateful that this came through in "
            "your purchase. We appreciate your trust."
        )

    if any(word in review_lower for word in ["fast", "quick", "efficient", "timely"]):
        return (
            "Thank you for noting our timely service. We know your time is valuable, "
            "and we are glad we could deliver promptly. We hope to assist you again soon."
        )

    if any(word in review_lower for word in ["recommend", "suggest", "refer"]):
        return (
            "Thank you for recommending us. There is no greater compliment than a "
            "satisfied customer willing to share their experience. We truly appreciate your support."
        )

    snippet = review_text[:120] + ("…" if len(review_text) > 120 else "")
    return (
        f"Thank you for your thoughtful review. We are grateful for your positive comments"
        f' regarding "{snippet}" and for choosing us. Your feedback motivates our team, '
        f"and we remain committed to maintaining this standard for you and all our customers."
    )


def _generate_negative_reply(review_text: str, review_lower: str) -> str:
    """Generate apology + solution for negative reviews, with keyword-aware context."""

    # Shipping / delay — explicit "delay" plus related terms
    if any(
        word in review_lower
        for word in (
            "delay",
            "delayed",
            "late",
            "shipping",
            "delivery",
            "arrived",
            "package",
            "dispatch",
            "wait",
        )
    ):
        return (
            "We are sorry for the delay and frustration this caused. Timely delivery matters "
            "to us, and we understand how disappointing a late shipment can be. Please contact "
            "our support team with your order details so we can investigate what happened and "
            "offer a suitable resolution, which may include expedited shipping or compensation "
            "where appropriate."
        )

    # Quality / defects
    if any(
        word in review_lower
        for word in (
            "quality",
            "defect",
            "broken",
            "damaged",
            "poor quality",
            "cheap",
            "flimsy",
            "scratch",
            "tear",
        )
    ):
        return (
            "We sincerely apologize that the product did not meet our quality standards. "
            "That is not the experience we want for you. Please reach out with your order "
            "information and, if possible, photos of the issue so we can arrange a replacement, "
            "repair, or refund in line with our policy."
        )

    # Size / fit
    if any(
        word in review_lower
        for word in (
            "size",
            "sizing",
            "fit",
            "fits",
            "tight",
            "loose",
            "small",
            "large",
            "too big",
            "too small",
        )
    ):
        return (
            "We are sorry the sizing or fit did not work for you. We know how important "
            "the right fit is. Please contact us with your order number; we will help you "
            "with an exchange for a different size or a return, depending on availability "
            "and our returns policy."
        )

    if any(word in review_lower for word in ["service", "rude", "unresponsive", "unhelpful", "support"]):
        return (
            "We apologize for the service experience you described. Your concerns deserve "
            "a careful review. Please share the details with our team so we can address "
            "what went wrong and follow up with you directly."
        )

    if any(word in review_lower for word in ["expected", "not as", "disappointed", "misleading", "false"]):
        return (
            "We are sorry the product did not match what you expected. We take accuracy "
            "seriously and want to make this right. Please contact us with specifics so we "
            "can resolve the issue or arrange a return according to our guidelines."
        )

    if any(
        phrase in review_lower
        for phrase in ["doesn't work", "not working", "malfunction", "error", "bug"]
    ):
        return (
            "We apologize for the trouble you had with the product's performance. Our team "
            "can help troubleshoot or arrange a replacement if needed. Please reach out with "
            "your order details and a short description of the issue."
        )

    snippet = review_text[:120] + ("…" if len(review_text) > 120 else "")
    return (
        "We are truly sorry for the negative experience you shared. "
        f'We have noted your feedback regarding "{snippet}" and take it seriously. '
        "Please contact our customer support with your order information so we can "
        "investigate and work with you on a fair resolution."
    )


def _generate_neutral_reply(review_text: str, review_lower: str) -> str:
    """Generate professional reply for neutral reviews."""

    if any(word in review_lower for word in ["could", "should", "improve", "better", "wish", "suggest", "feedback"]):
        return (
            "Thank you for your balanced feedback. We appreciate you outlining what could "
            "be improved. If you are open to sharing more detail, our team would welcome "
            "the opportunity to learn from your experience and follow up as needed."
        )

    if any(word in review_lower for word in ["okay", "alright", "decent", "acceptable", "average", "so-so", "fine"]):
        return (
            "Thank you for your honest review. We are glad you found aspects of your "
            "experience acceptable, and we would like to earn a stronger recommendation "
            "next time. Please let us know if there is anything specific we can do better."
        )

    if "but" in review_lower or "however" in review_lower:
        return (
            "Thank you for the detailed review. We value both the positives and the areas "
            "you highlighted. Please feel free to contact us with any follow-up questions "
            "so we can support you further."
        )

    snippet = review_text[:120] + ("…" if len(review_text) > 120 else "")
    return (
        "Thank you for taking the time to share your thoughts. "
        f'We have read your comments regarding "{snippet}" and appreciate the input. '
        "If there is anything we can clarify or improve, our team is here to help."
    )


def enrich_replies_with_contact_info(reply: str, contact_email: str = "support@company.com", contact_url: str = None) -> str:
    """
    Replace placeholder contact information in the reply.

    Args:
        reply: The generated reply with placeholders
        contact_email: The actual contact email to use
        contact_url: Optional support URL to include

    Returns:
        Reply with contact information filled in
    """
    reply = reply.replace("[SUPPORT_EMAIL]", contact_email)

    if contact_url:
        reply = reply.replace("[SUPPORT_URL]", contact_url)

    return reply
