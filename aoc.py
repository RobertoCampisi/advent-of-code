import json
import re
import cmd
import os
import urllib.request

#puzzle and solution states are stored in a JSON file
SAVEFILE_NAME = "save.json"
state = {'token': '', 'data': []}

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
            print('created data entries')
        except Exception as e:
            print('Failed to create data entry: ', e) 
        
    def do_fetch(self, arg):
        """
        Fetch puzzle input from advent of code.
        """
        try:
            fetch(*parse(arg))
            print('fetch puzzle input from Advent of Code')
        except Exception as e:
            print('Failed to fetch puzzle input: ', e)

    def do_token(self, arg):
        """Stores or shows the token (session cookie) for authorisation to the Advent of Code website"""
        if arg == '':
            print('token:', state['token'])
        else:
            state['token'] = arg
        save() 
    
    def do_test(self, arg):
        """Test puzzle on added examples and compare the outputs to the expected results"""
        try:
            test(*parse(arg))
        except Exception as e:
            print('Failed to test solution: ', e) 
        
    def do_run(self, arg):
        """Execute a puzzle solution on the input and print the output."""
        try:
            run(*parse(arg))
        except Exception as e:
            print('Failed to run solution: ', e) 
        
    def do_submit(self, arg):
        """
        Submits the output of given puzzle solution to the advent of code website.
        If the answer is correct, it will store the result for the future.
        """
        try:
            run(*parse(arg))
        except Exception as e:
            print('Failed to submit solution: ', e) 
    
    def do_benchmark(self, arg):
        """
        Benchmark the time it takes to execute the given puzzle solution(s). 
        It will also compare to the correct answer, if it is known already. 
        """
        try:
            run(*parse(arg))
        except Exception as e:
            print('Failed to benchmark solution: ', e) 
    
    def do_updateREADME(self,arg):
        """Update README.md file to represent the current state of answers"""
        try:
            update_README()
        except Exception as e:
            print('Failed to update README: ', e) 
    
    def do_scan(self, arg):
        """Does a scan to given directory and adds all unkown puzzles solutions and tests to JSON file"""
        print("WIP!")
        
    def do_quit(self, line):
        """Exit the CLI."""
        return True
    
    def preloop(self):
        pass
            
    def postloop(self):
        #close JSON file
        save()
    
    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop

def save():
    with open(SAVEFILE_NAME, 'w') as savefile:
            json.dump(state, savefile, indent=2)

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

#return the entry index of given year. returns -1 if entry does not exist
def get_year_id(year):
    id = -1
    for i, entry in enumerate(state['data']):
        if entry['year'] == year:
            id = i
    return id

def create(year, days):
    id = get_year_id(year)
    if id == -1: #unknown year
        id = len(state['data'])
        state['data'].append({'year':year, 'solutions':[]})
        try:
            os.mkdir(str(year))
        except FileExistsError:
            pass
    #known days
    known_days = [e['day'] for e in state['data'][id]['solutions']]
    for day in days:   
        if day in known_days:
            print('Warning', day, 'for year ',year,' already exists')
        else:
            state['data'][id]['solutions'].append({'day':day})
    save()

def fetch(year, days):
    id = get_year_id(year)
    if id == -1: #unknown year
        raise Exception("unknown year")
    try:#create directory if not exists
        os.mkdir(str(year)+'/input')
    except FileExistsError:
        pass
    for day in days:
        req = urllib.request.Request('https://adventofcode.com/'+str(year)+'/day/'+str(day)+'/input')
        req.add_header('Cookie', 'session='+state['token'])
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
            if 'Puzzle inputs differ by user.  Please log in to get your puzzle input.' not in html:
                f = open(str(year)+'/input/day'+str(day)+".txt", "w")
                f.write(html)
            else:
                raise Exception("missing or invalid session token")

def test(year, days):
    id = get_year_id(year)
    if id == -1: #unknown year
        raise Exception("unknown year")
    print("WIP!")

def run(year, days):
    id = get_year_id(year)
    if id == -1: #unknown year
        raise Exception("unknown year")
    print("WIP!")

def submit(year, days):
    id = get_year_id(year)
    if id == -1: #unknown year
        raise Exception("unknown year")
    print("WIP!")

def benchmark(year, days):
    id = get_year_id(year)
    if id == -1: #unknown year
        raise Exception("unknown year")
    print("WIP!")


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
    #load JSON file
    try:
        with open(SAVEFILE_NAME, 'r') as savefile:
            state = json.load(savefile)
    except FileNotFoundError:
        save()
    aocCLI().cmdloop()
