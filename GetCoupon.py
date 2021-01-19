import requests, bs4, os
from termcolor import colored
from colorama import init
from sys import argv

from Core import getCoupon

if __name__ == "__main__":
    if len(argv) > 1:
        course = argv[1]
    else:
        course = input("Enter The course name or URL\n")

    if course.startswith('http'):
        courseName = bs4.BeautifulSoup(requests.get(course).content, "html.parser").title.string[:-8]
    else:
        courseName = course


    couponLinks = getCoupon(courseName)

    ## Print Colored Text ##
    init()

    if any(couponLinks):
        print(colored("\nHere's ur Coupon Links", 'yellow') + "\n")
        for link in couponLinks:
            print(colored(str(link) + '\n', 'cyan'))
    else:
        print(colored("\nNo coupon Founded Make sure u write the right name or Write URL for good search\n", 'red'))

    os.system("pause")
