import requests
import json
import time
from collections import Counter

#  Twitter API
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAP5IuwEAAAAAEEJ52DpeGyTm9S6ZY5K34VxRR3E%3DapIguuueEMaURjXQnB2wBVqJ21MKV3nG8iB5GQbckU48abhVnZ'

def create_url_by_usernames(usernames):
    # get user's ID
    usernames_str = ','.join(usernames)
    return f"https://api.twitter.com/2/users/by?usernames={usernames_str}"

def create_url_by_user_id(user_id):
    # gets the user‘s following
    return f"https://api.twitter.com/2/users/{user_id}/following"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    else:
        # Handle API rate limits
        if int(response.headers['x-rate-limit-remaining']) == 0:
            sleep_time = int(response.headers['x-rate-limit-reset']) - time.time()
            time.sleep(sleep_time)
        else:
            pass
    return response.json()

# gets the user‘s following
def get_user_ids(usernames):
    url = create_url_by_usernames(usernames)
    json_response = connect_to_endpoint(url)
    print("information：")
    print(json.dumps(json_response, indent=4, sort_keys=True))
    user_ids = [user["id"] for user in json_response["data"]]
    return user_ids

# gets the user‘s following
def get_following(user_id):
    url = create_url_by_user_id(user_id)
    json_response = connect_to_endpoint(url)
    print(f"user's {user_id} following：")
    print(json.dumps(json_response, indent=4, sort_keys=True))
    following_ids = [user["id"] for user in json_response["data"]]
    return following_ids

def main(usernames):
    user_ids = get_user_ids(usernames)
    all_following_ids = []
    for user_id in user_ids:
        print(f"get user {user_id} following list")
        following_ids = get_following(user_id)
        all_following_ids.extend(following_ids)

    # Count the number of following
    following_count = Counter(all_following_ids)

    # rank
    ranked_following = following_count.most_common()
    return ranked_following

if __name__ == "__main__":
    usernames = ["afafugai", "SmokeyTheBera"]
    ranked_following_info = main(usernames)
    print("The most frequently followed accounts：")
    for user_id, count in ranked_following_info:
        print(f"user ID: {user_id}, times: {count}")
