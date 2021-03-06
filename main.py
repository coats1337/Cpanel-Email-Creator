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

    def create_email(self, save: bool, email_domain: str, email: str, password: str, amount: int):
        '''
        https://documentation.cpanel.net/display/DD/UAPI+Functions+-+Email%3A%3Aadd_pop
        '''
        for _ in range(amount):
            data = {
                'email': email,
                'domain': email_domain,
                'password': password,
                'send_welcome_email': 1,
                'quota': 1024 # recommended according to docs
            }
            auth = self.send_auth('user', 'password')
            auth_json = auth.json()['security_token']
            auth_headers = auth.headers
            r = self.session.post(f'{self.domain}{auth_json}/execute/Email/add_pop',
                                  data=data, headers=auth_headers)
            if '"errors":null' in r.text:
                if save:
                    self.save_accounts(f'Created: {email}@{email_domain}:{password}')
                return f'Created: {email}@{email_domain}:{password}'
            else:
                return f'Couldnt create: {email}@{email_domain}:{password} | {r.text}'


if __name__ == '__main__':
    client = CPanelLib('https://example.com:2083')
    created_email = client.create_email(True, 'domain.org', 'testexample123', 'asupersecurepassword_!"$', 5)
    print(created_email)
