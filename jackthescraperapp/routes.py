from jackthescraperapp import app
from flask import request, jsonify
import requests
import json
from services import scraper


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return 'tesssssssst !'


@app.route('/scrape', methods=['GET'])
def scrape():
    params = request.json
    return scraper.runScrape(params['url'], params['tags'])
