#!python3.9

#  Trick Surf Data Recap
#
#  Copyright (C) 2025  anominy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Final, Optional, Any, TextIO
from argparse import ArgumentParser, Namespace as ArgumentNamespace
from subprocess import Popen
from requests import Response

import sys
import requests
import os
import shutil


_CURRENT_PATH: Final[str] = os.path.dirname(__file__)
_PARENT_PATH: Final[str] = os.path.join(_CURRENT_PATH, '..')
_LICENSE_PATH: Final[str] = os.path.join(_PARENT_PATH, 'COPYING')
_RECAP_PATH: Final[str] = os.path.join(_PARENT_PATH, 'recap.txt')

_BASE_URL = 'https://raw.githubusercontent.com/anominy/trick-surf-data-dump/'


# noinspection DuplicatedCode
def _get_url_response(url: Optional[str]) -> Optional[Response]:
    if not url:
        return None

    response: Final[Response] = requests.get(url)
    response.raise_for_status()

    if response.status_code == 204:
        return None

    return response


def _get_url_json(url: Optional[str]) -> Optional[Any]:
    response: Final[Response] = _get_url_response(url)
    if response is None:
        return None

    return response.json()


def _get_diff_count(first_url: str, last_url: str) -> int:
    first_json: Final[Optional[Any]] = _get_url_json(first_url)
    last_json: Final[Optional[Any]] = _get_url_json(last_url)

    first_count: int
    if first_json is None:
        first_count = 0
    else:
        first_count = len(first_json)

    last_count: int
    if last_json is None:
        last_count = 0
    else:
        last_count = len(last_json)

    return last_count - first_count


def _get_players_diff(first_hash: str, last_hash: str) -> int:
    return _get_diff_count(
        _BASE_URL + first_hash + '/trick-surf/games/1/players.min.json',
        _BASE_URL + last_hash + '/trick-surf/games/1/players.min.json'
    )


def _get_maps_diff(first_hash: str, last_hash: str) -> int:
    return _get_diff_count(
        _BASE_URL + first_hash + '/trick-surf/maps.min.json',
        _BASE_URL + last_hash + '/trick-surf/maps.min.json'
    )


def _get_servers_diff(first_hash: str, last_hash: str) -> int:
    return _get_diff_count(
        _BASE_URL + first_hash + '/trick-surf/servers.min.json',
        _BASE_URL + last_hash + '/trick-surf/servers.min.json'
    )


def _get_events_diff(first_hash: str, last_hash: str) -> int:
    return _get_diff_count(
        _BASE_URL + first_hash + '/trick-surf/games/1/events.min.json',
        _BASE_URL + last_hash + '/trick-surf/games/1/events.min.json'
    )


def _get_triggers_diff(first_hash: str, last_hash: str, map_id: int) -> int:
    return _get_diff_count(
        _BASE_URL + first_hash + '/trick-surf/maps/' + str(map_id) + '/triggers.min.json',
        _BASE_URL + last_hash + '/trick-surf/maps/' + str(map_id) + '/triggers.min.json'
    )


def _get_teleports_diff(first_hash: str, last_hash: str, map_id: int) -> int:
    return _get_diff_count(
        _BASE_URL + first_hash + '/trick-surf/maps/' + str(map_id) + '/teleports.min.json',
        _BASE_URL + last_hash + '/trick-surf/maps/' + str(map_id) + '/teleports.min.json',
    )


def _get_tricks_diff(first_hash: str, last_hash: str, map_id: int) -> int:
    return _get_diff_count(
        _BASE_URL + first_hash + '/trick-surf/games/1/maps/' + str(map_id) + '/tricks.min.json',
        _BASE_URL + last_hash + '/trick-surf/games/1/maps/' + str(map_id) + '/tricks.min.json'
    )

def _get_rankings_diff(first_hash: str, last_hash: str, map_id: int, item: str) -> int:
    first_rankings_json: Final[Optional[Any]] = _get_url_json(_BASE_URL + first_hash + '/trick-surf/games/1/maps/' + str(map_id) +'/rankings.min.json')['rankings']
    last_rankings_json: Final[Optional[Any]] = _get_url_json(_BASE_URL + last_hash + '/trick-surf/games/1/maps/' + str(map_id) +'/rankings.min.json')['rankings']

    first_count: int = 0
    if first_rankings_json:
        for ranking_json in first_rankings_json:
            first_count += int(ranking_json[item])

    last_count: int = 0
    if last_rankings_json:
        for ranking_json in last_rankings_json:
            last_count += int(ranking_json[item])

    return last_count - first_count


def _get_jumps_diff(first_hash: str, last_hash: str, map_id: int) -> int:
    return _get_rankings_diff(first_hash, last_hash, map_id, 'jumps')


def _get_sprays_diff(first_hash: str, last_hash: str, map_id: int) -> int:
    return _get_rankings_diff(first_hash, last_hash, map_id, 'sprays')


# def _get_records_diff(first_hash: str, last_hash: str, map_id: int) -> int:
#     return _get_rankings_diff(first_hash, last_hash, map_id, 'total_records')
#
#
# def _get_time_records_diff(first_hash: str, last_hash: str, map_id: int) -> int:
#     return _get_rankings_diff(first_hash, last_hash, map_id, 'time_records')
#
#
# def _get_speed_records_diff(first_hash: str, last_hash: str, map_id: int) -> int:
#     return _get_rankings_diff(first_hash, last_hash, map_id, 'speed_records')
#
#
# def _get_completions_diff(first_hash: str, last_hash: str, map_id: int) -> int:
#     return _get_rankings_diff(first_hash, last_hash, map_id, 'completed_tricks')
#
#
# def _get_points_diff(first_hash: str, last_hash: str, map_id: int) -> int:
#     return _get_rankings_diff(first_hash, last_hash, map_id, 'points')


# noinspection PyTypeChecker
def _main() -> None:
    arg_parser: Final[ArgumentParser] = ArgumentParser()

    arg_parser.add_argument(
        '-l',
        '--license',
        help='show the project license and exit',
        dest='is_license_flag',
        action='store_const',
        const=True,
        default=False
    )

    arg_parser.add_argument(
        '--first-hash',
        help='set the first commit hash',
        dest='first_hash',
        action='store',
        required=True
    )

    arg_parser.add_argument(
        '--last-hash',
        help='set the last commit hash',
        dest='last_hash',
        action='store',
        required=True
    )

    args: Final[ArgumentNamespace] = arg_parser.parse_args()

    if args.is_license_flag:
        more_path: Final[Optional[str]] = shutil.which('more')
        if not more_path:
            with open(_LICENSE_PATH, 'r') as file:
                print(file.read())

            return

        more_process: Final[Popen] = Popen([more_path, _LICENSE_PATH])
        more_process.wait()

        return

    first_hash: Final[str] = args.first_hash
    last_hash: Final[str] = args.last_hash

    with open(_RECAP_PATH, 'w') as file:
        players_diff: Final[int] = _get_players_diff(first_hash, last_hash)
        print('Number Of New Players: ' + str(players_diff), file=sys.stdout)
        print('Number Of New Players: ' + str(players_diff), file=file)

        maps_diff: Final[int] = _get_maps_diff(first_hash, last_hash)
        print('Number Of New Maps: ' + str(maps_diff), file=sys.stdout)
        print('Number Of New Maps: ' + str(maps_diff), file=file)

        servers_diff: Final[int] = _get_servers_diff(first_hash, last_hash)
        print('Number Of New Servers: ' + str(servers_diff), file=sys.stdout)
        print('Number Of New Servers: ' + str(servers_diff), file=file)

        events_diff: Final[int] = _get_events_diff(first_hash, last_hash)
        print('Number Of New Events: ' + str(events_diff), file=sys.stdout)
        print('Number Of New Events: ' + str(events_diff), file=file)

        maps_json: Final[Optional[Any]] = _get_url_json(_BASE_URL + last_hash + '/trick-surf/maps.min.json')
        for map_json in maps_json:
            map_id: int = int(map_json['id'])
            map_name: str = str(map_json['name'])

            triggers_diff: int = _get_triggers_diff(first_hash, last_hash, map_id)
            print('\n' + map_name + '\n-- Number Of New Triggers: ' + str(triggers_diff), file=sys.stdout)
            print('\n' + map_name + '\n-- Number Of New Triggers: ' + str(triggers_diff), file=file)

            teleports_diff: int = _get_teleports_diff(first_hash, last_hash, map_id)
            print('-- Number Of New Teleports: ' + str(teleports_diff), file=sys.stdout)
            print('-- Number Of New Teleports: ' + str(teleports_diff), file=file)

            tricks_diff: int = _get_tricks_diff(first_hash, last_hash, map_id)
            print('-- Number Of New Tricks: ' + str(tricks_diff), file=sys.stdout)
            print('-- Number Of New Tricks: ' + str(tricks_diff), file=file)

            jumps_diff: int = _get_jumps_diff(first_hash, last_hash, map_id)
            print('-- Number Of New Jumps: ' + str(jumps_diff), file=sys.stdout)
            print('-- Number Of New Jumps: ' + str(jumps_diff), file=file)

            sprays_diff: int = _get_sprays_diff(first_hash, last_hash, map_id)
            print('-- Number Of New Sprays: ' + str(sprays_diff), file=sys.stdout)
            print('-- Number Of New Sprays: ' + str(sprays_diff), file=file)

            # records_diff: int = _get_records_diff(first_hash, last_hash, map_id)
            # print('-- Number Of New Records: ' + str(records_diff), file=sys.stdout)
            # print('-- Number Of New Records: ' + str(records_diff), file=file)
            #
            # time_records_diff: int = _get_time_records_diff(first_hash, last_hash, map_id)
            # print('-- Number Of New Time Records: ' + str(time_records_diff), file=sys.stdout)
            # print('-- Number Of New Time Records: ' + str(time_records_diff), file=file)
            #
            # speed_records_diff: int = _get_speed_records_diff(first_hash, last_hash, map_id)
            # print('-- Number Of New Speed Records: ' + str(speed_records_diff), file=sys.stdout)
            # print('-- Number Of New Speed Records: ' + str(speed_records_diff), file=file)
            #
            # completions_diff: int = _get_completions_diff(first_hash, last_hash, map_id)
            # print('-- Number Of New Completions: ' + str(completions_diff), file=sys.stdout)
            # print('-- Number Of New Completions: ' + str(completions_diff), file=file)
            #
            # points_diff: int = _get_points_diff(first_hash, last_hash, map_id)
            # print('-- Number Of New Points: ' + str(points_diff), file=sys.stdout)
            # print('-- Number Of New Points: ' + str(points_diff), file=file)


if __name__ == '__main__':
    try:
        _main()
    except KeyboardInterrupt:
        pass
