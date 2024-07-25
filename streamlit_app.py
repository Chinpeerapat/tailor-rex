import streamlit as st
import anthropic
import os

# Function to extract text from a given text block
def extract_text(text, start_tag, end_tag):
    pattern = rf'<{re.escape(start_tag)}>(.*?)</{re.escape(end_tag)}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return f"No content found between <{start_tag}> and </{end_tag}>"

# Function to process text blocks for summary and skills extraction
def pretty_print(message):
    # Extract the text from the TextBlock object
    text = message[0].text
    # Return the formatted string instead of just printing it
    return '\n\n'.join('\n'.join(line.strip() for line in re.findall(r'.{1,100}(?:\s+|$)', paragraph.strip('\n'))) for paragraph in re.split(r'\n\n+', text))

def extract_achievements(text):
    achievements_pattern = r"- (.+?)(?=\n\n|\Z)"
    return re.findall(achievements_pattern, text, re.DOTALL)

def extract_skills(text):
    skills_pattern = r"\d+\.\s(.+)"
    return re.findall(skills_pattern, text)

def format_output(summary, skills):
    # Extract the actual summary text and achievements
    summary_text = re.sub(r"== Profile Summary\n#chiline\(\)\n", "", summary).strip()
    achievements = extract_achievements(summary)

    # Extract skills from the skills text
    skill_list = extract_skills(skills)

    output = "== Profile Summary\n#chiline()\n"
    output += f"*{summary_text}*\n\n"

    for achievement in achievements[:3]:  # Limit to 3 achievements
        output += f"- {achievement.strip()}\n#v(0.5em)\n"

    output += "\n== Areas of Expertise\n#chiline()\n"
    output += "#columns(3)[\n"

    for i in range(0, len(skill_list), 4):
        output += "  #align(center)[\n"
        for skill in skill_list[i:i+4]:
            output += f"    {skill}\\\n"
        output += "  ]\n"
        if i < 8:  # Add colbreak for the first two columns
            output += "#colbreak()\n"

    output += "]"

    return output

# Streamlit app
def main():
    st.title("Resume Tailor with Anthropic API")
    
    # Get the API key from the user
    api_key = st.text_input("Enter your Anthropic API key:", type="password")
    
    if not api_key:
        st.warning("Please enter your API key to proceed.")
        return

    os.environ['ANTHROPIC_API_KEY'] = api_key
    
    # Get user inputs
    job_description = st.text_area("Job Description", height=200)
    
    if st.button("Tailor Resume"):
        client = anthropic.Anthropic(api_key=api_key)

        prompt = f"""You are tasked with tailoring a resume for a specific job role. You will be provided with the current resume, including the profile summary, and the job description. Your goal is to:

        1. Rewrite the profile summary to align with the job requirements.
        2. Identify and rank the top 12 skills that are both possessed by the candidate and valuable for the target job.

        First, you will be given the current resume:

        <resume>
        Peerapat Chiaprasert (Chin)
peerapat.chiaprasert@gmail.com|(+66)86-624-6630|linkedin.com/in/chpeerapat |BKK, Thailand
Profile Summary
Result-oriented leader with 8+ years of experience driving high impact initiatives, launching new businesses, and scaling teams. Proven track record in managing end-to-end operations, implementing data-driven strategies, and collaborating with stakeholders to deliver results
Led the successful launch of GrabFood in Thailand, crafting and executing a comprehensive go-to-market strategy and building key business functions to roll out the service in 6 weeks
Pioneered the GrabKitchen concept in Thailand, conducting detailed market research and using extensive data points to identify supply-demand gaps and growth opportunities.
Accelerated GrabKitchen expansion through innovative commercial strategy, and leading strategic partnerships that resulted in a profitable and scalable business model
Areas Of Expertise
Strategic Planning & Execution 	• Project Management		•  Team Leadership
Cross-Functional Collaboration 	• P&L Management 			•   Analytical thinking
Innovative Growth Strategies 	• Commercial Strategy	 	• Go-to-Market Strategy
e-Commerce Strategy 		• Online Platform Operations	• Stakeholders Management
 Professional Experience
TiffinLabs ⬝ Bangkok, Thailand	Mar 2022 - Oct 2023
Country General Manager
Expanded TiffinLabs' presence to 100 storefronts of delivery-centric brands. Built and directed the entire business team, namely, marketing, business development, and operations.
Crafted product value proposition to launch 7 delivery-focused food brands, defining brand roadmap to ensure product-market fit while setting up process to capture changing trends.
Improved GMV by 20% on monthly basis, streamlining the company’s marketing plans with the delivery platform to maximize NPD sales, and scheduling regular product enhancements.
Reduced COGS by 15% from initiating fulfillment partnership with distributor, crafting and negotiating terms, achieving target price, quality and faster sourcing process
Grab ⬝ Bangkok, Thailand	Jun 2017 - Feb 2022
Head, GrabKitchen (2019 - 2022)
Established GrabKitchen as the largest cloud kitchen network in Thailand, developing an asset-lite model and securing a strategic partnership with a top F&B company, CRG.
Achieved 20% GMV uplift and 4x ROI from initiating and managing marketing campaigns, including thematic campaigns, strategic partnerships, and JBPs.
Developed feasibility model to ensure profitability of individual kitchens and calculate payback period, constructing the model based on historical performance and demand trends data
Maintained high retention rate at all kitchen locations with 90% occupancy and less than 10% churn rate by using effective selection and pitching frameworks.
Developed and maintained a portfolio valued at more than 400 mn THB in annual GMV from more than 120 accounts, including street vendors, local chains, QSRs, and strategic partners.
Operations Manager, GrabFood | Special Project Lead, GrabBike & GrabExpress (2017–2019)
Propelled GrabFood to be market leader with within 8 months and established key functions including fleet management, business development, operations, and customer services
Developed and executed a highly impactful go-to-market e-commerce strategy for national brands such as MK, Starbucks, After You, Tim Hortons, CRG, MINOR, etc.
Formed and fostered high-performing teams across different functions and locations, overseeing more than 100 staff members, including 7 direct reports.
Contributed 10% GMV increment from launching 3PL services, Collaborating with B2B sales team to assess market opportunities, creating commercial terms, and leading sales pitches
Ipsos Business Consulting ⬝ Bangkok, Thailand	Jul 2016 - Jun 2017
Associate Consultant
Formulated e-payment business model and selected strategic partners to ensure a successful launch, assessing feasibility through extensive discussion with key players and regulators.
Crafted a go-to-market strategy for a Thai financial institution, assessing potentials and business models for the launch of e-commerce business
EY (Ernst & Young) ⬝ Bangkok, Thailand	Feb 2015 - Jun 2016
Consultant
Developed a costing model to identify service costs, addressing profitability issues for the Ministry of Public Health, including field visits at hospitals across the country.
Improved efficiency for listed manufacturing companies using ​​business process improvement framework, designing and implementing end-to-end accounting and finance flows.
Education
Thammasat University ⬝ Bangkok, Thailand	Jun 2011 - Dec 2014
Bachelor’s in Accounting (International Program)
        </resume>

        Next, you will be provided with the job description:

        <job_description>
        {job_description}
        </job_description>

        Analyze both documents carefully, noting key requirements, skills, and qualifications sought by the employer.

        Part 1: Profile Summary
        Rewrite the profile summary to better align with the job description. Focus on highlighting the candidate's most relevant skills, experiences, and achievements that match the job requirements. Use strong, action-oriented language and quantify achievements where possible.

        Format your output as follows:

        <output>
        == Profile Summary
        #chiline()
        [key statement]

        - [Key achievement 1]
        - [Key achievement 2]
        - [Key achievement 3]
        </output>

        Part 2: Skill Ranking
        Identify skills that are both mentioned in the resume (or can be reasonably inferred from the candidate's experience) and are relevant to the job description. Select and rank the top 12 skills based on candidate's level of expertise and relevancy to the job.

        Present your final list of 12 skills in descending order of importance using the following format:

        <skill_list>
        1. [Skill Name]
        2. [Skill Name]
        [Continue for all 12 skills]
        </skill_list>

        Ensure that your justifications are concise but informative, explaining why each skill is valuable for the job and how the candidate's experience demonstrates their proficiency."""

        # Create the message
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""{prompt}"""
                        }
                    ]
                }
            ]
        )

        new_summary = message.content

        tailor_resume = pretty_print(new_summary)
        tailor_summary = extract_text(tailor_resume, "output", "output")
        tailor_skills = extract_text(tailor_resume, "skill_list", "skill_list")
        formatted_output = format_output(tailor_summary, tailor_skills)

        st.subheader("Tailored Profile Summary")
        st.text_area("Profile Summary", value=tailor_summary, height=200)

        st.subheader("Ranked Skills")
        st.text_area("Skills", value=tailor_skills, height=200)

        st.subheader("Formatted Output")
        st.text_area("Formatted Output", value=formatted_output, height=300)

if __name__ == "__main__":
    main()
