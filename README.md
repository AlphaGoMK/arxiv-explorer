# Arxiv Explorer
**Search papers by key words at [arxiv.org](https://arxiv.org/list/cs.CV/recent)**. A more efficient way to browse recent arxiv papers.  
### Requirements
| Name | Version |  
| --- | --- |
| python | 3.6 |
| requests | 2.23.0 |
| beautifulsoup | 4.8.2 |

### Useages
```
search.py [-h] [-D DATE] [-K KEY_WORDS] [--find_abs]

optional arguments:
  -h, --help            show this help message and exit
  -D DATE, --date DATE  date range splitted by comma
  -K KEY_WORDS, --key_words KEY_WORDS
                        searching keys
  --find_abs            search in abstract
```
**Be aware**: It will search titles and comments by default, and you could add `--find_abs` argument if you want to further explore abstracts.
    
For example: 
`python search.py -D 1,2,3 -K detection,CVPR`  
Search for papers of past 1,2,3 days, which contains 'detection' **and** 'CVPR' (*Case insensitive*), quotation marks needed if keyword contains white space.  
It will output depend on date you search:
```
[1]: https://arxiv.org/abs/2003.00981
    Plug & Play Convolutional Regression Tracker for Video Object Detection

[2]: https://arxiv.org/abs/2003.00888
    3D Object Detection From LiDAR Data Using Distance Depended Feature Extraction
```

### FAQ
1. Get `ConnectionResetError: [Errno 54] Connection reset by peer` error  
  A: Run command again.