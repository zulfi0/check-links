# check-links
Simple multithreading python script for checking live links while doing bug bounty.
It's only examined the link that has the status code other than 404

Usage :
-
```python
python3 checks.py -f files.txt -t [threads number] -o outputfile.txt
```
or
- 
```python
python3 checks.py -f files.txt -t [threads number] | tee save.txt
```
Installation :
-
```bash
git clone https://github.com/zulfi0/check-links.git
```
