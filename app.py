from flask import Flask, redirect, url_for, session, request
import json
import oidc

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/')
def home():
    return 'Home page'

@app.route('/mysso')
def mysso():
    return redirect(oidc.authenticate())

@app.route('/debug', methods=['POST'])
def debug():
    result = request.form
    oidc.authorized_response(result)
    return result

# @app.route('/login')
# def login():
#     return oauth.azure_ad.authorize(callback=url_for('authorized', _external=True))

# @app.route('/logout')
# def logout():
#     session.pop('azure_ad_token', None)
#     return 'Logged out'

# @app.route('/login/authorized')
# def authorized():
#     response = oauth.azure_ad.authorized_response()
#     if response is None or response.get('access_token') is None:
#         return 'Access denied: reason={} error={} error_description={}'.format(
#             request.args['error_reason'],
#             request.args['error'],
#             request.args['error_description']
#         )

#     session['azure_ad_token'] = (response['access_token'], '')
#     me = oauth.azure_ad.get('me')
#     # print(response, type(oauth.azure_ad))
#     return 'Logged in as: {}'.format(me.data.get('displayName'))

# @oauth.azure_ad.tokengetter
# def get_azure_ad_oauth_token():
#     return session.get('azure_ad_token')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", ssl_context='adhoc')
