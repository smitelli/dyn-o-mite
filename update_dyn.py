import mechanize
from bs4 import BeautifulSoup
from prettytable import PrettyTable

DYN_USERNAME = 'FILL ME IN'
DYN_PASSWORD = 'FILL ME IN'
DYN_DOMAIN_NAME = 'FILL.ME.IN'

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36')
]

# ==============================================================================
# === LOG IN ===================================================================
# ==============================================================================

br.open('https://account.dyn.com/entrance/')

login_form = None
for form in br.forms():
    if 'log' in form.find_control(type='submit').attrs['value'].lower():
        form.name = 'yes-good-login'
        break

br.select_form(name='yes-good-login')
br['username'] = DYN_USERNAME
br['password'] = DYN_PASSWORD
br.submit()

# ==============================================================================
# === COMPLETE HOSTNAME FORM ===================================================
# ==============================================================================

br.open('https://account.dyn.com/dns/dyndns/' + DYN_DOMAIN_NAME)

hostname_form = None
for form in br.forms():
    if 'save' in form.find_control(type='submit').attrs['value'].lower():
        form.name = 'yes-good-save'
        break

br.select_form(name='yes-good-save')
result = br.submit()

# ==============================================================================
# === BUILD TABLE OF RESULTS ===================================================
# ==============================================================================

soup = BeautifulSoup(result.read())
rows = soup.find(id='dyndnshostnames').find_all('tr')

table = None
for row in rows:
    if row.parent.name == 'thead':
        continue

    th = [t.text.replace('\n', ' ').strip() for t in row.find_all('th')]
    td = [t.text.replace('\n', ' ').strip() for t in row.find_all('td')]

    if th and not table:
        table = PrettyTable(th)
        table.align = 'l'
        table.padding_width = 2
    elif td:
        table.add_row(td)

print table
