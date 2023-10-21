import json
from bs4 import BeautifulSoup
import requests
import json


def get_product_name(soup):
    try:
        #Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigableString Object
        title_value = title.string

		# Title as a string value
        title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()
    except AttributeError:
        title_string = ""	
    
    return title_string

def get_image(soup):
    img_div = soup.find(id="imgTagWrapperId")

    imgs_str = img_div.img.get('data-a-dynamic-image')  # a string in Json format

    # convert to a dictionary
    imgs_dict = json.loads(imgs_str)
    #each key in the dictionary is a link of an image, and the value shows the size (print all the dictionay to inspect)
    num_element = 0 
    first_link = list(imgs_dict.keys())[num_element]
    return first_link


# Function to extract Product Price
## FIX PRICE
def get_price(soup):

	try:
		#price = soup.find("span", attrs={'class':'a-price-whole'}).string.strip()
		price=soup.find("span",{"class":"a-price"}).find("span").text

	except AttributeError:
		price = "woahhh"	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = ""	

	return available

def get_catergory(soup):
	try:
		catergory = soup.find("div", attrs={'id':'availability'})
		catergory = catergory.find("span").string.strip()

	except AttributeError:
		catergory = ""	

	return catergory





# if __name__ == '__main__':
# 	HEADERS = ({'User-Agent':
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
#             'Accept-Language': 'en-US, en;q=0.5'})
# 	URL = "https://www.amazon.com/Sony-PlayStation-Pro-1TB-Console-4/dp/B07K14XKZH/"
# 	webpage = requests.get(URL, headers=HEADERS)
# 	soup = BeautifulSoup(webpage.content, "lxml")
# 	print("Product Title =", get_product_name(soup))

if __name__ == '__main__':

	# Headers for request
	HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	            'Accept-Language': 'en-US'})

	# The webpage URL
	URL = "https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers"
	
	# HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	# Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")

	# Fetch links as List of Tag Objects
	links = soup.find_all("a", attrs={'class':'a-link-normal',
								    'tabindex':'-1'})

	# Store the links
	links_list = []

	# Loop for extracting links from Tag Objects
	for link in links:
		links_list.append(link.get('href'))
		#print(link.get('href'))


	# Loop for extracting product details from each link 
	for link in links_list:

		new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

		new_soup = BeautifulSoup(new_webpage.content, "lxml")
		
		# Function calls to display all necessary product information
		print(link)
		print("Product Title =", get_product_name(new_soup))
		print("Product Price =", get_price(new_soup))
		print("Product Rating =", get_rating(new_soup))
		print("Number of Product Reviews =", get_review_count(new_soup))
		print("Availability =", get_availability(new_soup))
		print("Image = ", get_image(new_soup))
		print()
		print()