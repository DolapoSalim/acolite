## def auth
## gets authentication token from USGS EarthExplorer API
## written by Quinten Vanhellemont, RBINS
## 2023-09-19
## modifications: 2023-09-25 (QV) changed to separate earthexplorer credentials
##                2024-04-27 (QV) moved to acolite.api
##                2025-04-03 (QV) use login-token
##                2025-07-09 (QV) update code to get token from ac.shared.auth

def auth(api_url = None, return_auth = False, netrc_machine = 'earthexplorer',
         user = None, token = None):
    import os, requests, json, netrc
    import acolite as ac

    ## get credentials
    auth = ac.shared.auth(netrc_machine)

    if auth is None:
        print_machine = netrc_machine.upper().replace('_TOKEN', '')
        print('Could not determine {} credentials {}_u and {}_token.'.format(print_machine, print_machine, print_machine))
        print('Please add them to your .netrc file, environment variables, or ACOLITE config file.')
        return

    if (len(auth[1]) != 64):
        print('{}_token length is not 64 characters, this is likely wrong.'.format(netrc_machine.upper()))
        print('Retrieving access_token is unlikely to work!')

    ## get api URL from config
    if api_url is None: api_url = ac.config['EARTHEXPLORER_api']

    ## get access token
    data = {"username": auth[0], "token": auth[1]}
    response = requests.post(api_url+'/login-token', data = json.dumps(data))
    access_token = response.json()["data"]

    if return_auth: return(access_token, (auth[0], auth[1], token))

    return(access_token)
