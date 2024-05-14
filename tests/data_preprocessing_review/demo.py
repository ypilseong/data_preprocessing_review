import sys
sys.path.append('/home/chuaie/workspace/projects/review_confirm/src/data_preprocessing_review/crawling')
from get_blog_url import get_blog_url
from blog_scraping import extract_naverBlog
from ocr import ocr



import pandas as pd


def main(path, start):

    df = pd.read_csv(path, sep=',', encoding='utf-8')
    df = df[start:]
    store_data = df['new_store_name'].tolist()

    df_blog = pd.DataFrame(columns=['store_name', 'blog_url', 'result', 'word'])
    blog_count = 0
    store_count = 0
    for i in store_data:
        store_count += 1
        try:
            df_blog_url = get_blog_url(i)
            for k in range(len(df_blog_url)):
                if ((df_blog_url['date'][k] > pd.to_datetime('2020-01-01', format='%Y-%m-%d')) and
                    (df_blog_url['date'][k] < pd.to_datetime('2021-12-31', format='%Y-%m-%d'))):
                    try:
                        blog_count += 1
                        post_dir_name = extract_naverBlog(df_blog_url['blog_url'][k], i)
                        false_review_word = ocr(post_dir_name)
                        if false_review_word is not None:
                            
                            df_blog = df_blog.append({'store_name': i, 'blog_url': k, 'result': 'False', 'word': false_review_word}, ignore_index=True)
                        else:
                            df_blog = df_blog.append({'store_name': i, 'blog_url': k, 'result': 'True', 'word': 'None'}, ignore_index=True)
                    except:
                        blog_count += 1
                        print(f'skip blog Number {blog_count}')
                        continue
        except:
            print(f'Skip store Number {store_count}: {i}')
            continue

    df_blog.to_csv('/home/chuaie/workspace/projects/review_confirm/data/blog_crawling_data.csv', index=False)


if __name__ =='__main__':
    start = int(180)
    main('/home/chuaie/workspace/projects/review_confirm/data/unique_store_data.csv', start)
