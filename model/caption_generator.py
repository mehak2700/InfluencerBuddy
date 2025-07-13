def generate_caption(topic, tone, platform, category):
    base = f"As a {category.lower()} content creator on {platform}, here’s a {tone.lower()} caption about {topic.lower()}: "

    body = (
        f"{topic} is not just a trend—it's a way of expressing who you are. "
        f"In the world of {category.lower()}, authenticity matters more than perfection. "
        f"Let your content speak from the heart and inspire others. "
        f"Stay true to yourself, trust the journey, and share what matters most."
    )

    closing = " 💬 What’s your take on this? Drop your thoughts below! 👇"

    return base + body + closing
