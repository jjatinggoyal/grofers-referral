# grofers-referral

## Live build

You can access a live build of the web-app at [grofers.onrender.com](https://grofers.onrender.com)

(Use referral code `jatin` at signup for ₹100 Grofers Cash (^-^))

## Files

### static

contains .css elements

### templates

contains html templates for the web-app

### app.py

backend in flask

### data_dump.sql

initialize database on PostgreSQL

### requirements.txt

contains library requirements

## Local Deployment

Install the required libraries using -
```typescript
pip install -r requirements.txt
```

Create a PostgreSQL database and run data_dump.sql to create required tables.
Edit your database credentials in `app.py` at line 13

run `gunicorn app:app`
Alternatively, you can un-comment the last line of `app.py` and run `python app.py`.

![Home Page]<img src="/images/1.png" width="720" height="480">
![Signup Page](/images/2.png)
![Signup Success Page](/images/3.png)
![Dashboard 0](/images/4.png)
![Generate Refer Code](/images/5.png)
![Dashboard 1](/images/6.png)
![Referral History](/images/7.png)
![Referral Milestones](/images/8.png)
![Withdraw Referral](/images/9.png)
![Dashboard 0](/images/10.png)