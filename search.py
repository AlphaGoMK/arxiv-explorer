import requests
from bs4 import BeautifulSoup
import argparse


def get_split_ids(soup):
    content = soup.body.find_all(id='content')[0].find(id='dlpage')
    date_list = content.find_all('ul')[0]  # ul
    split_ids = []  # start idx of each day
    for item in date_list.find_all('li'):
        href = item.a['href']
        split_ids.append(int(href[href.find('?skip=')+6:href.find('&show=')]))
    last_page_str = content.find_all('small')[0].find_all('a')[-1].contents[0]
    if last_page_str.find('-') == -1:
        split_ids.append(int(last_page_str))
    else:
        split_ids.append(int(last_page_str.split('-')[-1]))
    return split_ids


def find_paper_info(soup, key_words, find_abs=False):
    res = {}
    content = soup.body.find(id='dlpage')
    dt_list = content.find_all('dt')
    print('Start searching...')
    for idx, item in enumerate(dt_list):
        paper_id = item.find(title='Abstract')['href'].split('/')[-1]
        dd = item.find_next_siblings('dd')[0]
        # contents[0]='\n'
        title = dd.find(class_='list-title mathjax').contents[2]
        # paper may not contain comment
        mathjax = dd.find(class_='list-comments mathjax')
        if not mathjax is None:
            comment = mathjax.contents[2]
        else:
            comment = ''
        # find in abs, need more time.
        if find_abs:
            new_soup = BeautifulSoup(requests.get(
                'https://arxiv.org/abs/'+paper_id).text, 'lxml')
            abstract = new_soup.find(class_='abstract mathjax').contents[1]
        else:
            abstract = ''

        flag = True
        for k in key_words:  # every key word should exists in this paper
            if not k in title.lower() + abstract.lower() + comment.lower():
                flag = False
        if flag:
            res[paper_id] = ['https://arxiv.org/abs/' +
                             paper_id, title, abstract, comment]
            print('[%d]: https://arxiv.org/abs/%s\n   %s' %
                  (len(res), paper_id, title))
    print('Search finished')
    return res  # {paper_id: [paper_url, title, abs, comment]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--date', type=str,
                        default='1,2,3,4,5', help='date range splitted by comma')
    parser.add_argument('-K', '--key_words', type=str,
                        default='Detection,cvpr', help='searching keys')
    parser.add_argument('--find_abs', action='store_true',
                        help='search in abstract')
    arg = parser.parse_args()
    # get start and end id of each day
    soup = BeautifulSoup(requests.get(
        'https://arxiv.org/list/cs.CV/recent').text, 'lxml')    # only recent papers
    split_ids = get_split_ids(soup)
    res_dict = {}
    query_dates = [int(x) for x in arg.date.split(',')]
    query_keys = [x for x in arg.key_words.split(',')]
    extra = []
    for item in query_keys:  # convert all to lower case
        extra.append(item.lower())
    query_keys = extra
    query_keys = list(set(query_keys))    # remove duplicate

    for date in query_dates:
        url = 'https://arxiv.org/list/cs.CV/pastweek?skip=%d&show=%d' % (
            split_ids[date-1], split_ids[date]-split_ids[date-1])
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        tmp_dict = find_paper_info(soup, query_keys, arg.find_abs)
        res_dict = {**res_dict, **tmp_dict}
    with open('result%s.txt' % '_'.join(query_keys), 'w+') as f:
        for idx, paper_id in enumerate(res_dict.keys()):
            f.write('%d: %s\n' % (idx+1, res_dict[paper_id][0]))
            f.write('    %s\n' % res_dict[paper_id][1])
