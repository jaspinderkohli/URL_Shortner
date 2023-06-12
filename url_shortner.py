import string
import random
import supabase
from flask import Flask, redirect, request
from config import SUPABASE_URL, SUPABASE_KEY


app = Flask(__name__)
db = supabase.create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

def save_url_mapping(short_url, long_url):
    response = db.table('urls').insert([{'short_url': short_url, 'long_url': long_url}]).execute()
    if response['error']:
        # Handle the error response
        print("Error:", response['error'])


def get_long_url(short_url):
    response = db.table('urls').select('long_url').eq('short_url', short_url).execute()
    if response['count'] > 0:
        return response.data[0]['long_url']
    return None

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = get_long_url(short_url)
    print('long_url', long_url)
    if long_url:
        return redirect(long_url)
    return "Short URL not found."

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('url')

    if long_url:
        short_url = generate_short_url()
        print('short_url', short_url)
        save_url_mapping(short_url, long_url)
        return f"Short URL: {request.host}/{short_url}"
    return "Invalid URL."

if __name__ == '__main__':
    app.run()
    # shorten_url()
    # redirect_to_long_url('0AXGxS')

