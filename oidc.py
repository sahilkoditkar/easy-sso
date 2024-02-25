
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
import requests

client_id = '83076db3-9a7f-4100-8cfd-70152cdbcde7'
client_secret = 'WrN8Q~5nkHxYfv2XJiEJvQlzWz3R4GDQtU3y5bYl'
client_secret_id = '0049ca7d-6697-485c-9c39-d4446cc2f9c5'   
tenant_id = 'aa2e8356-dcda-41aa-a021-b9da87cfb1c0'

auth_server = "https://login.microsoftonline.com"

def authenticate():
    url_ip = "172.25.189.164:5000"
    endpoint = "debug"
    authorize_url = f'{auth_server}/{tenant_id}/oauth2/authorize'
    scope = "openid"
    response_type = "id_token"
    response_mode = "form_post"
    state = "e598a6yl89"
    nonce = "fh99qovn2r9"
    return f"{authorize_url}?client_id={client_id}&redirect_uri=https%3A%2F%2F{url_ip}%2F{endpoint}&scope={scope}&response_type={response_type}&response_mode={response_mode}&state={state}&nonce={nonce}"

def authorized_response(result):
    # Your OIDC ID token
    jwt_token = result["id_token"]

    # Your OIDC issuer (the identity provider's URL)
    issuer = "https://sts.windows.net/aa2e8356-dcda-41aa-a021-b9da87cfb1c0/"
    # issuer = f"https://{auth_server}/{tenant_id}/v2.0"

    # Your OIDC audience (usually your client ID)
    audience = client_id
    expected_algorithm = "RS256"

    # Construct the Azure AD JWKS URI based on the issuer
    jwks_uri = f"{auth_server}/{tenant_id}/discovery/v2.0/keys"

    try:
        # Retrieve the Azure AD JSON Web Key Set (JWKS)
        jwks_response = requests.get(jwks_uri)
        jwks_response.raise_for_status()
        jwks = jwks_response.json()

        # Get the JSON Web Key (JWK) from the JWKS
        jwt_header = jwt.get_unverified_header(jwt_token)
        key_id = jwt_header.get("kid")

        for key in jwks["keys"]:
            if key["kid"] == key_id:
                # Create a PyJWT RSAAlgorithm instance from the JWK
                rsa_algorithm = jwt.algorithms.RSAAlgorithm.from_jwk(key)

                # Decode the JWT token using the RSAAlgorithm instance
                decoded_token = jwt.decode(
                    jwt_token,
                    algorithms=[expected_algorithm],
                    issuer=issuer,
                    audience=client_id,
                    key=rsa_algorithm,
                    options={"verify_signature": True, "verify_aud": True},
                )

                # Print the decoded JWT
                print(decoded_token)

    except ExpiredSignatureError:
        print("ID token has expired.")
    except DecodeError as e:
        print(f"ID token decoding failed: {e}")
