from flask import Flask, request, render_template, url_for, redirect
import requests
import json
import os

SECRET_KEY = os.environ['KEY']
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/error', methods=['GET'])
def error():
  return render_template('error.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
  # search function
  def search_result(username):
    api = requests.get(f'https://api.github.com/users/{username}')
    response = json.loads(api.text)
    repos_link = requests.get(f'https://api.github.com/users/{username}/repos')
    repos_response = json.loads(repos_link.text)
    
    if 'message' in response:
      return render_template('user_not_found.html')
    
    bio = response['bio'].replace('\r\n', '')
    name = response['name']
    user = response['login']
    followers = response['followers']
    follwoing = response['following']
    site = response['blog']
    
    email = response['email']
    if email == None:
      email = "Don't have a public email"
    
    hireable = response['hireable']
    if hireable == None:
      hireable = 'Not hireable'
    
    twitter_username = response['twitter_username']
    location = response['location']
    company = response['company']
    profile_picture = response['avatar_url']
    repos = response['public_repos']
    newest_repo = repos_response[0]['full_name']

    # render template with all collected information
    return render_template('search.html', 
      bio = bio, 
      name = name, 
      username = user, 
      followers = followers, 
      follwoing = follwoing, 
      website = site, 
      twitter = twitter_username, 
      location = location, 
      company = company, 
      picture = profile_picture, 
      repos = repos,
      newest_repo = newest_repo
    )

  if request.method == 'POST':
    username = request.form['user']
    # render the search template page
    return search_result(username)
  else:
    # redirect to the error page
    return redirect('error')

if __name__ == '__main__':
  # run the app
  app.run(host='0.0.0.0', port=8080, debug=True)