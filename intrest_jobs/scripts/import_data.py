import csv
from app.models import Job, Skill

# Open the CSV file and read the data
with open('/Users/basel/Documents/Projects/Intrest jobs project/intrest_jobs/scripts/occupation_intrest_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Create a new job instance
        job = Job.objects.create(
            title=row['title'],
            description=row['descriptionskills'],
            interest=row['intrest'],
        )

        # Add skills to the job instance
        skill_names = row['skills'].split(',')
        for skill_name in skill_names:
            skill, created = Skill.objects.get_or_create(name=skill_name.strip())
            job.skills.add(skill)

        # Save the job instance
        job.save()
