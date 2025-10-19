# Wichteln - or secret santa

Finds a secret-santa matching (or in German: Wichteln).
Run via (from top-level wichteln directory) `PYTHONPATH=. python secret_santa/main.py` and configure as below.
Ensured to run with python 3.8, incompatible with 3.12.

## Configuration
The program is configured through environment variables:
1. WICHTELN_GROUP_CONFIG_PATH: Path to load the participants from. Looks like this
```
[
  {"name": "Mom", "email": "mom@web-mail.com", "exclusions": ["Kid2"]},
  {"name": "Dad", "email": "dad@mydomain.com", "exclusions":  ["Mom"]},
  {"name": "Kid1", "email": "kiddo1@apple.ai", "exclusions":  ["Dad"]},
  {"name": "Kid2", "email": "kiddo2@apple.ai", "exclusions":  ["Kid1"]}  
]
```
which might result in a match like: Mom -> Dad, Dad -> Kid1, Kid1 -> Kid2, Kid2 -> Mom.
2. WICHTELN_EMAIL_CONFIG_PATH: Path to load the email-configuration from (where the emails to participants will be 
sent from). Looks like this:  
```
{
  "host": "smtp.gmail.com",  # gmail
  "port": 465,  # gmail
  "sender_address": "benkuc.throwaway@gmail.com",
  "sender_password": "...",  # api token of the email account
  "subject": "your secret-santa",
  "message_template": "your secret-santa is: {taker}"
}
```
3. WICHTELN_SAVE_TO: A path to save the matching to (optional). Might be good to keep for next year, e.g. if the 
wichtel-group agrees that participants shall not gift the same person twice in a row, one can look at the saved 
matching next year and set the exclusions correspondingly. 
4. WICHTELN_MATCHING_MAX_ATTEMPTS: The matching is found by randomly constructing one. A single attempt to find a 
matching this way might fail. The maximum number of attempts defaults to 1000 before giving up.
