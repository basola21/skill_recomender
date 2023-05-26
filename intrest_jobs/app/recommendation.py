import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Step 1: Load the CSV file
data = pd.read_csv('/Users/basel/Documents/Projects/Intrest jobs project/intrest_jobs/scripts/jobs.csv')

# Step 2: Data Preprocessing
data = data.drop("Unnamed: 0",axis=1)
data['Key Skills'] = data['Key Skills'].str.replace('|',',')

# Step 3: Feature Extraction
# Convert job titles and key skills into numerical representations
vectorizer = TfidfVectorizer()
job_titles_skills = data['Job Title'] + ' ' + data['Key Skills']
job_title_skills_vectors = vectorizer.fit_transform(job_titles_skills)

# Step 4: Training the Model
# Build and train a machine learning model
model = NearestNeighbors(n_neighbors=5, metric='cosine')
model.fit(job_title_skills_vectors)

# Step 5: User Interface
def get_best_skills(job_title):
    # Convert the user input job title into a numerical vector
    user_input_vector = vectorizer.transform([job_title])

    # Find the nearest neighbors based on cosine similarity
    distances, indices = model.kneighbors(user_input_vector)

    # Retrieve the best suited skills for the job title
    best_skills = data.iloc[indices[0]]['Key Skills']

    # transform the best skills into a list
    best_skills = best_skills.tolist()

    return best_skills

