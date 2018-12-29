import boto3

from nba_client import NBAClient
from config import pub_arn


class GameNotOverError(Exception):
    pass


def publish(game_summary):
    client = boto3.client('sns', region_name='us-west-2')
    client.publish(TopicArn=pub_arn, Message=game_summary, Subject='Game Over')


def get_player_from_boxscore(self, boxscore, player_id=1628368):
    template = '{points}/{totReb}/{assists}/{blocks}/{steals} 3p:{tpm}/{tpa} to:{turnovers}' \
               ' min: {min}'

    raw_player = [x for x in boxscore if x['personId'] == str(player_id)][0]
    return template.format(**raw_player)

def create_summary(game_data, boxscore, players=[]):

    player_data = get_player_from_boxscore(boxscore)

    to_print_data = {
        'h_team': game_data['hTeam']['triCode'],
        'h_score': game_data['hTeam']['score'],
        'v_team': game_data['vTeam']['triCode'],
        'v_score': game_data['vTeam']['score'],
        'nugget': game_data['nugget']['text'],
        'fox_stats': player_data
    }

    summary = '''

        {h_team} {h_score} - {v_team} {v_score}
        {nugget}
        De'Aaron Fox: {fox_stats}

        '''.format(**to_print_data)


def main(anchor_date=None):

    client = NBAClient(anchor_date)
    # client = NBAClient('20181121')

    game_data = client.get_todays_scores('SAC')[0]
    game_id = game_data['gameId']

    boxscore = client.get_boxscore(game_id)
    player_stats = client.get_player_from_boxscore(boxscore, 1628368)

    if not game_data['nugget']:
        quit()



    publish(summary)

    return summary

if __name__ == '__main__':
    main('20181208')
