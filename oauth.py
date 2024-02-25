from flask_oauthlib.client import OAuth

client_id = '83076db3-9a7f-4100-8cfd-70152cdbcde7'
client_secret = 'WrN8Q~5nkHxYfv2XJiEJvQlzWz3R4GDQtU3y5bYl'
client_secret_id = '0049ca7d-6697-485c-9c39-d4446cc2f9c5'   
tenant_id = 'aa2e8356-dcda-41aa-a021-b9da87cfb1c0'

# Configure OAuth for Azure AD
oauth = OAuth()
azure_ad = oauth.remote_app(
    'azure_ad',
    consumer_key=client_id,
    consumer_secret=client_secret,
    request_token_params={'scope': 'openid profile'},
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/token',
    authorize_url=f'https://login.microsoftonline.com/{tenant_id}/oauth2/authorize'
)
