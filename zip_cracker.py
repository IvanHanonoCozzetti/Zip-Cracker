from datetime import timedelta
from time import time
import itertools, string
import zipfile, zlib


def crack_zip(src, min_length=1, max_length=None, chars=string.printable.strip()):
	start = time()
	count = 1
	with zipfile.ZipFile(src, 'r') as zf:
		while True:

			if max_length is not None:
				if min_length == max_length+1:
					input('Scan exceeded max length. Press ENTER to exit...')
					raise SystemExit

			for pwd in itertools.product(chars, repeat=min_length):
				try:
					zf.extractall(pwd=bytes(''.join(pwd), encoding='utf-8'))
					fmt = "\n+{}+\n|{:^88}|\n|{:^88}|\n+{}+"
					return print(fmt.format(f"{'-'*34}_!PASSWORD_CRACKED!_{'-'*34}",
						"[+] Password Cracked!",
						f"Attempts: {count}  |  Password: {''.join(pwd)}  |  "
						f"Elapsed Time: {timedelta(seconds=time()-start)}", '-'*88))
				except (RuntimeError, zlib.error, zipfile.BadZipFile):
					print(f"[{count}] [-] Password Failed: {''.join(pwd)}  |  "
						f"Elapsed Time: {timedelta(seconds=time()-start)}")
					count += 1
			min_length += 1


if __name__ == '__main__':
	crack_zip('Locked.zip', min_length=5, chars=string.ascii_lowercase)
	input('\nPress Enter to exit...')