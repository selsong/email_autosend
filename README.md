# email_autosend
NAMI ACS Connections email autosend with Google Spreadsheets
Description: Automated email reply system that adds custom zoom link based on which groups the respondent has selected. It keeps track of which form respondents have already received an email through Google Spreadsheets. Developed in Summer 2023 for NAMI connections support groups.

Step 1: Copy your google account generated passcode
Youtube Video: https://www.youtube.com/watch?v=g_j6ILT-X0k

Step 2: Download credentials.json
https://developers.google.com/sheets/api/quickstart/python
Create project
Enable API
Add user
Create certificate and download the file credentials.json
Move it into the same folder/directory 

Step 3: Download github code onto the same folder as the other files:
https://github.com/2023SS/email_autosend

Edit the following identifiers:
email_receiver
Password (from Step 2)
* Only if the spreadsheet for form responses changes (Sheet ID, Sheet / Tab Name). The email sender must also be the owner of the spreadsheet. If you change the spreadsheet, you have to delete the file “tokens.json” from your folder since the code auto generates a tokens.json file.

Step 4: Run the code:
Open Terminal

Step 5: (Under development) Create CronJob

Sends every minute
<pre><code>
$ crontab -e 
* * * * * cd /Users/selinasong/Downloads/nami; python3 check_send.py
</code></pre>

Send every day at 23:15pm 
<pre><code>
$ crontab -e 
15 23 * * * cd /Users/selinasong/Downloads/nami; python3 check_send.py
</code></pre>
https://www.geeksforgeeks.org/crontab-in-linux-with-examples/
https://www.cloudways.com/blog/wordpress-cron-job/
Computer must be on at the time per day

