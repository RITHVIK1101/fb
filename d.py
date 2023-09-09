import logging
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Define a function to scrape player information from the website
def scrape_player_info():
    try:
        website_url = "https://www.wolvesfootball.com/roster/varsity"
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        player_infos = soup.find_all('li', class_='list-item')

        player_data = []

        for player_info in player_infos:
            player_name = player_info.find('h2', class_='list-item-content__title').text.strip()
            details = player_info.find('p', class_='').text.strip().split('|')
            grade = details[0].strip()
            position = details[1].strip()
            height = details[2].strip()
            weight = details[3].strip()

            player_data.append({
                "Player Name": player_name,
                "Grade": grade,
                "Position": position,
                "Height": height,
                "Weight": weight
            })

        return player_data

    except Exception as e:
        return str(e)

@app.route('/get_player_info', methods=['GET'])
def get_player_info():
    try:
        player_name = request.args.get('player_name').upper()  # Extract and normalize player name
        player_data = scrape_player_info()

        # Find player information in the scraped data
        found_players = [player for player in player_data if player_name in player['Player Name'].upper()]

        if found_players:
            # Take the first found player (you can modify this logic if needed)
            player_info = found_players[0]

            # Construct a response
            response_text = (
                f"{player_info['Player Name']} is in grade {player_info['Grade']}, "
                f"plays as {player_info['Position']}, has a height of {player_info['Height']}, "
                f"and a weight of {player_info['Weight']}."
            )
        else:
            response_text = "Player not found."

        return jsonify({
            "fulfillmentText": response_text
        })

    except Exception as e:
        return jsonify({
            "fulfillmentText": f"An error occurred: {str(e)}"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
