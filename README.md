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
Edit your database credentials in `app.py` at line 19

run `gunicorn app:app`
Alternatively, you can un-comment the last line of `app.py` and run `python app.py`.

