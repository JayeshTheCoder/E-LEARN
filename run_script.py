import gspread
from oauth2client.service_account import ServiceAccountCredentials
import difflib  # For fuzzy matching

# Step 1: Authenticate and Access Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\Jayesh\\Desktop\\E-Learning-Website-HTML-CSS-main\\minor-project-439108-cc4a93fe43e4.json', scope)
client = gspread.authorize(creds)

# Step 2: Access Course Data and User Preferences Sheets
course_sheet_id = "1HPsvg6oFH40R_7FY9MS8SYpqPPWNdItbqZFAOCbbNfY"  # ID of the course data sheet
user_prefs_sheet_id = "1_T9r80LVnvwc5PKokC-GSen7GKITdB3JintqkAIKVvs"  # ID of the user preferences sheet

# Open the spreadsheets using the ID
course_sheet = client.open_by_key(course_sheet_id).sheet1  # Open course data sheet
user_prefs_sheet = client.open_by_key(user_prefs_sheet_id).sheet1  # Open user preferences sheet

# Step 3: Get All Course Data and User Preferences
courses = course_sheet.get_all_records()  # Get all course data as a list of dictionaries
user_prefs = user_prefs_sheet.get_all_records()  # Get all user preferences as a list of dictionaries

# Step 4: Define a synonym/related terms dictionary
synonyms = {
    "ai": ["artificial intelligence", "ml", "machine learning"],
    "ml": ["machine learning", "ai", "artificial intelligence"],
    "data science": ["data analysis", "big data", "machine learning"],
    # Add more terms as needed
}

# Helper function to expand synonyms for a topic
def expand_synonyms(topic):
    normalized_topic = topic.lower()
    expanded_topics = {normalized_topic}  # Start with the original topic

    # Expand using the synonym dictionary
    for key, related_terms in synonyms.items():
        if normalized_topic == key or normalized_topic in related_terms:
            expanded_topics.update([key] + related_terms)  # Add all related terms

    return expanded_topics

# Helper function for fuzzy matching topics and calculating similarity score
def get_similarity_score(course_topic, interested_topics):
    max_similarity = 0
    expanded_course_topics = expand_synonyms(course_topic)  # Expand synonyms for the course topic

    for topic in interested_topics:
        expanded_interested_topics = expand_synonyms(topic)  # Expand synonyms for the interested topic
        for expanded_course_topic in expanded_course_topics:
            for expanded_interested_topic in expanded_interested_topics:
                similarity = difflib.SequenceMatcher(None, expanded_course_topic, expanded_interested_topic).ratio()
                max_similarity = max(max_similarity, similarity)  # Track the highest similarity score

    return max_similarity

# Step 5: Process the Last User's Preferences and Filter Courses
if user_prefs:  # Check if there are any user preferences
    last_user = user_prefs[-1]  # Get the last user in the list
    interested_topics = [topic.strip().lower() for topic in last_user["Interested Fields/Subjects"].split(",")]
    pacing_preference = last_user["Pacing Preferences"].lower()
    learning_style_preference = last_user["Preferred Learning Style"].lower()

    print(f"Recommending Courses Based On Your Preferences....")
    print("Here are some courses recommended to you based on your preferences:")
    print(f"Interested Fields: {interested_topics}")
    print(f"Pacing: {pacing_preference}")
    print(f"Learning Style: {learning_style_preference}")
    print("----Recommending----")

    # Step 6: Filter and Rank Courses Based on Similarity Score
    ranked_courses = [
        {
            "course": course,
            "similarity": get_similarity_score(course["Course Topic"], interested_topics)
        }
        for course in courses
        if get_similarity_score(course["Course Topic"], interested_topics) > 0.4  # Only include courses with a similarity score > 0.4
    ]

    # Sort courses by similarity score in descending order
    ranked_courses.sort(key=lambda x: x["similarity"], reverse=True)

    # Step 7: Display Filtered Courses Ranked by Similarity
    if ranked_courses:
        displayed_courses = 0
        for ranked_course in ranked_courses:
            course = ranked_course["course"]
            similarity_score = ranked_course["similarity"]

            # Display courses that match at least one preference even if not exact
            if (pacing_preference in course["Pacing"].lower() or pacing_preference == "any" or similarity_score == 1) and \
               (learning_style_preference in course["Learning Style"].lower() or learning_style_preference == "any" or similarity_score == 1):
                print(f"- {course['Course Name']} ({course['Course Link']}) [Similarity: {similarity_score:.2f}]")
                displayed_courses += 1

        # Fallback: Display more courses if very few are found
        if displayed_courses == 0:
            print("No exact matches, showing courses based on topic relevance:")
            for ranked_course in ranked_courses:
                course = ranked_course["course"]
                similarity_score = ranked_course["similarity"]
                print(f"- {course['Course Name']} ({course['Course Link']}) [Similarity: {similarity_score:.2f}]")
    else:
        print("No courses found matching the preferences.")

    print("\n-------------------------\n")
else:
    print("No user preferences found.")