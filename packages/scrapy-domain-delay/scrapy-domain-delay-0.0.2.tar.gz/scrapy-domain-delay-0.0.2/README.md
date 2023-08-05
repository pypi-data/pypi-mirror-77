# Scrapy-Domain-Delay

[![Build Status](https://travis-ci.com/ChiaYinChen/scrapy-domain-delay.svg?branch=master)](https://travis-ci.com/ChiaYinChen/scrapy-domain-delay)

## Install
```
$ pip install scrapy-domain-delay
```

## Usage

Step 1: Extract only the domain name from a url using Python tldextract.

```
>>> import tldextract
>>> tldextract.extract('https://www.google.com/').domain
'google'
```

Step 2: Use the following config values in your scrapy settings:

1. Enable the AutoThrottle extension.

	```
	AUTOTHROTTLE_ENABLED = True
	```

2. Enable the Custom Delay Throttle by adding it to `EXTENSIONS`.

	```
	EXTENSIONS = {
	    'scrapy.extensions.throttle.AutoThrottle': None,
	    'scrapy_domain_delay.extensions.CustomDelayThrottle': 300,
	}
	```

3. Add `{'domain': 'download delay (in seconds)'}` to the `DOMAIN_DELAYS`.

	something like:

	```
	# set up custom delays per domain
	DOMAIN_DELAYS = {
	    'google': 1.0,
	}
	```
