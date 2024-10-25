import gspread
from oauth2client.service_account import ServiceAccountCredentials
import difflib
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import json  # Add JSON to structure the output

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\xampp\\htdocs\\E-Learning-Website-HTML-CSS-main\\minor-project-439108-cc4a93fe43e4.json', scope)
client = gspread.authorize(creds)

course_sheet_id = "1HPsvg6oFH40R_7FY9MS8SYpqPPWNdItbqZFAOCbbNfY"
user_prefs_sheet_id = "1_T9r80LVnvwc5PKokC-GSen7GKITdB3JintqkAIKVvs"

course_sheet = client.open_by_key(course_sheet_id).sheet1
user_prefs_sheet = client.open_by_key(user_prefs_sheet_id).sheet1

courses = course_sheet.get_all_records()
user_prefs = user_prefs_sheet.get_all_records()

synonyms = {
    "ai": ["artificial intelligence", "ml", "machine learning"],
    "ml": ["machine learning", "ai", "artificial intelligence"],
    "data science": ["data analysis", "big data", "machine learning"],
}

def expand_synonyms(topic):
    normalized_topic = topic.lower()
    expanded_topics = {normalized_topic}
    for key, related_terms in synonyms.items():
        if normalized_topic == key or normalized_topic in related_terms:
            expanded_topics.update([key] + related_terms)
    return expanded_topics

def get_similarity_score(course_topic, interested_topics):
    max_similarity = 0
    expanded_course_topics = expand_synonyms(course_topic)
    for topic in interested_topics:
        expanded_interested_topics = expand_synonyms(topic)
        for expanded_course_topic in expanded_course_topics:
            for expanded_interested_topic in expanded_interested_topics:
                similarity = difflib.SequenceMatcher(None, expanded_course_topic, expanded_interested_topic).ratio()
                max_similarity = max(max_similarity, similarity)
    return max_similarity

if user_prefs:
    last_user = user_prefs[-1]
    interested_topics = [topic.strip().lower() for topic in last_user["Interested Fields/Subjects"].split(",")]

    similarity_data = [
        {
            "Course Name": course["Course Name"],
            "Course Link": course["Course Link"],
            "Course Topic": course["Course Topic"],
            "Pacing": course["Pacing"],
            "Learning Style": course["Learning Style"],
            "Similarity": get_similarity_score(course["Course Topic"], interested_topics)
        }
        for course in courses
    ]
    
    df = pd.DataFrame(similarity_data)
    df = df[df['Similarity'] > 0.4]

    if not df.empty:
        X = df[['Similarity']].values  
        knn = NearestNeighbors(n_neighbors=3, metric='euclidean')
        knn.fit(X)

        _, indices = knn.kneighbors([[1]])
        recommended_courses = df.iloc[indices[0]]

        # Prepare the structured JSON response
        recommended_list = recommended_courses.to_dict(orient='records')
        
        # Output as JSON string
        print(json.dumps(recommended_list))
    else:
        print(json.dumps({"error": "No courses found matching the preferences."}))
else:
    print(json.dumps({"error": "No user preferences found."}))
