# Web Scraping Amazon Reviews

## Introduction

As a self-proclaimed tech-enthusiast, I've been following the tech review community, especially on YouTube, for quite a while. During that time, I recognized a certain pattern emerge after every new iPhone release: highly popular videos (as well as articles) would be released criticizing initial problems with the new iPhone.

However, Apple's sales numbers do not seem to be impacted by this negative atmosphere around its release date. This made me wonder who is most impacted by these videos and articles and whether or not they affect Apple's customer satisfaction. Should these reviews, in fact, impact Apple's customers, a more loosely defined release schedule, giving Apple more time to refine new features of the iPhone, might increase Apple's customer satisfaction.

## Why amazon.co.uk?

I chose to scrape amazon.co.uk for several reasons. Firstly, Europe, besides China, is arguably the most important foreign market for the iPhone. Thus, customer reviews from the UK present relevant information for Apple. Secondly, Amazon enabled me to not only gather information regarding the reviews themselves (Rating, Title, Text, Helpful Votes) but also regarding the Amazon user that published the review. By clicking on the username, I was able to collect information about each user, such as the total number of helpful votes and reviews as well as all published reviews.

In conducting my research, I chose to exclusively focus on reviews for the iPhone X from November 2017 to September 2018 to only gather reviews for the newest iPhone at that point in time. Future research could apply the same concept to older iPhones.

## Work Flow

I used Selenium to scrape amazon.co.uk, mainly because of its flexibility in navigating between different websites.

After having scraped the data, I prepared and cleaned the data, mostly using Pandas, NumPy, and RE. This step included identifying and appropriately dealing with missing values, adapting my code, and reformatting the gathered data to enable further processing and analysis.

Then, I manipulated and analyzed the data, breaking it down into subgroups and comparing their characteristics.

Finally, I visualized the results of my analysis with matplotlib, seaborn, and wordcloud.

#### Link to full blog post: https://nycdatascience.com/blog/student-works/does-apples-fixed-iphone-release-schedule-hurt-its-customer-satisfaction/
