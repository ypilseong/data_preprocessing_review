from data_preprocessing_review.crawling.get_blog_url import get_blog_url
from data_preprocessing_review.crawling.blog_scraping import extract_naverBlog
from data_preprocessing_review.crawling.ocr import ocr
from argparse import ArgumentParser

import pandas as pd


def main(args):

    df = pd.read_csv(args.path, header=None)
    store_data = df['new_sotre_name']

    false_review = []
    for i in store_data:
        blog_url_list = get_blog_url(i)
        for k in blog_url_list:
            post_dir_name = extract_naverBlog(k, store_data)
            false_review_word = ocr(post_dir_name)
            if false_review_word is not None:
                false_review.append(k)




if __name__ =='__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--path',
        type= str,
        default= None,
        help='csv file path of store data inculding addres and name'
    )

    args = parser.parse_args()

    if args.path:
        assert args.path is not None, 'Please enter the file path'
