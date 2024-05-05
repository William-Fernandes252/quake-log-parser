from io import StringIO

import pytest

from quake_log_parser.parser import Parser


class TestParser:

    class TestCaseGameFound:
        @pytest.fixture
        def input(self) -> StringIO:
            lines: list[str] = [
                "  0:00 ------------------------------------------------------------",
                r"  0:00 InitGame: sv_floodProtect\1\sv_maxPing\0\sv_minPing\0\sv_maxRate\10000\sv_minRate\0\sv_hostname\Code Miner Server\g_gametype\0\sv_privateClients\2\sv_maxclients\16\sv_allowDownload\0\dmflags\0\fraglimit\20\timelimit\15\g_maxGameClients\0\capturelimit\8\version\ioq3 1.36 linux-x86_64 Apr 12 2009\protocol\68\mapname\q3dm17\gamename\baseq3\g_needpass\0",
                " 20:54 Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT",
                " 21:07 Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT",
                " 22:06 Kill: 2 3 7: Isgalamido killed Mocinha by MOD_ROCKET_SPLASH",
            ]
            output = StringIO()
            for line in lines:
                output.write(line + "\n")
            return StringIO(initial_value=output.getvalue())

        def it_should_parse_the_input_and_store_the_correct_output(
            self, input: StringIO
        ):
            parser = Parser()
            parser.parse(input)
            assert parser.results == [
                {
                    "game": 1,
                    "status": {
                        "total_kills": 3,
                        "players": [
                            {"name": "Isgalamido", "kills": 1},
                            {"name": "Mocinha", "kills": 0},
                        ],
                    },
                }
            ]

    class TestCaseNoGame:
        def it_should_not_store_any_output(self):
            parser = Parser()
            parser.parse(StringIO(initial_value=""))
            assert parser.results == []
