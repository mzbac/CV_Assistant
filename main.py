import requests

from tools import search_web, web_pages_content

ANTHROPIC_API_KEY = "YOUR KEY HERE"  # Replace with your Anthropic API key


def calling_agent(role: str, goal: str, backstory: str, task: str) -> str:
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        # "anthropic-beta": "tools-2024-04-04",
        "content-type": "application/json",
    }

    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 2000,
        "temperature": 0,
        "system": f"You are a {role}, {backstory}, your goal is to {goal}.",
        "messages": [{"role": "user", "content": f"here is the task: {task}"}],
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages", headers=headers, json=data
    )
    if response.status_code == 200:
        response_data = response.json()
        completion_text = response_data["content"][0]["text"].strip()
        return completion_text
    else:
        print("Error:", response.status_code, response.text)


def calling_search_agent(role: str, goal: str, backstory: str, task: str) -> str:
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "tools-2024-04-04",
        "content-type": "application/json",
    }

    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 2000,
        "temperature": 0,
        "system": f"You are a {role}, {backstory}, your goal is to {goal}.",
        "messages": [{"role": "user", "content": f"here is the task: {task}"}],
        "tools": [
            {
                "name": "search_web",
                "description": "Perform a web search for a given search terms.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "search_terms": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "The search queries for which the web search is performed.",
                        }
                    },
                    "required": ["search_terms"],
                },
            }
        ],
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages", headers=headers, json=data
    )
    if response.status_code == 200:
        response_data = response.json()
        response_data = response_data["content"]
        for content in response_data:
            if content["type"] == "tool_use":
                response_data = content
                break

        search_queries = content["input"]["search_terms"]
        return search_queries
    else:
        print("Error:", response.status_code, response.text)


def calling_verification_agent(role: str, goal: str, backstory: str, task: str) -> str:
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "tools-2024-04-04",
        "content-type": "application/json",
    }

    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 2000,
        "temperature": 0,
        "system": f"You are a {role}, {backstory}, your goal is to {goal}.",
        "messages": [{"role": "user", "content": f"here is the task: {task}"}],
        "tools": [
            {
                "name": "web_pages_content",
                "description": "Perform read web contents for a given urls.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "urls": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "The urls for which the web page need to access is performed.",
                        }
                    },
                    "required": ["urls"],
                },
            }
        ],
    }
    response = requests.post(
        "https://api.anthropic.com/v1/messages", headers=headers, json=data
    )
    if response.status_code == 200:
        response_data = response.json()
        response_data = response_data["content"]
        for content in response_data:
            if content["type"] == "tool_use":
                response_data = content
                break

        search_queries = content["input"]["urls"]
        return search_queries
    else:
        print("Error:", response.status_code, response.text)


with open("job_description.md", "r") as file:
    job_description = file.read()

job_analyst_result = calling_agent(
    "Job Requirement Analyst",
    "Analyze the job posting to extract key requirements, skills, and qualifications needed.",
    "Specializes in dissecting job postings to identify critical skills and qualifications for a role.",
    f"Analyze the job description provided to identify key requirements, skills, and qualifications needed for the position. Job Description: ```{job_description}```. Focus on understanding the specific needs and expectations mentioned in the job posting, and how they align with the industry standards and trends.",
)

print(job_analyst_result)

search_queries = calling_search_agent(
    "SearchQueryGenerator",
    "Converts the detailed job analysis into targeted Google search queries for further validation of the skills and qualifications.",
    "Specializes in synthesizing job requirements, skills, and qualifications into search queries to verify their relevance and demand in the current job market.",
    f"""Generate Google search queries based on the analysis provided by the Job Requirement Analyst. Use the extracted key requirements, skills, and qualifications to formulate queries aimed at validating these elements against industry standards and trends. Job Analyst Result: ```{job_analyst_result}```. Focus on crafting queries that will bring up authoritative and relevant information, allowing for a comprehensive validation process.""",
)

search_query = " ".join(search_queries)
search_reuslt = search_web(search_query)

verification_urls = calling_verification_agent(
    "VerificationAgent",
    "Analyzes content from specific URLs to verify the Job Analyst Result, focusing on industry relevance and demand for skills and qualifications.",
    "Specializes in web content analysis for the purpose of validating job market trends and requirements against job analysis.",
    f"""Based on the search results, identify and analyze content from authoritative URLs to verify the Job Analyst Result. Utilize advanced content analysis techniques to assess the relevance and accuracy of the identified skills and qualifications. Generate a report summarizing findings and their implications for the job analysis. Search Results: ```{search_reuslt}```. The focus is on extracting and analyzing information that directly relates to the job requirements, skills, and qualifications listed by the Job Requirement Analyst.""",
)

page_contents = web_pages_content(verification_urls)

verification_result = "\n\n".join(page_contents)

refined_job_analyst_result = calling_agent(
    "JobAnalysisRefiner",
    "Refines job analysis by integrating verification results to ensure alignment with current industry standards.",
    "Leverages insights from content verification to enhance the accuracy of job requirements, skills, and qualifications analysis.",
    f"""Refine the initial job analysis by comparing it with the verification results. Update the job requirements, skills, and qualifications to reflect verified industry standards and demands. Job Description: ```{job_description}```. Initial Job Analyst Result: ```{job_analyst_result}```. Verification Result: ```{verification_result}```. Focus on ensuring the refined job analysis is comprehensive and accurately aligned with the current job market, providing a solid foundation for CV updates and job application strategies.""",
)

print("Refined Job Analyst Result:")
print(refined_job_analyst_result)

with open("cv.md", "r") as file:
    cv_text = file.read()

profile_analyst_result = calling_agent(
    "Profile Analyst",
    "Review the current CV, to identify relevant skills, experiences, and projects.",
    "Expert in analyzing technical profiles and CVs to highlight relevant experiences and projects.",
    f"Based on the job analyst result: ```{refined_job_analyst_result}```.\nReview the candidate's current CV : ```{cv_text}```. Extract relevant skills, experiences, and projects that align with the job requirements. Focus on identifying standout achievements and contributions that can enhance the candidate's appeal for the position.",
)

print("Profile Analyst Result:")
print(profile_analyst_result)

cv_update_result = calling_agent(
    "CV Update Specialist",
    "Use insights from the Job Requirement Analyst and Profile Analyst to update the CV, making it tailored to the job post.",
    "Skilled in refining CVs to align with job requirements and showcase the candidate in the best light.",
    f"Based on the profile analyst result: ```{profile_analyst_result}```.\nUse the insights from the job requirements report:```{refined_job_analyst_result}``` and the candidate CV: ```{cv_text}``` to update the candidate's CV. Ensure that the CV aligns with the job description, highlighting relevant skills, experiences, and achievements. The updated CV should be tailored to reflect the candidate's suitability for the role, making use of persuasive and impactful language to capture the hiring manager's attention.",
)

print("CV Update Result:")
print(cv_update_result)

with open("updated_cv.md", "w") as file:
    file.write(cv_update_result)

final_cv = calling_agent(
    "CV Review and Refinement Specialist",
    "Review the updated CV for clarity, relevance, grammatical accuracy, and alignment with job requirements.",
    "A meticulous editor focused on ensuring the CV is perfectly tailored to the job and error-free.",
    f"Based on the Job Description:```{job_description}``` and the CV update result: ```{cv_update_result}```.\nReview the updated CV for clarity, relevance, grammatical accuracy, and overall impact. Ensure that the CV is free from errors and that it effectively communicates the candidate's qualifications and suitability for the role. Provide the final refined CV.",
)

print("Final CV:")
print(final_cv)

with open("final_cv.md", "w") as file:
    file.write(final_cv)
