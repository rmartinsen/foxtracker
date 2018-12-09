import boto3

from nba_client import NBAClient
from config import pub_arn


class GameNotOverError(Exception):
    pass


def publish(game_summary):
    client = boto3.client('sns', region_name='us-west-2')
    client.publish(TopicArn=pub_arn, Message=game_summary, Subject='Game Over')



def main(anchor_date=None):

    # client = NBAClient(anchor_date)
    client = NBAClient('20181121')

    game_data = client.get_todays_scores('SAC')[0]
    game_id = game_data['gameId']

    boxscore = client.get_boxscore(game_id)

    if not game_data['nugget']:
        raise GameNotOverError

    player_stats = client.get_player_from_boxscore(boxscore, 1628368)

    to_print_data = {
        'h_team': game_data['hTeam']['triCode'],
        'h_score':  game_data['hTeam']['score'],
        'v_team': game_data['vTeam']['triCode'],
        'v_score': game_data['vTeam']['score'],
        'nugget': game_data['nugget']['text'],
        'fox_stats': player_stats
    }

    summary = '''

    {h_team} {h_score} - {v_team} {v_score}
    {nugget}
    De'Aaron Fox: {fox_stats}

    '''.format(**to_print_data)

    publish(summary)

    return summary

if __name__ == '__main__':
    main('20181208')
