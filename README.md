# Club-rush-fortune-teller-app

Made for use during Club Rush, September 3rd, 2025. A basic fortune telling app that users Cloudflare's AI Worker API to answer a question about someones fortune.

## How it was made

A lot of the styling was done using Claude 3.5 Sonnet via Copilot as this needed to be done in as little time as possible. All logic in the main loop was coded by me. Some of the logic in the styling functions was either done by me or edited to not be broken/work the way I intended vs. the AI "implementation".

## Utilization

Requires a Cloudflare AI Worker API key and BASEURL in a .env file.
Vars:
APIKEY
BASE_URL

Required Libraries:

requests
dotenv
os
random
colorama
time
re