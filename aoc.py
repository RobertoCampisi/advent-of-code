import json
import re

save = {'token': '123123', 'data': [{'year':2024, 'solutions':[{'day':1},]},{'year':2023},{'year':2022}]}

#README.md contains gold stars (total count of ans_part1 and ans_part2) 

# json save
# main -> token: string
#      -> date_gen: string (timestamp of time README.md has been generated)
#      -> data:
#           -> year: int
#           -> solutions:
#               -> day: int
#               -> ans_p1: string (stored when puzzle submission is correct)
#               -> ans_p2: string (stored when puzzle submission is correct)
#               -> date_last_submission_part1:
#               -> date_last_submission_part2:

#stored ans_p1 and ans_p2 can be used for comparing for correct answer after correct submission
#cd on last submission. will not be updated after submission has been verified as correct.

def update_README():
    with open('README.md','r') as f:
        current = f.read()
        summary = dict()
        table_rows = ['| Year | Stars | Advent of Code Link |\n','| :--: | :---: | :--: |\n']
        badges = []
        for year_overview in save['data']:
            year = str(year_data['year'])
            star_count = str(0) #year_data['solutions']
            summary[year] = star_count
        for entry in summary:
            badges.append('[![AoC '+y+'](https://img.shields.io/badge/'+y+'-⭐%20'+y+'-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/'+y+')'))
            table_rows.append('| ['+y +']('+y+') | ⭐️'+star_count+' | https://adventofcode.com/'+y+'|\n')
            
        print(badges)

update_README()
