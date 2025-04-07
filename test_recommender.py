from recommender import get_recommendations

# Try out any natural language query or job description
query = "We are looking for a software developer with strong problem solving and numerical skills"

# Get top 5 relevant SHL assessments
recommendations = get_recommendations(query, top_k=5)

# Print them
for i, rec in enumerate(recommendations, 1):
    print(f"\n{i}. {rec['Assessment Name']}")
    print(f"   URL: {rec['URL']}")
    print(f"   Remote Testing: {rec['Remote Testing Support']}")
    print(f"   Adaptive: {rec['Adaptive Support']}")
    print(f"   Duration: {rec['Duration']}")
    print(f"   Test Type: {rec['Test Type']}")
    print(f"   Description: {rec['Description']}")
