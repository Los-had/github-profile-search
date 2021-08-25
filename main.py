from flask import Flask, request, render_template, url_for, redirect
import requests
import json
import os

SECRET_KEY = os.environ['KEY']
print('Online')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
  try:
    return render_template('index.html')
  except:
    return redirect('/error')

@app.route('/user_not_found', methods=['GET'])
def user_not_found():
  return render_template('user_not_found.html')

@app.route('/error', methods=['GET'])
def error():
  return render_template('error.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
  try:
    # search function
    def search_result(username):
      api = requests.get(f'https://api.github.com/users/{username}')
      response = json.loads(api.text)
      repos_link = requests.get(f'https://api.github.com/users/{username}/repos')
      repos_response = json.loads(repos_link.text)
      
      if 'message' in response:
        
        if response['message'] == "API rate limit exceeded for 34.67.63.254. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)":
          
          return 'Wait one hour the limit is 60 request for hour'

        return redirect('/user_not_found')
      
      bio = response['bio'].replace('\r\n', '')
      name = response['name']
      user = response['login']
      followers = response['followers']
      following = response['following']
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
      profile_link = f'https://github.com/{user}'

      # render template with all collected information
      return render_template('search.html', 
        bio = bio, 
        name = name, 
        username = user, 
        followers = followers, 
        following = following, 
        website = site, 
        twitter = twitter_username, 
        location = location, 
        company = company, 
        picture = profile_picture, 
        repos = repos,
        newest_repo = newest_repo,
        link = profile_link
      )

    if request.method == 'POST':
      username = request.form['user']
      # render the search template page
      return search_result(username)
    else:
      # redirect to the error page
      return redirect('/error')
  
  except:
    return redirect('/error')

if __name__ == '__main__':
  # run the app
  app.run(host='0.0.0.0', port=8080, debug=True)