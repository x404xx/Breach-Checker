<div align="center">

<img src="assets/logo.png" width="300" height="auto">

**Breach-Checker** is a tool to check emails and passwords for security breaches. Source: (https://haveibeenpwned.com)

</div>

## **Installation**

**Using** _`poetry`_

```
git clone https://github.com/x404xx/Breach-Checker.git
cd Breach-Checker
poetry shell
poetry install
```

**Using** _`pip`_

```
git clone https://github.com/x404xx/Breach-Checker.git
cd Breach-Checker
virtualenv env
env/scripts/activate
pip install -r requirements.txt
```

## Help

```
usage: python -m bchecker [-h] [-pu PROXY_URL] [-e EMAIL] [-m {1,2}] [-t {1,2}]
                   [-p PASSWORD] [-v] [-f FILENAME]

Email and password checker for leaked data breaches!

options:
  -h, --help            show this help message and exit
  -pu PROXY_URL, --proxy_url PROXY_URL
                        Proxy URL. Example: (http://username:password@host:port or
                        socks5://username:password@host:port)
  -e EMAIL, --email EMAIL
                        Email that should be checked!
  -m {1,2}, --mode {1,2}
                        (1) Email Checker (2) Password Checker
  -t {1,2}, --task_type {1,2}
                        (1) Single Check (2) Mass Check
  -p PASSWORD, --password PASSWORD
                        Password that should be checked!
  -v, --verbose         Get breaches details!
  -f FILENAME, --filename FILENAME
                        List of passwords for mass checking!
```

## Usage

-   _**`Simple execute. Just follow the given steps in the terminal`**_

```python
python -m bchecker
```

-   _**`Check email with the command`**_

```python
python -m bchecker -m 1 -e 'target email'
```

-   _**`Check a single password with the command`**_

```python
python -m bchecker -m 2 -t 1 -p 'target password'
```

-   _**`Check the mass password with the command using a text file`**_

```python
python -m bchecker -m 2 -t 2 -f 'your text filename that contains a password line by line'
```

-   [x] **Proxy**: You can also use a proxy by using the command `-pu socks5://username:password@host:port`

## Example Output

-   **Email check with verbose**: This command `-v` will print information about where the data breaches have been leaked.
    > Verbose mode only supports email checking; it does not support password checking.

```json
{
    "count": 2,
    "email": "johnny.rotten@yahoo.com",
    "breaches": [
        {
            "name": "Collection1",
            "breachDate": "7/01/2019",
            "description": "In January 2019, a large collection of credential stuffing lists (combinations of email addresses and passwords used to hijack accounts on other services) was discovered being distributed on a popular hacking forum. The data contained almost 2.7 billion records including 773 million unique email addresses alongside passwords those addresses had used on other breached services. Full details on the incident and how to search the breached passwords are provided in the blog post The 773
Million Record \"Collection #1\" Data Breach.",
            "compromised": "Email addresses, Passwords"
        },
        {
            "name": "VerificationsIO",
            "breachDate": "25/02/2019",
            "description": "In February 2019, the email address validation service verifications.io suffered a data breach. Discovered by Bob Diachenko and Vinny Troia, the breach was due to the data being stored in a MongoDB instance left publicly facing without a password and resulted in 763 million unique email addresses being exposed. Many records within the data also included additional personal attributes such as names,
phone numbers, IP addresses, dates of birth and genders. No passwords were included in the data. The Verifications.io website went offline during the disclosure process, although an archived copy remains viewable.",
            "compromised": "Dates of birth, Email addresses, Employers, Genders, Geographic locations, IP addresses, Job titles, Names, Phone numbers, Physical addresses"
        }
    ]
}
```

<div align="center">

**Email check without verbose**

<img src="assets/withoutverbose.png" width="600" height="auto">

**Password single check**

<img src="assets/singlepass.png" width="600" height="auto">

**Password with mass check**

<img src="assets/masspass.png" width="600" height="auto">

</div>

## **Legal Disclaimer**

> This was made for educational purposes only, nobody which directly involved in this project is responsible for any damages caused. **_You are responsible for your actions._**
