def suggest_hashtags(topic, category):
    base_hashtags = [
        f"#{topic.lower()}",
        f"#{category.lower()}life",
        f"#{topic.lower()}daily",
        f"#{category.lower()}style",
        f"#{topic.lower()}community",
        f"#{topic.lower()}inspiration",
        f"#{category.lower()}lovers",
        f"#explore{category.lower()}",
        f"#trending{topic.lower()}",
        f"#influencer{category.lower()}",
    ]

    return base_hashtags
