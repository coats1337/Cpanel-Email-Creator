import requests

class CPanelLib:
    def __init__(self, domain: str):
        self.session = requests.Session()
        self.domain = domain

    def send_auth(self, user, password):
        r = self.session.post(f'{self.domain}login/?login_only=1',
                              data={'user': user, 'pass': password, 'goto_uri': '/'})
        return r

    @staticmethod
    def save_accounts(content: str):
        with open('accounts.txt', 'a+') as f:
            f.write(content)

    def create_email(self, email_domain, email, password):
        data = {
            'email': email,
            'domain': email_domain,
            'password': password,
            'send_welcome_email': 1,
            'quota': 1024
        }
        auth = self.send_auth('user', 'password')
        auth_json = auth.json()['security_token']
        auth_headers = auth.headers
        r = self.session.post(f'{self.domain}{auth_json}/execute/Email/add_pop',
                              data=data, headers=auth_headers)
        if '"errors":null' in r.text:
            return f'{email}@surfnimpact.org:{password}'
        else:
            return f'Couldnt create: {email}@surfnimpact.org:{password}'


if __name__ == '__main__':
    client = CPanelLib('https://example.com:2083/')
    client.create_email('domain.org', 'testexample123', 'asupersecurepassword_!"$')
