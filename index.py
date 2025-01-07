from bs4 import BeautifulSoup

urlq = "https://api.stackexchange.com/2.3/questions"
paramsq = {
    'order': 'asc',
    'sort': 'activity',
    'site': 'stackoverflow',
    'filter': 'withbody',
}
response = requests.get(urlq, params=paramsq)
data = response.json()

cleaned_questions = []
questions_id = []
for question in data['items']:
  if question['is_answered']:
    # print(question['is_answered'])
    soup = BeautifulSoup(question['body'], 'html.parser')
    clean_text = question['title'] + '\n' + soup.get_text().strip()
    cleaned_questions.append(clean_text)
    questions_id.append(question['question_id'])
    print(clean_text)
    print('-' * 50)
print(len(questions_id))
