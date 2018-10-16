from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import csv

#GitHub Link
#https://github.com/lksfr/WebScraping/

#opening Chrome
driver = webdriver.Chrome()

#retrieving the website containing the reviews for the iPhone X
driver.get('https://www.amazon.co.uk/Apple-iPhone-64-SIM-Free-Smartphone-Space-Grey/product-reviews/B076GQZRR9/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1')

#setting an index to count page numbers
index = 1

#creating a csv file named reviews_uk to save all review data in
csv_file = open('uk_reviewsactual.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)

#starting a while-loop that ends once Selenium doesnt find a "Next Page" button on the last review page
while True:
	try:
		#printing the page index to verify that the loop is working properly 
		print('scraping page number ' + str(index))

		#increasing the page index by one during every loop iteration
		index += 1

		wait = WebDriverWait(driver, 10)
		wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-hook="review"]')))


		#finding all review boxes, creating a list of these WebElements and finally calculating the length of that list
		number_of_reviews = len(driver.find_elements_by_xpath('//div[@data-hook="review"]'))
	
		#starting a for-loop iterating over the length of the review boxes list
		#finding all reviews and saving them in variable "reviews"
		#opening a "review_dict" dictionary to store results in
		#subscripting the "reviews" list and retrieving the ith review box
		for i in range(number_of_reviews):

			wait = WebDriverWait(driver, 10)

			wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-hook="review"]')))
			reviews = driver.find_elements_by_xpath('//div[@data-hook="review"]')
			review_dict = {}
			review = reviews[i]
	


			#extracting the star rating of review i
			star_rating = review.find_element_by_xpath('.//i[@data-hook="review-star-rating"]/span[1]').get_attribute("textContent")

			#extracting the title of review i
			title = review.find_element_by_xpath('.//a[@data-hook="review-title"]').get_attribute("textContent")

			#extracting the date of review i
			date = review.find_element_by_xpath('.//span[@data-hook="review-date"]').get_attribute("textContent")

			#extracting the username of review i
			username = review.find_element_by_xpath('.//a[@data-hook="review-author"]').get_attribute("textContent")

			#extracting the text of review i
			text = review.find_element_by_xpath('.//span[@data-hook="review-body"]').get_attribute("textContent")

			#extracting whether or not review i is a verified purchase
			try:
				purchase_type = review.find_element_by_xpath('.//span[@data-hook="avp-badge"]').get_attribute("textContent")

			except Exception:
				purchase_type = 'Not Verified Purchase'

			#extracting the number of "helpful" votes, 0 if element does not exist
			try:

				helpful = review.find_element_by_xpath('.//span[@data-hook="helpful-vote-statement"]').get_attribute("textContent")
			except Exception:
				helpful = '0 people found this helpful'

			#saving all retrieved information in the review_dict dictionary
			review_dict['date'] = date
			review_dict['star_rating'] = star_rating
			review_dict['title'] = title
			review_dict['review_text'] = text
			review_dict['user_name'] = username
			review_dict['purchase_type'] = purchase_type
			review_dict['helpful'] = helpful

			#writing all entries of review i into the csv file
			writer.writerow(review_dict.values())

		#identifying and clicking the "Next Page" button once all reviews on one page have been extracted
		next_button = driver.find_element_by_xpath('//li[@class="a-last"]')
		actions = ActionChains(driver)
		actions.move_to_element(next_button).click().perform()

		time.sleep(5)

	#printing the error in case scraping fails
	except Exception as e:
		print(e)
		break