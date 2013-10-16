from flask_oauth import OAuth

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='http://localhost:5000/',
    consumer_key="529423813793656",
    consumer_secret="e3535cd1ebc8d29b712fc853b670ff9e",
    request_token_params={'scope': 'email'}
)


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('oath_authorized',\
        next=request.args.get('next') or request.referrer or None))
