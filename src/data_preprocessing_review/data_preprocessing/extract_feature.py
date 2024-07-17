import pandas as pd

data = {
    "store": [
        {
        "name": name,
        "review": [
            {
                "metadata_feature":[
                    {
                    "url": url,
                    "post_title": post_title,
                    "date": date,
                    "week": week,
                    "like": count,
                    "tag_count": tag_count,
                    "content_len": content_len
                        }
                    ]
                "textual_feature":{
                    "content": content
                        }
                "reviewer_feature":{
                    "num_post": num_post
                }
                    
                }


            ] 
        }
    ]
}