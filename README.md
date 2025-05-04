# Groover.co Feedbacks Scraping
## Introduction
This project scrapes data about feedback and feedback writers from the Groover.co music website.<br>
There are three scripts included that extract data about feedback and feedback writers for your music.

# Getting Started
<b>1.Clone the repository:</b>

```bash
git clone https://github.com/AslanEmil008/Groover.co-Feedbacks-Scraping.git
cd linkedin-data-scraper
```

<b>2.Then install the requirements:</b>

```bash
pip install -r requirements.txt
```
## How to Run
To run this project, follow the step-by-step instructions provided in the <br>
<b>[Project Documentation for Song Feedback and Genre Extraction Process (PDF)](https://github.com/AslanEmil008/Groover.co-Feedbacks-Scraping/blob/main/Project%20Documentation%20for%20Song%20Feedback%20and%20Genre%20Extraction%20Process.pdf)</b>
<br>
After making the necessary changes in the `update_feedbacks.py` file (as described in the documentation), run:
```bash
python3 update_feedbacks.py
```
After making the necessary changes in the `LinksProfiles.py` file, run:

```bash
python3 LinksProfiles.py
```

After making the necessary changes in the `Run Genres.py` file, run:
```bash
python3 Run Genres.py
```
## What data will you get?
After running the `update_feedbacks.py` script, you will get data such as:

- Feedback content
- Feedback giver's name
- Song name (to distinguish each song's feedback)
- Feedback type (e.g., 'Promise to share' marked as Success, 'Feedback in red' marked as Fail)

After running `LinksProfiles.py`, you will get the following data:

- Feedback writers' names
- Profile URLs

After running `Genres.py`, you will get:

- Genres associated with the feedback writers











