import requests, bs4, os
from termcolor import colored
from colorama import init

from coupon_extractor.Core import getCoupon

def main(argv):
    if len(argv) > 1:
        course = ' '.join(argv[1:])
    else:
        course = input("Enter The course name or URL\n")

    if course.startswith('http'):
        courseName = bs4.BeautifulSoup(requests.get(course).content, "html.parser").title.string[:-8]
    else:
        courseName = course


    coupons = getCoupon(courseName)

    ## Print Colored Text ##
    init()

    if any(coupons):
        print(colored("\nHere's ur Coupon Links", 'yellow') + "\n")
        for item in coupons:
            if item and item[0].startswith('$'):
                if course.startswith('http'):
                    req = requests.models.PreparedRequest()
                    params={'couponCode':item.split()[1]}
                    req.prepare_url(course, params)
                    print(colored(req.url + '\n', 'cyan'))
                else:
                    print(colored(f'Course Coupon:  {item.split()[1]}' + '\n', 'cyan'))
                continue
            print(colored(str(item) + '\n', 'cyan'))
    else:
        print(colored("\nNo coupon Founded Make sure u write the right name or Write URL for good search\n", 'red'))

    os.system("pause")
