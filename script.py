import requests
import subprocess
import logging
import random
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def send_email(recipient_email, subject, content):
    """Send the generated blog content via email."""
    try:
        sender_email = "edwardlorilla2013@gmail.com"
        sender_password = "giax bwty esxw dquw"

        # Set up the MIME message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject.replace("\n", " ").strip()

        # Attach the blog content
        message.attach(MIMEText(content, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"Error sending email: {e}")






def generate_content(prompt):
    """Generate content using the Ollama model."""
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Error generating content: {result.stderr.strip()}")
    return result.stdout.strip()

def fetch_stackoverflow_questions(tag="python"):
    """Fetch questions tagged with a specific tag from Stack Overflow."""
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "activity",
        "tagged": tag,
        "site": "stackoverflow",
        "filter": "withbody"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch questions: {response.status_code}")
    
    data = response.json()
    if not data.get("items"):
        raise Exception("No questions found.")
    
    return data["items"]

def clean_question_data(questions):
    """Clean and format question data for easier readability."""
    cleaned_questions = []
    for question in questions:
        if question['is_answered']:
            soup = BeautifulSoup(question['body'], 'html.parser')
            clean_text = f"Title: {question['title']}\n\nBody:\n{soup.get_text().strip()}"
            cleaned_questions.append({
                "id": question['question_id'],
                "title": question['title'],
                "body": soup.get_text().strip(),
                "link": question['link'],
                "cleaned_text": clean_text
            })
    return cleaned_questions

def main():
    try:
        # Fetch and clean Stack Overflow questions
        questions = fetch_stackoverflow_questions(tag="python")
        cleaned_questions = clean_question_data(questions)

        if not cleaned_questions:
            logger.info("No answered questions found.")
            return

        # Select a random cleaned question
        selected_question = random.choice(cleaned_questions)
        logger.info(f"Selected Question: {selected_question['title']} (ID: {selected_question['id']})")

        # Prepare the prompt
        prompt = f"Generate a response to the following Stack Overflow question:\n\n{selected_question['cleaned_text']}"
        
        # Generate content using Ollama
        response_content = generate_content(prompt)
        recipients = [
            "edwardlance.lorilla.edwardlancelorilla@blogger.com",
        ]
        for recipient in recipients:
            send_email(
                recipient_email=recipient,
                subject=selected_question['title'],
                content=response_content
            )
        
        time.sleep(10)  # Respect API rate limits
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
