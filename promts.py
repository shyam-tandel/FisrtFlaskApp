
from datetime import date

today_date = date.today().strftime("%b %Y")  # Format as 'Jan 2025'
RESUME_PROMPT = f"""I want response from uploaded file in JSON format that starts and ends with curly brackets.
Here are the keys used in the response:
- name
- email
- address
- phone
- education (degree, institute, year)
- skills
- work_experience (company, position, start_date, end_date, duration : duration between start_date and         end_date i.e. 1.5,2.5,1.3,1.2,etc, location)
- total_work_experience : addition of work_experience (duration)

start_date and end_date should be in month and year format (e.g., Jan 2021, May 2024).  

If end_date is null or present or till now, set end_date as {today_date} and calculate experience based on the today date {today_date}.  

Calculate duration between start_date and end_date. 

"""


print(RESUME_PROMPT)

