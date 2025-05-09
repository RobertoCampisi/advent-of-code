import json
import re
import cmd
import os
import urllib.request
import sys
import time

import subprocess
from subprocess import Popen, PIPE, STDOUT

#puzzle and solution states are stored in a JSON file
SAVEFILE_NAME = "save.json"
state = {'token': '', 'data': {}}


class AoCCLI(cmd.Cmd):
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
            submit(*parse(arg))
        except Exception as e:
            print('Failed to submit solution: ', e) 
    
    def do_benchmark(self, arg):
        """
        Benchmark the time it takes to execute the given puzzle solution(s). 
        It will also compare to the correct answer, if it is known already. 
        """
        try:
            benchmark(*parse(arg))
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

    def do_parse(self, line):
        """method to Test current parse function"""
        try:
            print(parse(line))
        except Exception as e:
            print('failed to parse:',e)
        

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

#TODO simplify and unspaghettify the function
def parse(args):
    """
    parse for most commands.
    """
    part_one_patterns = [r'one',r'p[\-_=]{0,1}1',r'part[\-_=]{0,1}one',r'part[\-_=]{0,1}1']
    part_two_patterns = [r'two',r'p[\-_=]{0,1}2',r'part[\-_=]{0,1}two',r'part[\-_=]{0,1}2']
    number_option_patterns = [r'n[\-_=]{0,1}(\d+)'] #additional integer used for some functions
    year = '2024' #default year #TODO: automate this, default year updates every end of november
    days = []
    part = 0 #default
    number = None #no defined default
    year_str = ''
    day_str = ''
    #check for part 1 argument
    for pttrn in part_one_patterns:
        m = re.search(pttrn, args, re.IGNORECASE)
        if m is not None:
            if part == 0:
                part = 1
            else:
                raise Exception('invalid arguments')
    #check for part 2 argument
    for pttrn in part_two_patterns:
        m = re.search(pttrn, args, re.IGNORECASE)
        if m is not None:
            if part == 0:
                part = 2
            else:
                raise Exception('invalid arguments')
    # check for number argument
    for pttrn in number_option_patterns:
        m = re.search(pttrn, args, re.IGNORECASE)
        if m is not None:
            if number is None:
                number = int(m[1])
            else:
                raise Exception('invalid arguments')
    temp = args.split(' ')
    if len(temp) == 1 and part == 0 and number is None:
        day_str = temp[0]
    elif len(temp) == 1 and (part != 0 or number is not None):
        raise Exception('required argument for day missing')
    elif len(temp) == 2 and (part != 0 or number is not None):
        day_str = temp[0]
    elif len(temp) == 3 and part != 0 and number is not None:
        day_str = temp[0]
    elif len(temp) == 2 and part == 0 and number is None:
        year_str, day_str = temp[0:2]
    elif len(temp) == 3 and part == 0 and number is not None:
        year_str, day_str = temp[0:2]
    elif len(temp) == 3 and part != 0 and number is None:
        year_str, day_str = temp[0:2]
    elif len(temp) == 3 and part == 0 and number is None:
        raise Exception('too many arguments provided or unclear defined part.')
    elif len(temp) == 4 and part != 0 and number is not None:
        year_str, day_str = temp[0:2]
    else:
        raise Exception('incorrect number of arguments provided')
    #year validation
    if year_str != '':
        res = re.fullmatch(r'(\d{4})', year_str)
        if res is not None:
            cand = int(res.group(1))
            if 2015 <= cand <= 2024:
                year = res.group(1)
            else:
                raise Exception('{} is an invalid year'.format(cand))
        else:
            raise Exception('{} is an invalid year'.format(year_str))
    day_str = day_str.split(',') 
     #check empty days
    if not day_str:
        raise Exception('no day given')
    for d in day_str:
        res = re.fullmatch(r'all', d)
        if res is not None:
            for i in range(1, 26):
                days.append(i)
        else: 
            res = re.fullmatch(r'(\d+)\-(\d+)', d)
            if res is not None:
                cand1 = int(res.group(1))
                cand2 = int(res.group(2))
                if 0 < cand1 <= 25 and 0 < cand2 <= 25:
                    for i in range(cand1, cand2+1):
                        days.append(str(i))
                else:
                   raise Exception('invalid day in '+res.group(0))
            else:
                res = re.fullmatch(r'(\d+)', d)
                if res is not None:
                    cand = int(res.group(1))
                    if 0 < cand <= 25:
                        days.append(res.group(1))
                    else:
                        raise Exception('invalid day given')
                else:
                   raise Exception('invalid day given')
    return year,days,part,number

def create(year, days, part, number):
    if part != 0: 
        raise Exception('invalid command')
    if number is not None:
        raise Exception('invalid command')
    if year not in state['data']: #unknown year
        state['data'][year] = {}
        try:
            os.mkdir(year)
        except FileExistsError:
            pass
    #known days
    for day in days:   
        if day in state['data'][year]:
            print('Skipped, ', day, 'for year ',year,' already exists in JSON file')
        else:
            template = open('template.py', 'r').read().format(year,day)
            fname = '{}/day{}.py'.format(year,day)
            if not os.path.isfile(fname):
                with open(fname,'w') as f:
                    f.write(template)
                    print('Successfully created {}'.format(fname))
            else:
                print('Warning python file for {} for year {} already exists.'.format(day, year))
            state['data'][year][day] = {'answer_p1': None, 'answer_p2': None}
    save()

def fetch(year, days, part, number):
    if part != 0 or number is not None:
        raise Exception('invalid argument')
    if year not in state['data']: #unknown year
        raise Exception("unknown year")
    try:#create directory if not exists
        os.mkdir(year+'/input')
    except FileExistsError:
        pass
    for day in days:
        if day in state['data'][year]:
            if state['token'] == '':
                raise Exception("missing session token. please add the <session cookie> to token in the savefile or use token <session_cookie>.")
            req = urllib.request.Request('https://adventofcode.com/{}/day/{}/input'.format(year,day))
            req.add_header('Cookie', 'session='+state['token'])
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    html = response.read().decode("utf-8")
                    if 'Puzzle inputs differ by user. Please log in to get your puzzle input.' not in html:
                        f = open('{}/input/day{}.txt'.format(year, day), "w")
                        f.write(html[:-1])#ignore new_line character at the end
                    else:
                        raise ValueError("Received bad response")
                else:
                        raise ValueError("Received bad response")
        time.sleep(1)#we do not want to spam the website, when fetching input data in bulk
        

def test(year, days):
    if year not in state['data']: #unknown year
        raise Exception("unknown year")
    print("WIP!")

def run_solution(cmd):
    proc = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    return output.decode(sys.stdout.encoding).strip(), error.decode(sys.stdout.encoding)

def run(year, days, part, number):
    if number is not None:
        raise Exception('invalid argument')
    if year not in state['data']: #unknown year
        raise Exception("unknown year")
    for day in days:
        match part:
            case 0:
                (out, err) = run_solution("python {}/day{}.py part_one".format(year,day))
                print(err) if err else print(out)
                (out, err) = run_solution("python {}/day{}.py part_two".format(year, day))
                print(err) if err else print(out)
            case 1:
                (out, err) = run_solution("python {}/day{}.py part_one".format(year, day))
                print(err) if err else print(out)
            case 2:
                (out, err) = run_solution("python {}/day{}.py part_two".format(year,day))
                print(err) if err else print(out)
            case _:
                raise Exception('invalid argument')

def fetch_previous_submission(year, day):
    if state['token'] == '':
        raise Exception("missing session token. please add the <session cookie> to token in the savefile or use token <session_cookie>.")
    req = urllib.request.Request('https://adventofcode.com/{}/day/{}'.format(year,day))
    req.add_header('Cookie', 'session='+state['token'])
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")
        prev_submissions = re.findall(r'<p>Your puzzle answer was <code>(.*)</code>.</p>', html)
        if len(prev_submissions) == 2: #both parts submitted and answered correctly
            state['data'][year][day]['answer_p1'] = prev_submissions[0]
            state['data'][year][day]['answer_p2'] = prev_submissions[1]
            print('found previous answer for part 1 and 2')
        elif len(prev_submissions) == 1: #part 1 
            state['data'][year][day]['answer_p1'] = prev_submissions[0]
            print('found previous answer for part 1')
        else:
            print('no previous answer found')
    save()

def submit_answer(year, day, part, answer):
    if state['token'] == '':
        raise Exception("missing session token. please add the <session cookie> to token in the savefile or use token <session_cookie>.")
    data = urllib.parse.urlencode({'level':part, 'answer':answer})    
    req = urllib.request.Request('https://adventofcode.com/{}/day/{}/answer'.format(year,day),data=data)
    req.add_header('Cookie', 'session='+state['token'])
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")
        #todo extract response msg and return this
        if re.search('That\'s the'): #assume answer is correct TODO:verify this
            state['data'][year][day]['answer_p{}'.format(part)] = answer
            save()
            return True
        return False

def submit(year, days, part, number):
    if number is not None:
        raise Exception('nubmer argument invalid for command submit')
    if year not in state['data']: #unknown year
        raise Exception("unknown year")
    for day in days:
        if  state['data'][year][day]['answer_p1'] is None or state['data'][year][day]['answer_p2'] is None:
            #check for previous submission
            print("checking for previous answers...")
            fetch_previous_submission(year,day)
        match part:
            case 0:
                on_cooldown = False
                (out, err) = run_solution("python {}/day{}.py part_one".format(year, day))
                if err:
                    print(err)
                    raise RuntimeError
                else:
                    if  state['data'][year][day]['answer_p1'] is None:
                        print("sumbitting \"{}\" as answer for day {} part 1".format(out, day))
                        #TODO: store submission time and build in 5 minute check before resubmitting
                        if submit_answer(year, day, 1, out):
                            print("\"{}\" : * The answer is correct! *".format(out))
                        else:
                            print("\"{}\", sadly, is incorrect. wait 5 minutes before resubmitting.".format(out))
                            on_cooldown = True
                    else:
                        if out == state['data'][year][day]['answer_p1']:
                            print("\"{}\" : * The answer is correct! *".format(out))
                        else:
                            print("\"{}\", sadly, is incorrect. ".format(out))
                if not on_cooldown:
                    (out, err) = run_solution("python {}/day{}.py part_two".format(year, day))
                    if err:
                        print(err)
                        raise RuntimeError
                    else:
                        if  state['data'][year][day]['answer_p2'] is None:
                            print("sumbitting \"{}\" as answer for day {} part 2".format(out, day))
                            #TODO: store submission time and build in 5 minute check before resubmitting
                            if submit_answer(year, day, 2, out):
                                print("\"{}\" : * The answer is correct! *".format(out))
                            else:
                                print("\"{}\", sadly, is incorrect. wait 5 minutes before resubmitting.".format(out))
                        else:
                            if out == state['data'][year][day]['answer_p2']:
                                print("\"{}\" : * The answer is correct! *".format(out))
                            else:
                                print("\"{}\", sadly, is incorrect. ".format(out))
                else: 
                    raise Exception('The submission of day {day} part 1 was incorrect. \nCurrent submissions are on a five minute timeout. Please wait before resubmitting.')
            case 1:
                (out, err) = run_solution("python {}/day{}.py part_one".format(year, day))
                if err:
                    print(err)
                    raise RuntimeError
                else:
                    if  state['data'][year][day]['answer_p1'] is None:
                        print("sumbitting \"{}\" as answer for day {} part 1".format(out, day))
                        #TODO: store submission time and build in 5 minute check before resubmitting
                        if submit_answer(year, day, 1, out):
                            print("\"{}\" : * The answer is correct! *".format(out))
                        else:
                            print("\"{}\", sadly, is incorrect. wait 5 minutes before resubmitting.".format(out))
                    else:
                        if out == state['data'][year][day]['answer_p1']:
                            print("\"{}\" : * The answer is correct! *".format(out))
                        else:
                            print("\"{}\", sadly, is incorrect. ".format(out))
            case 2:
                (out, err) = run_solution("python {}/day{}.py part_two".format(year, day))
                if err:
                    print(err)
                    raise RuntimeError
                else:
                    if  state['data'][year][day]['answer_p2'] is None:
                        print("sumbitting \"{}\" as answer for day {} part 2".format(out, day))
                        #TODO: store submission time and build in 5 minute check before resubmitting
                        if submit_answer(year, day, 2, out):
                            print("\"{}\" : * The answer is correct! *".format(out))
                        else:
                            print("\"{}\", sadly, is incorrect. wait 5 minutes before resubmitting.".format(out))
                    else:
                        if out == state['data'][year][day]['answer_p2']:
                            print("\"{}\" : * The answer is correct! *".format(out))
                        else:
                            print("\"{}\", sadly, is incorrect. ".format(out))
            case _:
                raise Exception('invalid part argument')
        time.sleep(1) #to reduce request load to advent of code
    print("WIP!")

def benchmark(year, days, part, number):
    if year not in state['data']: #unknown year
        raise Exception("unknown year")
    if number is None:
        number = 100 #default
    if number < 1:
        raise Exception('invalid argument')
    total_milliseconds = 0.0
    for day in days:
        match part:
            case 0:
                (out, err) = run_solution("python {}/day{}.py benchmark part_one {}".format(year, day, number))
                print(err) if err else print("day {} part_one took {} milliseconds".format(day, out))
                total_milliseconds += float(out) if not err else 0.0
                if number >= 10: #treshold to store benchmark results
                    state['data'][year][day]['p1_prev_bench'] = out + ' ms'
                (out, err) = run_solution("python {}/day{}.py benchmark part_two {}".format(year, day, number))
                print(err) if err else print("day {} part_two took {} milliseconds".format(day, out))
                total_milliseconds += float(out)  if not err else 0.0
                if number >= 10: #treshold to store benchmark results
                    state['data'][year][day]['p2_prev_bench'] = out + ' ms'

            case 1:
                (out, err) = run_solution("python {}/day{}.py benchmark part_one {}".format(year, day, number))
                print(err) if err else print("day {} part_one took {} milliseconds".format(day, out))
                total_milliseconds += float(out)  if not err else 0.0
                if number >= 10: #treshold to store benchmark results
                    state['data'][year][day]['p1_prev_bench'] = out + ' ms'
            case 2:
                (out, err) = run_solution("python {}/day{}.py benchmark part_two {}".format(year, day, number))
                print(err) if err else print("day {} part_two took {} milliseconds".format(day, out))
                total_milliseconds += float(out)  if not err else 0.0
                if number >= 10: #treshold to store benchmark results
                    state['data'][year][day]['p2_prev_bench'] = out + ' ms'
            case _:
                raise Exception('invalid arguments')
        if number >= 10:
            save()
    print("total average time taken: {} milliseconds".format(total_milliseconds))


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
    #sys.stout = Log()
    #load JSON file
    try:
        with open(SAVEFILE_NAME, 'r') as savefile:
            state = json.load(savefile)
    except FileNotFoundError:
        save()
    AoCCLI().cmdloop()
