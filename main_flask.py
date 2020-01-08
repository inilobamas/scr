from flask import Flask, render_template, request, Response, send_file, send_from_directory
import main_twitter, os, tweepy, main_instagram

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("main_flask.html")

@app.route("/authenticate_twitter", methods=['POST'])
def authenticate_twitter():
    consumer_key = request.json.get("key")
    consumer_secret = request.json.get("secret")
    access_token = request.json.get("token")
    access_token_secret = request.json.get("token_secret")

    # Authentication Data
    consumer_key = consumer_key
    consumer_secret = consumer_secret
    access_token = access_token
    access_token_secret = access_token_secret

    # Authorize
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        redirect_url = auth.get_authorization_url()
        return "Authorize Twitter Success"
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
        return "Authorize Twitter Failed"


@app.route("/generate_twitter", methods=['POST'])
def generate_twitter():
    consumer_key = request.json.get("key")
    consumer_secret = request.json.get("secret")
    access_token = request.json.get("access_token")
    access_token_secret = request.json.get("access_token_secret")

    hashtag = request.json.get("hashtag")
    since = request.json.get("since")
    until = request.json.get("until")
    maxtweets = request.json.get("maxtweets")
    outputFileName = main_twitter.main(consumer_key, consumer_secret, access_token, access_token_secret, hashtag, since, until, maxtweets)

    with open(os.getcwd() + "/" + outputFileName) as fp:
        csv = fp.read()
        return Response(
                csv,
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename=" + outputFileName})

@app.route("/authenticate_instagram", methods=['POST'])
def authenticate_instagram():
    # Authentication Data
    username = request.json.get("username")
    password = request.json.get("password")

    # Authorize
    auth = main_instagram.login(username, password)
    if auth == "Login gagal":
        return "Authorize Instagram Failed"
    else:
        return "Authorize Instagram Success"

@app.route("/generate_instagram", methods=['POST'])
def generate_instagram():
    username = request.json.get("username")
    password = request.json.get("password")

    hashtag = request.json.get("hashtag")
    maxposts = request.json.get("maxposts")
    outputFileName = main_instagram.main(username, password, hashtag, int(maxposts))

    with open(os.getcwd() + "/" + outputFileName) as fp:
        csv = fp.read()
        return Response(
                csv,
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename=" + outputFileName})

if __name__ == "__main__":
    app.run(debug=True)