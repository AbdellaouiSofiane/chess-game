import unittest
from tinydb.table import Table
from models import Tournament, Player, Match, Round


class BaseModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db_table = Tournament._table()

    def setUp(self):
        self.tournament = Tournament(name="some name").save()

    def tearDown(self):
        self.db_table.truncate()

    def test_db_table_gets_correct_name_from_model(self):
        self.assertIsInstance(self.db_table, Table)
        self.assertEqual(self.db_table.name, 'tournament')

    def test_saving_model_to_database(self):
        self.assertEqual(len(self.db_table), 1)
        self.assertEqual(
            self.db_table.get(doc_id=self.tournament.id),
            {
             'name': 'some name',
             'nb_rounds': 4,
             'players': [],
             'rounds': []
            }
        )

    def test_update_model_in_database(self):
        self.tournament.name = 'other name'
        self.tournament.save()
        self.assertEqual(len(Tournament._table()), 1)
        self.assertEqual(
            self.db_table.get(doc_id=self.tournament.id),
            {
             'name': 'other name',
             'nb_rounds': 4,
             'players': [],
             'rounds': []
            }
        )

    def test_dict(self):
        self.assertEqual(
            self.tournament.dict,
            {
             'name': 'some name',
             'nb_rounds': 4,
             'players': [],
             'rounds': []
            }
        )

    def test_retreive_object_from_database(self):
        self.assertEqual(
            Tournament.get(self.tournament.id),
            self.tournament
        )

    def test_retrieve_all_objects_from_database(self):
        tournament_two = Tournament(name="other name").save()
        self.assertEqual(
            Tournament.all(),
            [self.tournament, tournament_two]
        )


class MatchModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.db_table = Player._table()

    def setUp(self):
        self.player_a = Player(
            first_name="Chuck", last_name="Nourris", sexe="M", rank=100
        )
        self.player_b = Player(
            first_name="Harry", last_name="Potter", sexe="M", rank=120
        )
        self.player_a.save()
        self.player_b.save()

    def tearDown(self):
        self.db_table.truncate()

    def test_representation_match_not_finished(self):
        match = Match(self.player_a.id, self.player_b.id)
        self.assertFalse(match.is_finished)
        self.assertEqual(str(match), "Chuck Nourris VS Harry Potter")

    def test_representation_match_finished(self):
        match = Match(self.player_a.id, self.player_b.id)
        match.score_player_1 = 1
        self.assertTrue(match.is_finished)
        self.assertEqual(str(match), "Chuck Nourris:1 VS Harry Potter:0")

    def test_representation_match_finished_with_draw(self):
        match = Match(self.player_a.id, self.player_b.id)
        match.score_player_1 = 0.5
        match.score_player_2 = 0.5
        self.assertTrue(match.is_finished)
        self.assertEqual(str(match), "Chuck Nourris:0.5 VS Harry Potter:0.5")

    def test_set_score_with_winner(self):
        match = Match(self.player_a.id, self.player_b.id)
        match.set_score(winner=self.player_a)
        self.assertEqual(match.score_player_1, 1)
        self.assertEqual(match.score_player_2, 0)
        self.assertEqual(match.get_score(self.player_a), 1)
        self.assertEqual(match.get_score(self.player_b), 0)

    def test_set_score_draw(self):
        match = Match(self.player_a.id, self.player_b.id)
        match.set_score()
        self.assertEqual(match.score_player_1, 0.5)
        self.assertEqual(match.score_player_2, 0.5)
        self.assertEqual(match.get_score(self.player_a), 0.5)
        self.assertEqual(match.get_score(self.player_b), 0.5)


class RoundModelTest(MatchModelTest):

        def setUp(self):
            super().setUp()
            self.player_c = Player(
                first_name="Gerald", last_name="Rivia", sexe="M", rank=150
            )
            self.player_d = Player(
                first_name="Luffy", last_name="Monkey D", sexe="M", rank=300
            )
            self.player_c.save()
            self.player_d.save()

            self.first_match = Match(self.player_d.id, self.player_b.id)
            self.second_match = Match(self.player_c.id, self.player_a.id)

        def tearDown(self):
            super().tearDown()

        def test_round_representation(self):
            round = Round(index=1, matchs=[])
            self.assertEqual(str(round), "Round 1")

        def test_round_is_finished_with_empty_match_list(self):
            round = Round(index=1, matchs=[])
            self.assertFalse(round.is_finished)

        def test_round_is_finished_with_one_match_not_finished(self):
            round = Round(index=1, matchs=[self.first_match, self.second_match])
            self.first_match.score_player_1 = 1
            self.assertFalse(round.is_finished)

        def test_round_is_finished_with_all_matchs_finished(self):
            round = Round(index=1, matchs=[self.first_match, self.second_match])
            self.first_match.score_player_1 = 1
            self.second_match.score_player_2 = 1
            self.assertTrue(round.is_finished)


class TournamentModelTest(RoundModelTest):

    @classmethod
    def setUpClass(self):
        self.db_table_tournament = Tournament._table()
        self.db_table_players = Player._table()

    def setUp(self):
        super().setUp()
        self.first_round = Round(
            index=1,
            matchs=[self.first_match, self.second_match]
        )
        self.final_match = Match(self.player_d, self.player_a)
        self.second_round = Round(
            index=2,
            matchs=[self.final_match]
        )
        self.tournament = Tournament(
            name='test_tournament', nb_rounds=2)

    def tearDown(self):
        self.db_table_tournament.truncate()
        self.db_table_players.truncate()

    def test_representation(self):
        self.assertEqual(str(self.tournament), "test_tournament")

    def test_tournament_not_finished_with_empty_rounds(self):
        self.assertFalse(self.tournament.is_finished)

    def test_tournament_not_finished_with_missing_rounds(self):
        self.tournament.rounds.append(self.first_round)
        self.first_match.score_player_1 = 1
        self.second_match.score_player_2 = 1
        self.assertFalse(self.tournament.is_finished)

    def test_tournament_finished(self):
        self.tournament.rounds.append(self.first_round)
        self.first_match.score_player_1 = 1
        self.second_match.score_player_2 = 1
        self.tournament.rounds.append(self.second_round)
        self.final_match.score_player_1 = 1
        self.assertTrue(self.tournament.is_finished)

    def test_enroll_player(self):
        self.tournament.enroll_player(self.player_a)
        self.assertIn(self.player_a.id, self.tournament.players)

    def test_tournament_is_ready(self):
        self.tournament.enroll_player(self.player_a)
        self.assertFalse(self.tournament.ready)
        self.tournament.enroll_player(self.player_b)
        self.assertFalse(self.tournament.ready)
        self.tournament.enroll_player(self.player_c)
        self.assertFalse(self.tournament.ready)
        self.tournament.enroll_player(self.player_d)
        self.assertTrue(self.tournament.ready)

    def test_generate_next_round_with_no_enrolled_player(self):
        self.tournament.generate_next_round()
        self.assertEqual(len(self.tournament.rounds), 0)

    def test_generate_next_round(self):

        self.tournament.enroll_player(self.player_a)
        self.tournament.enroll_player(self.player_b)
        self.tournament.enroll_player(self.player_c)
        self.tournament.enroll_player(self.player_d)

        self.tournament.generate_next_round()
        self.assertEqual(len(self.tournament.rounds), 1)
        self.assertIn(
            Match(self.player_b.id, self.player_d.id),
            self.tournament.rounds[0].matchs
        )
        self.assertIn(
            Match(self.player_a.id, self.player_c.id),
            self.tournament.rounds[0].matchs
        )

        self.tournament.rounds[0].matchs[0].score_player_1 = 1
        self.tournament.rounds[0].matchs[1].score_player_2 = 1
        self.tournament.generate_next_round()

        self.assertEqual(len(self.tournament.rounds), 2)
        self.assertIn(
            Match(self.player_a.id, self.player_d.id),
            self.tournament.rounds[1].matchs
        )
        self.assertIn(
            Match(self.player_b.id, self.player_c.id),
            self.tournament.rounds[1].matchs
        )
        self.tournament.generate_next_round()


if __name__ == '__main__':
    unittest.main()
