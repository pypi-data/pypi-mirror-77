# PyLol #

A Module to reduce imports

## Status ##

Current Verison: 1.0.1
Author: BXRCODES
License: MIT License

### Description ###

Python has so many packages to offer, but perhaps a bit too many. Are your imports looking messy? Well PyLol is the solution for all of that. Simply put a couple of imports rather than 100 and still get the same results!

#### Usage ####

Use PyLol for many things like Async Development and Opening Files, manipulate JSON Files, Do Maths and many more

##### License #####

MIT License
See LICENSE for more details

###### Patch Notes ######

# New: #
Random Class was Added to the Package

## INITIAL RELEASE ##

All new functions in define state:
# ALL THE FUNCTIONS WILL HAVE THE SAME NAMES AS THEIR PROPER MODULES SO WHEN USING THEM, YOU DON'T NEED TO LEARN ANY NEW SYNTAX #


# Update 1.0.11 #
Fixed Bugs for Random Functions!

# Update 1.0.1 #

1. Added os (not all of it was complete as there was so many functions but will be completed in future updates, see below for OS Functions) functions
2. Split each class into different files
3. Import Statements are now like --> from Pylol.fileName import functionNames
4. Fixed issues with random functions giving errors

### OS FUNCS SO FAR ###

def ctermid():
	os.ctermid()

def environ():
	os.environ()

def environb():
	os.environb()

def chdir(path):
	os.chdir(path)

def fchdir(fd):
	os.fchdir(fd)

def getcwd():
	os.getcwd()

def fsencode(filename):
	os.fsencode(filename)

def fsdecode(filename):
	os.fsdecode(filename)

def fspath(path):
	os.fspath(path)

def __fspath__():
	os.__fspath__()

def getenv(key, default=None):
	os.getenv(key, default)

def getenvb(key, default=None):
	os.getenvb(key, default)

def get_exec_path(env=None):
	os.get_exec_path(env)

def getegid():
	os.getegid()

def geteuid():
	os.geteuid()

def getgrouplist(user,group):
	os.getgrouplist(user,group)

def getgroups():
	os.getgroups()

def getlogin():
	os.getlogin()

def getpgid(pid):
	os.getpgid(pid)

def getpgrp():
	os.getpgrp()

def getppid():
	os.getppid()

def getpriority(which,who):
	os.getpriority(which, who)

def getreusid():
	os.getresuid()

def getresgid():
	os.getresgid()

def getuid():
	os.getuid()

def initgroups(username,gid):
	os.initgroups(username,gid)

def putenv(key,value):
	os.putenv(key,value)

def setegid(egid):
	os.setegid(egid)

def seteuid(euid):
	os.seteuid(euid)

def setgid(gid):
	os.setegid(gid)

def setgroups(groups):
	os.setgroups(groups)

def setpgrp():
	os.setpgrp()

def setpgid(pid,pgrp):
	os.setpgid(pid, pgrp)

def setpriority(which,who,priority):
	os.setpriority(which,who,priority)

def setregid(rgid,egid):
	os.setregid(rgid,egid)

def setresgid(rgid,egid,sgid):
	os.setresgid(rgid, egid, sgid)

def setresuid(ruid,euid,suid):
	os.setresuid(ruid, euid, suid)

def setreuid(ruid,euid):
	os.setreuid(ruid, euid)


Previous Update

Random Functions!

	seed(a=None, version=2)

	getstate()

	setstate(state)

	getrandbits(k)

	randrange(start, stop)

	randint(a, b)

	choice(seq)

	choices(population, weights=None, *, cum_weights=None, k=1)

	shuffle(x)

	sample(population, k)

	random()

	uniform(a,b)

	triangular(low, high, mode)

	betavariate(alpha, beta)

	expovariate(lambd)

	gammavariate(alpha, beta)

	gauss(mu, sigma)

	lognormvariate(mu, sigma)

	normalvariate(mu, sigma)

	vonmisesvariate(mu, kappa)

	paretovariate(alpha)

	weibullvariate(alpha, beta)
