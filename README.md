# E-Commerce-Image-And-Review-Scrape

Two simple web scraping scripts:
1. For scraping product images from Cosmetify, Amazon, Sephora, ColourPop, Elf, Maybelline, Bing, Ulta, Temptalia.
2. For scraping product reviews from Sephora, Ulta, Amazon.

How to Use?

This is a console-based app. For both scripts, the necessary input is the product URL. For image scraping, app will identify the product images on the URL, download images to your local file, and create/update a .csv file including image name, url, date, product name, etc. For review scraping, app will identify the product reviews on the URL, and create/update a .csv file inluding comment, comment title, username, rating, product name, etc.

An example CSV file after scarping product reviews:
![review-scrape](https://user-images.githubusercontent.com/86730766/171702680-5d036330-0e5c-42a3-9ddd-2f58b59c2f3e.png)
(This can be extremely useful if used with NLP.)
