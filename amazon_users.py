from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import csv

#opening Chrome
driver = webdriver.Chrome()

#retrieving the website containing the reviews for the iPhone X
driver.get('https://www.amazon.co.uk/Apple-iPhone-64-SIM-Free-Smartphone-Space-Grey/product-reviews/B076GQZRR9/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1')

#setting an index to count page numbers
index = 1

#creating a csv file named user_values to save all review data in
csv_file = open('user_values_uk.csv', 'w', encoding='utf-8')
writer = csv.writer(csv_file)

#starting a while-loop that ends once Selenium doesnt find a "Next Page" button on the last review page
while True:
	try:

		#printing the page index to verify that the loop is working properly 
		print('scraping page number ' + str(index))

		#increasing the page index by one during every loop iteration
		index += 1

		time.sleep(3)



		#finding all review authors, creating a list of these WebElements and finally calculating the length of that list
		number_of_users  = len(driver.find_elements_by_xpath('//a[@data-hook="review-author"]'))


		#starting a for-loop iterating over the length of the review authors list
		#finding all reviews and saving them in variable "user_names"
		#opening a "review_dict" dictionary to store results in
		#subscripting the "user_names" list and retrieving the ith user 
		for i in range(number_of_users):

			user_names = driver.find_elements_by_xpath('//a[@data-hook="review-author"]')

			review_dict = {}
			user = user_names[i]

			#storing the username in the variable user_name
			user_name = user.get_attribute("textContent")

			#clicking on the user name to go to the user's profile
			actions = ActionChains(driver)
			actions.move_to_element(user).click().perform()

			time.sleep(5)

			#finding the total number of "helpful" votes for that user
			try:
				user_helpful_total = driver.find_element_by_xpath('//div[@class="dashboard-desktop-stats-section"]/div[1]/a[1]/div[1]/div[1]/span[1]').get_attribute("textContent")
			except Exception:
				user_helpful_total = '0'
			#dealing with user that have received more than 1000 "helpful" votes
			if 'k' in user_helpful_total:
				user_helpful_total = (float(user_helpful_total[:3]))*1000

			#finding the number of reviews by that user
			try:
				user_num_reviews = driver.find_element_by_xpath('//div[@class="dashboard-desktop-stats-section"]/div[2]/a[1]/div[1]/div[1]/span[1]').get_attribute("textContent")
			except Exception:
				user_num_reviews = '0.001'
			if user_num_reviews == '0':
				user_num_reviews = '0.001' 
			
			#finding the dates on which the user has left a review
			user_review_dates = driver.find_elements_by_xpath('//div[@class="a-row a-spacing-mini profile-at-user-info"]')
			
			time.sleep(5)

			date_ls = []
			#finding each review in user_review_dates and appending it to the date_sl list
			for ureview in user_review_dates:
					
				udates = ureview.find_element_by_xpath('./div[1]/div[2]/span[2]').get_attribute("textContent")
				date_ls.append(udates)


			#finding all review ratings
			user_review_ratings = driver.find_elements_by_xpath('//div[@class="a-section profile-at-content"]')

			rate_ls = []
			headers_ls = []
			text_ls = []

			#extracting the rating, title, and text from each review and appending it to the lists above
			for urating in user_review_ratings:

				uratings = urating.find_element_by_xpath('./div[1]/div[1]/i[1]/span[1]').get_attribute("textContent")
				rate_ls.append(uratings)

				uheaders = urating.find_element_by_xpath('./div[2]/h1[1]/span[1]/span[1]').get_attribute("textContent")
				headers_ls.append(uheaders)

				utexts = urating.find_element_by_xpath('./div[2]/p[1]/span[1]/span[1]').get_attribute("textContent")
				text_ls.append(utexts)



			time.sleep(5)
			

			# Calculate Fake Review Index:
			# Highest possible score on the Fake Review Index: 100
			#
			# Understanding the scale:
			#
			# Score below 10: very unlikely that review is fake
			# Score above 10 and below 20: unlikely that review is fake
			# Score above 20 and below 30: most likely not fake but occassionally might be if fake is hard to identify
			# Score above 30 and below 40: grey area, could be either
			# Score above 40 and below 50: likely fake
			# Score above 50: very likely to be fake
			#
			# Used indicators for calculating the Fake Review Index:
			#
			#			total number of helpful votes: if a user gets less than or equal to one helpful votes
			#                                          it's more likely that the review is not genuine and thus not helpful 
			#										   (max=10): 
			#													user_helpful_total/user_num_reviews <= 1: +10												
			#													user_helpful_total/user_num_reviews > 1 and <=2: +8
			#													user_helpful_total/user_num_reviews > 3 and <=4: +4
			#													user_helpful_total/user_num_reviews > 5 and <=8: +2
			#													user_helpful_total/user_num_reviews > 8: +0
			#
			#	
			#
			#			total number of reviews: if a user leaves very little reviews, then he/she is most likely
			#                                    not an active member of the Amazon review community(max=20):
			#
			#													user_num_reviews = 1: +20
			#													user_num_reviews >1 and <=5: +15
			#													user_num_reviews >5 and <=15: +10
			#													user_num_reviews >15 and <= 30: +7
			#													user_num_reviews >30 and <= 50: +3
			#													user_num_reviews >30 and <= 50: +0								
			#
			#
			#			review dates: if a user leaves several reviews on the same date, these are more likely to be
			#                         fake (max=17.5):
			#
			#										max([date_ls.count(x) for x in date_ls]) > 4: +17.5
			#										max([date_ls.count(x) for x in date_ls]) = 3: +14
			#										max([date_ls.count(x) for x in date_ls]) = 2: +10
			#										max([date_ls.count(x) for x in date_ls]) = 1: +0
			#
			#
			#
			#			ratings: a user is more likely to be fake if he/she only leaves either 5 star or 1 star reviews (max=17.5):
			#
			#									ratings_int = [int(x[0]) for x in rate_ls]
			#									
			#									ratings_int.count(5) or ratings_int.count(1) > 15: +17.5
			#									ratings_int.count(5) or ratings_int.count(1) >=10 and < 15: +12
			#									ratings_int.count(5) or ratings_int.count(1) >5 and <= 10: +7
			#									ratings_int.count(5) or ratings_int.count(1) <5: +3
			#
			#
			#
			#			review titles: a user is more likely to be fake if he/she repeatedly uses the same review title (max=17.5):
			#
			#										max([headers_ls.count(x) for x in headers_ls]) > 4: +17.5
			#										max([headers_ls.count(x) for x in headers_ls]) = 3: +14
			#										max([headers_ls.count(x) for x in headers_ls]) = 2: +10
			#										max([headers_ls.count(x) for x in headers_ls]) = 1: +0
			#
			#
			#			review texts: (max=17.5): a user is more likely to be fake if he/she uses the same review text repeatedly
			#
			#										max([text_ls.count(x) for x in text_ls]) > 4: +17.5
			#										max([text_ls.count(x) for x in text_ls]) = 3: +14
			#										max([text_ls.count(x) for x in text_ls]) = 2: +10
			#										max([text_ls.count(x) for x in text_ls]) = 1: +0
			#
			#
			#
			#
			#										
	

			fake_index = 0


	#helpful votes
		
			if float(user_num_reviews) == 0:
				fake_index += 0

			if float(user_helpful_total)/float(user_num_reviews) <= 1:
				fake_index += 10

			elif float(user_helpful_total)/float(user_num_reviews) > 1 and float(user_helpful_total)/float(user_num_reviews) <=2:
				fake_index += 8

			elif float(user_helpful_total)/float(user_num_reviews) > 3 and float(user_helpful_total)/float(user_num_reviews) <=4:
				fake_index += 4

			elif float(user_helpful_total)/float(user_num_reviews) > 5 and float(user_helpful_total)/float(user_num_reviews) <=8:
				fake_index += 2

			elif float(user_helpful_total)/float(user_num_reviews) > 8:
				fake_index += 0

			

			time.sleep(2)
	#number of reviews
				
			if float(user_num_reviews) == 1:
				fake_index += 20

			elif float(user_num_reviews) >1 and float(user_num_reviews) <=5:
				fake_index += 15


			elif float(user_num_reviews) >5 and float(user_num_reviews) <=15:
				fake_index += 10


			elif float(user_num_reviews) >15 and float(user_num_reviews) <=30:
				fake_index += 7


			elif float(user_num_reviews) >30 and float(user_num_reviews) <=50:
				fake_index += 4


			elif float(user_num_reviews) >50:
				fake_index += 0


	#review dates
			try:
				max_date = max([date_ls.count(x) for x in date_ls])
			except Exception:
				max_date == 0

			if max_date == "":
				max_date == 0

			if max_date >= 4:
				fake_index += 17.5

			elif max_date == 3:
				fake_index +=14

			elif max_date == 2:
				fake_index +=10

			elif max_date <= 1:
				fake_index +=0



	#ratings

			ratings_int = [int(x[0]) for x in rate_ls]

			if (ratings_int.count(5) or ratings_int.count(1)) > 15:
				fake_index += 17.5

			elif (ratings_int.count(5) or ratings_int.count(1)) >=10 and (ratings_int.count(5) or ratings_int.count(1)) < 15:
				fake_index += 12

			elif (ratings_int.count(5) or ratings_int.count(1)) >=5 and (ratings_int.count(5) or ratings_int.count(1)) < 10:
				fake_index += 7

			elif (ratings_int.count(5) or ratings_int.count(1)) < 5:
				fake_index += 3


		

	#review titles

			try:
				review_title = max([headers_ls.count(x) for x in headers_ls])
			except Exception:
				review_title == 0

			if review_title == "":
				review_title == 0

			if review_title >= 4:
				fake_index += 17.5

			elif review_title == 3:
				fake_index += 14

			elif review_title == 2:
				fake_index += 10

			elif review_title == 1:
				fake_index += 0



	#review texts

			try:
				review_texts = max([text_ls.count(x) for x in text_ls])
			except Exception:
				review_texts == 0

			if review_texts == "":
				review_texts == 0


			if review_texts >= 4:
				fake_index += 17.5

			elif review_texts == 3:
				fake_index += 14

			elif review_texts == 2:
				fake_index += 10

			elif review_texts == 1:
				fake_index += 0


			

			#saving results in a dictionary and writing it to a csv		
			review_dict['user_name'] = user_name
			review_dict['fake_review_index'] = fake_index	
			writer.writerow(review_dict.values())
			
			#returning to the "all reviews" website
			driver.execute_script("window.history.go(-1)")
			

			time.sleep(5)

		
		#finding the "Next Page" button and clicking it
		next_button = driver.find_element_by_xpath('//li[@class="a-last"]')
		next_button.click()

		time.sleep(5)

	#print exception if there should be one
	except Exception as e:
		print(e)
		break