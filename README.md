# grofers-referral

## Live build

You can access a live build of the web-app at [grofers.onrender.com](https://grofers.onrender.com)

(Use referral code `jatin` at signup for ₹100 Grofers Cash (^-^))

Note: the web-app may take upto 30 seconds to load on the first visit.

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

## Functionalities

Go to [tour.md](tour.md) for a step by step visit of the web-app.

### Signup with/without Referral code

Username and password must be atleast 3 characters long.

### Generate and share Referral Code

Shows Users Referral Code, which they can share to earn incentives.

Also users' dashboard now shows metrics such as Referral History and Referral Milestones

### Get your Referral History

Shows users Referral History

### Get Referral Milestones

Shows Referral Milestones achieved and remaining.

### Withdraw from Referral Program

User's referral code becomes invalid and their dashboard rolls back to only showing the option to join back referral program.

However, no referral history for the user is deleted. It is accessible again when they re-register for the referral program.

### Miscellaneous

App uses GET and POST requests in Flask to serve requests.

The login'ed user is not remembered, so going to home page (i.e. `grofers.onrender.com`) is equivalent to logging out.

Use the `Dashboard` button to go navigate to your dashboard. 

Using browsers `back` and `forward` should be avoided. However, they will work fine for most cases.

## Working

The app uses Flask and PostgreSQL.

Database consists of two tables - `users` and `referrals`, which store information about users and all referrals respectively.

Data is updated for both the referrer and referred user on signup. Users' refer_status is also updated as and when they register or withdraw from the referral program.

You can visit [grofers.onrender.com/admin](https://grofers.onrender.com/admin) to see all the registered users.