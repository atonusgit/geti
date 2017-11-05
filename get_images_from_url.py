#!/usr/bin/python

"""
Get Images from URL

This script downloads images from
provided URL and saves them in a
folder next to the script file.

It also saves image URLs as a
list in a text file.

Author: Anton Valle
"""

import os, sys, requests, urllib
from bs4 import BeautifulSoup
try: from urlparse import urljoin # Python2
except ImportError: from urllib.parse import urljoin # Python3

def get_images_from_url(url_address):

	source_code = get_source_code(url_address)

	for image_tag in source_code.find_all('img'):

		image_src = get_image_src(image_tag)
		root_folder = os.path.dirname(os.path.realpath(__file__))
		images_folder_name = "/images/"

		create_folder(root_folder, images_folder_name)

		# fetch image
		urllib.urlretrieve(urljoin(url_address, image_src), root_folder + images_folder_name + os.path.split(image_src)[1])

		# list URL to file
		write_file(root_folder + "/image_urls.txt", urljoin(url_address, image_src))


def get_source_code(url_address):

	r = requests.get(url_address)
	return BeautifulSoup(r.text, "lxml")


def get_image_src(image_tag):

	image_src = image_tag.get("src")
	image_src = remove_image_adjusters(image_src)
	return image_src


def remove_image_adjusters(image_src):

	question_mark = image_src.find("?")
	if question_mark > 0:
		image_src = image_src[:question_mark]
	return image_src


def create_folder(root_folder, images_folder_name):

	if not os.path.exists(root_folder + images_folder_name):
		os.makedirs(root_folder + images_folder_name)


def write_file(filename, destination):

	f = open(filename,"a+")
	f.write(destination + "\n")
	f.close()


def main():

	try:

		print "Crawling images from " + sys.argv[1]
		get_images_from_url(sys.argv[1])

	except IndexError:

		print "WELCOME to use " + os.path.basename(__file__)
		print "\nPlease pass URL into the script."
		print "\nExample:\npython " + os.path.basename(__file__) + " http://www.antonvalle.fi/page.php\n"
		return

	except:

		print "Unexpected error:", sys.exc_info()[0]
		return

	print "\nSUCCESS\n"
	print "Images downloaded to " + os.path.dirname(os.path.realpath(__file__)) + "/images/"
	print "Image URLs listed in " + os.path.dirname(os.path.realpath(__file__)) + "/image_urls.txt\n"


if __name__ == "__main__":
	main()