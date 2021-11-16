from threading import Thread, Lock
import requests
import random
import queue
import sys

'''
Simple script that check for live links and save it to output
'''

#try to support pipe tee (| tee )
sys.stdout.reconfigure(line_buffering=True)

#define variables
q =  queue.Queue()
status = ''
out = []
out_lock = Lock()
user_agent = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240', 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko']
picker = random.choice(user_agent)
header = {'User-Agent' : ''+picker+''}

def check_links() :
	global q

	while not q.empty():
		link = q.get()

		try :
			response = requests.get(link, headers=header)
			status = response.status_code
		except Exception as e:
			print(e)
			sys.exit(1)

		if status != 404 :
			#append live links in list
			with out_lock :
				out.append(link)

			#print the output
			print(f"[{status}] {link}")

		#done checking
		q.task_done()

if __name__ == '__main__' :
	import argparse
	parser = argparse.ArgumentParser(epilog='written by zulfi0',allow_abbrev=False, description='Checks for live links in a file from link finder tools')
	parser.add_argument('-f', '--file',required=True, metavar='file', help='file containing list of links to check')
	parser.add_argument('-t', '--threads',required=False, metavar='number', help='number of threads default 30', default=30)
	parser.add_argument('-o', '--output',required=False, metavar='file', help='save output to given name and format')

	args = parser.parse_args()

	if args.threads is not None :
		n_threads = int(args.threads)
	
	#read the wordlists
	try :
		links = open(args.file).read().strip().split('\n')
	except :
		print('Error while opening files or files is not found')
		sys.exit(1)

	#from here we begin the check links
	print('-----------------------------')
	print(f'links to check : {len(links)}')
	print(f'threads : {n_threads}')
	print(f'User Agent : {picker}')
	print('-----------------------------')
	print('starting to check...')

	for link in links :
		q.put(link)

	for i in range(n_threads):
		try :
			t = Thread(target=check_links)
			t.daemon = True
			t.start()
		except Exception as e :
			print(e)
			sys.exit(1)
	try :
		q.join()
	except KeyboardInterrupt  :
			print('\nKeyboard interrupt received, exiting.')
			sys.exit(1)

	# save the list into a file when finish
	if args.output :
		save =  open(args.output, 'w')
		for link in out :
			save.write('%s\n' % link)