from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch hackathon details for a given company and year
def fetch_hackathons(company_name, year):
    url = f"https://www.hackerearth.com/challenges/?company={company_name}&year={year}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the relevant hackathon details on the page
        hackathons = []
        for hackathon in soup.find_all('div', class_='challenge-card'):
            title = hackathon.find('h3')
            if title:
                title = title.text.strip()
            description = hackathon.find('p')
            if description:
                description = description.text.strip()

            hackathons.append({'title': title, 'description': description})
        
        return hackathons
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['company']
        year = request.form['year']

        hackathons = fetch_hackathons(company_name, year)
        if hackathons:
            return render_template('index.html', hackathons=hackathons, company=company_name, year=year)
        else:
            return render_template('index.html', error="Unable to fetch hackathons. Please try again.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
