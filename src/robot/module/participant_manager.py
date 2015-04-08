# -*- coding:utf8 -*-
__author__ = 'changyuf'

from robot.utility.db_manager import DBManager
from robot.utility.utilities import to_str
from robot.bean.participant import Participant


class ParticipantManager:
    def __init__(self):
        self.db_manager = DBManager()

    def get_participants(self, activity_id):
        sql = """SELECT activity_id, card, qq, type, gender, add_on_female, add_on_male, cost
                FROM participants
                WHERE activity_id = %d""" % activity_id

        rows = self.db_manager.fetchall(sql)
        participants = []
        for row in rows:
            participant = Participant()
            participant.activity_id = row[0]
            participant.card = to_str(row[1])
            participant.qq = to_str(row[2])
            participant.type = to_str(row[3])
            participant.gender = to_str(row[4])
            participant.add_on_female = row[5]
            participant.add_on_male = row[6]
            participant.cost = row[7]
            participants.append(participant)

        return participants

    def get_participant(self, activity_id, qq):
        sql = """SELECT activity_id, card, qq, type, gender, add_on_female, add_on_male, cost
                FROM participants
                WHERE activity_id = %d AND qq = "%s" """ % (activity_id, qq)

        rows = self.db_manager.fetchall(sql)
        if not rows:
            return None
        if len(rows) < 1:
            return None

        row = rows[0]
        participant = Participant()
        participant.activity_id = row[0]
        participant.card = to_str(row[1])
        participant.qq = to_str(row[2])
        participant.type = to_str(row[3])
        participant.gender = to_str(row[4])
        participant.add_on_female = row[5]
        participant.add_on_male = row[6]
        participant.cost = row[7]

        return participant

    def insert_participant(self, participant):
        sql = """INSERT INTO participants
                (activity_id, card, qq, type, gender, add_on_female, add_on_male, cost)
            VALUES
                ("{p.activity_id}", "{p.card}", "{p.qq}", "{p.type}", "{p.gender}",
                {p.add_on_female}, {p.add_on_male}, {p.cost});""".format(p=participant)

        return self.db_manager.execute(sql)

    def delete_participant(self, activity_id, qq):
        sql = "DELETE FROM participants WHERE activity_id = %d and qq = '%s'" % (activity_id, qq)
        return self.db_manager.execute(sql)

    def get_participant_message(self, activity_id, max_participants):
        participants = self.get_participants(activity_id)
        msg = "人数限制：%d/%d\\n" % (len(participants), max_participants)
        msg += "已报名人员：\\n"
        for participant in participants:
            msg += "【%s】 %s(%s)" % (participant.type, participant.card, participant.gender)
            if participant.add_on_male > 0:
                msg += " +%d男" % participant.add_on_male
            if participant.add_on_female > 0:
                msg += " +%d女" % participant.add_on_female
            msg += "\\n"

        return msg


