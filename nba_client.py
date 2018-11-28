from datetime import datetime
import requests

endpoints = {
    'endpoints': 'http://data.nba.net/10s/prod/v1/today.json',
    'scoreboard': 'http://data.nba.net/10s/prod/v2/{}/scoreboard.json',
    'teams': 'http://data.nba.net/10s/prod/v2/2018/teams.json',
    'boxscore': 'http://data.nba.net/10s/prod/v1/{}/{}_boxscore.json'
}


class NBAClient():
    def __init__(self, anchor_date=None):
        self.anchor_date = anchor_date or self._get_anchor_date()
        self.teams = self._get_teams()

    def _get_anchor_date(self):
        return '20181121'
        return datetime.today().strftime('%Y%m%d')

    def _get_teams(self):
        team_response = self._get_from_url('teams', response_keys=['league', 'standard'])
        teams = {team['tricode']: team['teamId'] for team in team_response}
        return teams

    def get_todays_scores(self, team=None):
        scoreboard = self._get_from_url('scoreboard', url_formatters=[self.anchor_date],
                                        response_keys=['games'])

        if team:
            team_id = self.teams[team]
            scoreboard = list(filter(lambda x: x['hTeam']['teamId'] == team_id
                                             or x['vTeam']['teamId'] == team_id,
                                     scoreboard))
        return scoreboard

    def _get_boxscore(self, game_id):
        boxscore = self._get_from_url('boxscore', url_formatters=[self.anchor_date, game_id],
                                      response_keys=['stats', 'activePlayers'])
        return boxscore


    def get_player_data(self, player_id):

        1628368

    @staticmethod
    def _get_from_url(endpoint, url_formatters=[], response_keys=[]):
        url = endpoints[endpoint].format(*url_formatters)

        response = requests.get(url).json()
        for key in response_keys:
            response = response[key]
        return response




