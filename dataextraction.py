import time
import httpx
import pandas as pd

base_url = 'https://www.reddit.com'
endpoint = '/r/fitness30plus/'
category = '/hot'

url = base_url + endpoint + category + ".json"
after_post_id = None
dataset = []

for _ in range(5):
    params = {
        'limit': 100,
        't': 'year', # time
        'after': after_post_id
    }
    response = httpx.get(url, params=params)
    print(f'fetching "{response.url}"...')
    if response.status_code != 200 :
        raise Exception('failed to fetch data')
    
    json_data = response.json()

    dataset.extend([rec['data'] for rec in json_data['data']['children']])

    after_post_id = json_data['data']['after']
    time.sleep(0.5)

df = pd.DataFrame(dataset)
df.to_csv('reddit_python.csv', index=False)
print("done.")