from __future__ import division

import csv
import collections
import math


class Answer(object):

    _by_team = collections.defaultdict(list)

    def __init__(self, cid, tid, name):
        self.cid = cid
        self.tid = tid
        self.name = name
        type(self)._by_team[tid].append(self)

    @classmethod
    def from_file(cls, fname):
        with open(fname, 'rb') as fp:
            rdr = csv.reader(fp)
            for row in rdr:
                cls(*row)

    @classmethod
    def teams(cls):
        return cls._by_team.keys()


class Challenge(object):

    _all = {}

    def __init__(self, cid, name, points, solves):
        self.cid = cid
        self.name = name
        self.points = int(points)
        self.solves = int(solves)
        type(self)._all[cid] = self

   @classmethod
    def from_file(cls, fname):
        with open(fname, 'rb') as fp:
            rdr = csv.reader(fp)
            for row in rdr:
                cls(*row)


score_algs = [
        ('linear', lambda c: int(1000/c.solves)),
        ('log', lambda c: int(1000/math.log(c.solves+1))),
        ('exp', lambda c: int(1000/math.pow(c.solves, 2))),
        ]


def main():
    Answer.from_file("answers.csv")
    Challenge.from_file("challenges.csv")
    all_teams = []
    for team in Answer.teams():
        name = Answer._by_team[team][0].name
        old_score = 0
        new_scores = [0] * len(score_algs)
        for a in Answer._by_team[team]:
            chall = Challenge._all[a.cid]
            old_score += chall.points
            for i, a in enumerate(score_algs):
                new_scores[i] = score_algs[i][1](chall)
        all_teams.append({
            'name': name,
            'old_score': old_score,
            'new_scores': new_scores,
            'new_ranks': [],
            })
    all_teams.sort(key=lambda x: x['old_score'], reverse=True)
    for i, t in enumerate(all_teams, 1):
        t['old_rank'] = i
    for i in range(len(score_algs)):
        all_teams.sort(key=lambda x: x['new_scores'][i], reverse=True)
        for i, t in enumerate(all_teams, 1):
            t['new_ranks'].append(i)
    with open("results.csv", "wb") as fp:
        wr = csv.writer(fp)
        header = ['name', 'old_score', 'old_rank']
        for a in score_algs:
            header += [a[0] + '_score', a[0] + '_rank']
        wr.writerow(header)
        for t in all_teams:
            values = [t['name'], t['old_score'], t['old_rank']]
            for i in range(len(t['new_scores'])):
                values += [t['new_scores'][i], t['new_ranks'][i]]
            wr.writerow(values)


if __name__ == '__main__':
    main()
