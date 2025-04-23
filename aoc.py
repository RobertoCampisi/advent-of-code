import json
import re
import cmd
import os

#puzzle and solution states are stored in a JSON file

save = {'token': '123123', 'data': [{'year':2024, 'solutions':[{'day':1}]},{'year':2023, 'solutions':[]},{'year':2022, 'solutions':[]}]}

class aocCLI(cmd.Cmd):
    prompt = '>>'
    intro = 'Advent of Code command line interface. Type "help" for available commands.'
    
    def do_create(self, arg):
        """
        Add entry to the JSON file.
        Create directory and python file(s) for the defined days according to template if needed.
        DOES NOT OVERWRITE EXISTING FILES
        """
        try:
            create(*parse(arg))
        except Exception as e:
            print('Failed to create data entry due to: 'e) 
        
    def do_fetch(self, arg):
        """
        Fetch puzzle input from advent of code.
        """
        print("WIP!")
    
    def do_test(self, arg):
        """Test puzzle on added examples and compare the outputs to the expected results"""
        print("WIP!")
        
    def do_execute(self, arg):
        """Execute a puzzle solution on the input and print the output."""
        print("WIP!")
        
    def do_submit(self, arg):
        """
        Submits the output of given puzzle solution to the advent of code website.
        If the answer is correct, it will store the result for the future.
        """
        print("WIP!")
    
    def do_benchmark(self, arg):
        """
        Benchmark the time it takes to execute the given puzzle solution(s). 
        It will also compare to the correct answer, if it is known already. 
        """
        print("WIP!")
    
    def do_updateREADME(self,arg):
        """Update README.md file to represent the current state of answers"""
        print("WIP!")
    
    def do_scan(self, arg):
        """Does a scan to given directory and adds all unkown puzzles solutions and tests to JSON file"""
        print("WIP!")
        
    def do_quit(self, line):
        """Exit the CLI."""
        return True
    
    def preloop(self):
        #load JSON file
        pass
    
    def postloop(self):
        #close JSON file
        pass
    
    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop

def parse(args):
    """
    parse for most commands.
    """
    year = 2024 #default year
    days = []
    year_str = ''
    day_str = ''
    if ' ' in args:
        year_str, day_str = args.split(' ')
    else:
        day_str = args
    day_str = day_str.split(',')
    #check empty days
    if day_str == []:
        raise Exception('NO day given')
    #year validation
    res = re.fullmatch(r'(\d{4})', year_str)
    if res is not None:
        cand = int(res.group(1))
        if cand >= 2015 and cand <= 2024:
           year = cand
        else:
            raise Exception('invalid year')    
    for d in day_str:
        res = re.fullmatch(r'all', d)
        if res is not None:
            for i in range(1, 26):
                days.append(i)
        else: 
            res = re.fullmatch(r'(\d+)-(\d+)', d)
            if res is not None:
                cand1 = int(res.group(1))
                cand2 = int(res.group(2))
                if cand1 > 0 and cand1 <= 25 and cand2 > 0 and cand2 <= 25:
                    for i in range(cand1, cand2+1):
                        days.append(i)
                else:
                   raise Exception('invalid day in '+res.group(0))
            else:
                res = re.fullmatch(r'(\d+)', d)
                if res is not None:
                    cand = int(res.group(1))
                    if cand > 0 and cand <= 25:
                        days.append(cand)
                    else:
                        raise Exception('invalid day given')
                else:
                   raise Exception('invalid day given')
    return (year,days)

def create(year, days):
    id = -1
    for i, entry in enumerate(save['data']):
        if entry['year'] == year:
            id = i
    if id == -1: #unknown year
        id = len(save['data'])
        save['data'].append({'year':year, 'solutions':[]})
    #known days
    known_days = [e['day'] for e in save['data'][id]['solutions']]
    for day in days:   
        if day in known_days:
            print('Warning', day, 'for year ',year,' already exists')
        else:
            save['data'][id]['solutions'].append({'day':day})
    print('created data entries')
    print(json.dumps(save))


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
            badges.append('[![AoC '+y+'](https://img.shields.io/badge/'+y+'-⭐%20'+y+'-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/'+y+')')
            table_rows.append('| ['+y +']('+y+') | ⭐️'+star_count+' | https://adventofcode.com/'+y+'|\n')
            
        print(badges)

if __name__ == '__main__':
    aocCLI().cmdloop()
