import requests


def get_livros():
  res = requests.get('http://127.0.0.1:8000/api/livros/')
  return res.json()