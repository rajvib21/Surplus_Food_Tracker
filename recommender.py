def recommend(donations, food_query):
    results = []
    food_query = food_query.lower()

    for d in donations:
        score = 0
        if food_query in d["title"].lower():
            score += 2
        if food_query in d["description"].lower():
            score += 1
        if score > 0:
            results.append((d, score))

    return sorted(results, key=lambda x: x[1], reverse=True)
