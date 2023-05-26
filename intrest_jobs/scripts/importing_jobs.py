import csv
from app.models import Job, Skill

file_path = '/Users/basel/Documents/Projects/Intrest jobs project/intrest_jobs/scripts/jobs.csv'

with open(file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    total_rows = sum(1 for _ in reader)
    csvfile.seek(0)  # Reset the file pointer to the beginning
    next(reader)  # Skip the header row
    
    for i, row in enumerate(reader, start=1):
        title = row['Job Title']
        skills = row['Key Skills'].split('|')
        
        job = Job.objects.create(title=title)
        
        for skill_name in skills:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            job.skills.add(skill)
        
        job.save()
        
        print(f'Processed {i}/{total_rows} rows')
