import abc
import csv
import json
import os
from typing import Dict, List, Tuple

import requests


class ApiBase(abc.ABC):
    """ The Abstract Base Class on which every Api[Boolmaker] is based on. """

    def _load_competitions(self) -> Dict:
        """ Read .csv from S1M0N38/soccerapi-competitions and create a
        dictioary of available competitions (not supported league are leave empty '')
        e.g. {'england-premier_league': '',
         'england-championship': 'E42294894',
         'germany-bundesliga_2': 'E42422121'}
        """
        competitions = {}
        url = (
            'https://docs.google.com/spreadsheets/d/'
            '1kHFeE1hsiCwzLBNe2gokCOfVDSocc0mcKTF3HEhQ3ec/'
            'export?format=csv&'
            'id=1kHFeE1hsiCwzLBNe2gokCOfVDSocc0mcKTF3HEhQ3ec&'
            'gid=1816911805'
        )
        data = requests.get(url).text.splitlines()
        rows = csv.DictReader(data)
        for row in rows:
            key = f'{row["country"]}-{row["league"]}'
            competitions[key] = row[self.name]
        return competitions

    def _competition(self, country: str, league: str) -> str:
        """ Get standard country and league and return the corresponding
        competition id. Could be something like 'E42294894' (bet365) or
        'england/premier_league' (888sport, unibet)."""

        competition = f'{country}-{league}'
        msg = (
            f'{competition} is not supported for {self.name}. '
            'Check the docs for a list of supported competitions.'
        )
        try:
            competition_id = self.competitions[competition]
        except KeyError:
            raise KeyError(msg)
        if competition_id == '':
            raise KeyError(msg)
        return competition_id

    @abc.abstractmethod
    def odds(self, country: str, league: str, market: str = 'IT') -> Dict:
        """ Get the odds from the country-league competition as a python dict """
        pass


class ApiKambi(ApiBase):
    """ 888sport, unibet and other use the same CDN (eu-offering.kambicdn)
     so the requetsting and parsing process is exaclty the same.
     The only thing that chage is the base_url """

    @staticmethod
    def _full_time_result(data: Dict) -> List:
        """ Parse the raw json requests for full_time_result """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            try:
                full_time_result = {
                    '1': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'X': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                full_time_result = None

            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'full_time_resut': full_time_result,
                }
            )
        return odds

    @staticmethod
    def _both_teams_to_score(data: Dict) -> List:
        """ Parse the raw json requests for both_teams_to_score """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            try:
                both_teams_to_score = {
                    'yes': event['betOffers'][0]['outcomes'][0].get('odds'),
                    'no': event['betOffers'][0]['outcomes'][1].get('odds'),
                }
            except IndexError:
                both_teams_to_score = None
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'both_teams_to_score': both_teams_to_score,
                }
            )
        return odds

    @staticmethod
    def _double_chance(data: Dict) -> List:
        """ Parse the raw json requests for double chance """

        odds = []
        for event in data['events']:
            if event['event']['state'] == 'STARTED':
                continue
            try:
                double_chance = {
                    '1X': event['betOffers'][0]['outcomes'][0].get('odds'),
                    '12': event['betOffers'][0]['outcomes'][1].get('odds'),
                    '2X': event['betOffers'][0]['outcomes'][2].get('odds'),
                }
            except IndexError:
                double_chance = None
            odds.append(
                {
                    'time': event['event']['start'],
                    'home_team': event['event']['homeName'],
                    'away_team': event['event']['awayName'],
                    'double_chance': double_chance,
                }
            )
        return odds

    def _requests(self, competition: str, market: str = 'IT') -> Tuple[Dict]:
        """ Build URL starting from country and league and request data for
            - full_time_result
            - both_teams_to_score
            - double_chance
        """
        s = requests.Session()
        base_params = {'lang': 'en_US', 'market': market}
        url = '/'.join([self.base_url, competition]) + '.json'

        return (
            # full_time_result
            s.get(url, params={**base_params, 'category': 12579}).json(),
            # both_teams_to_score
            s.get(url, params={**base_params, 'category': 11942}).json(),
            # double_chance
            s.get(url, params={**base_params, 'category': 12220}).json(),
        )

    def odds(self, country: str, league: str, market: str = 'IT') -> Dict:
        """ Get odds from country-league competition """

        # get competition id for country-league
        competition = self._competition(country, league)

        # reuquest odds data
        odds = self._requests(competition, market)

        # parse json response
        odds = [
            self._full_time_result(odds[0]),
            self._both_teams_to_score(odds[1]),
            self._double_chance(odds[2]),
        ]
        return [{**i, **j, **k} for i, j, k in zip(*odds)]
