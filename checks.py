import urllib3
import threading
import queue
import argparse
import random
import sys

user_agent = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240', 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko']
agent = random.choice(user_agent)

sys.stdout.reconfigure(line_buffering=True)

def create_wordlist(wordlist):
    resume = False
    words = queue.Queue()

    try:
        with open(wordlist) as fp:
            raw = fp.readline()
            while raw:
                word = raw.strip()
                words.put(word)
                raw = fp.readline()
        fp.close()
    except FileNotFoundError:
        print('Wordlist File Not Found')

    return words

def check_links(qued_word, npool):

    while not qued_word.empty():
        link = qued_word.get()
        
        try:
            http = urllib3.PoolManager(timeout=0.5, num_pools=npool)
            headers = {'User-Agent':agent}
            response = http.request('GET', url=link,headers=headers)
            status = response.status
            print('[{}] {}'.format(status, link))
        except (urllib3.exceptions.ConnectTimeoutError,urllib3.exceptions.MaxRetryError):
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(epilog='by zulfi0',allow_abbrev=False, description='Checks for live links in a file from link finder tools')
    parser.add_argument('-f', '--file',required=True, metavar='file', help='file containing list of links to check')
    parser.add_argument('-t', '--threads',required=False, metavar='number', help='number of threads default 30', default=15)
    parser.add_argument('-o', '--output',required=False, metavar='file', help='save output to given name and format')

    args = parser.parse_args()
    
    if args.threads is not None:
        threads = int(args.threads)

    print('-----------------------------')
    print('threads : {}'.format(threads))
    print('User Agent : {}'.format(agent))
    print('-----------------------------')

    cw = create_wordlist(args.file)

    for i in range(threads):
        t = threading.Thread(target=check_links, args=(cw,int(args.threads),))
        t.start()
