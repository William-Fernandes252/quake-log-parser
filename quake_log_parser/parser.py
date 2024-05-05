import re
from io import StringIO
from typing import TypedDict


class Player(TypedDict):
    name: str
    kills: int


class Status(TypedDict):
    total_kills: int
    players: list[Player]


class Entry(TypedDict):
    game: int
    status: Status


class Parser:
    _results: list[Entry]
    _games_count: int
    _players_per_game: list[set[str]]

    def __init__(self):
        self._games_count = -1
        self._players_per_game = []
        self._results = []

    def parse(self, input: StringIO):
        """Parse a log file.

        Args:
            path (str): The path to the log file.
        """
        while line := input.readline():
            self._parse_line(line)

    def _parse_line(self, line: str) -> bool:
        """Parse a log line.

        Args:
            line (str): The log line

        Returns:
            bool: `True` if the line passed is valid and was successfully processed,
            `False` otherwise.
        """
        if len(re.findall(r"InitGame:", line)) > 0:
            self._games_count += 1
            self._results.append(
                {
                    "game": self._games_count + 1,
                    "status": {"total_kills": 0, "players": []},
                }
            )
            self._players_per_game.append(set())
            return True
        if match := re.match(
            r"\s\d{2}:\d{2}\s+Kill:\s+[\d\s]+:\s+([\w<>]+)\s+killed\s+([\w\s]+)\sby",
            line,
        ):
            self._results[self._games_count]["status"]["total_kills"] += 1

            killer, killed = match.groups()
            if killer != "<world>":
                if killer not in self._players_per_game[self._games_count]:
                    self._players_per_game[self._games_count].add(killer)
                    self._results[self._games_count]["status"]["players"].append(
                        {"name": killer, "kills": 1}
                    )
                else:
                    for player in self._results[self._games_count]["status"]["players"]:
                        if player["name"] == killer:
                            player["kills"] += 1
            if killed not in self._players_per_game[self._games_count]:
                self._players_per_game[self._games_count].add(killed)
                self._results[self._games_count]["status"]["players"].append(
                    {"name": killed, "kills": 0}
                )
            if killer == "<world>":
                for player in self._results[self._games_count]["status"]["players"]:
                    if player["name"] == killed and player["kills"] > 0:
                        player["kills"] -= 1
        return False

    @property
    def results(self) -> list[Entry]:
        return self._results
