import json
import re
import cmd
import os
import urllib.request
import sys
import time
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
        """Does a scan in the directory for a spesific file structure and adds entries of all found puzzles solutions to JSON file"""
        try:
            scan_directory()
        except Exception as e:
            print('Failed to scan current directory', e)

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

#function to parse and validate an expected year argument
def parse_year(year_arg):
    res = re.fullmatch(r'(\d{4})', year_arg)
    if res is not None:
        cand = int(res.group(1))
        if 2015 <= cand <= 2024: #automate upperbound
            return res.group(1)
        else:
            raise Exception('{} is an invalid year'.format(cand))
    else:
        raise Exception('{} is an invalid year'.format(year_arg))

#function to parse and validate an days argument
def parse_days(days_arg):
    days = []
    for d in days_arg:
        res = re.fullmatch(r'all', d)
        if res is not None:
            for i in range(1, 26):
                days.append(str(i))
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
    return days
          
#TODO simplify and unspaghettify the function even further
def parse(args):
    """
    parse and validate provided arguments
    """
    part_one_patterns = [r'one',r'p[\-_=]{0,1}1',r'part[\-_=]{0,1}one',r'part[\-_=]{0,1}1']
    part_two_patterns = [r'two',r'p[\-_=]{0,1}2',r'part[\-_=]{0,1}two',r'part[\-_=]{0,1}2']
    number_option_patterns = [r'n[\-_=]{0,1}(\d+)'] #additional integer used for some functions
    year = '2024' #default year #TODO: automate this, default year updates every end of november
    days = []
    part = 0 #default
    number = None #no defined default
    year_arg = ''
    days_arg = ''
    #optional arguments
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
    
    #determine if the first argument is a year or day argument
    temp = args.split(' ')
    if len(temp) == 1 and (part != 0 or number is not None):
        raise Exception('required argument for day missing')
    elif any([len(temp) == 1 and part == 0 and number is None,
              len(temp) == 2 and (part != 0 or number is not None),
              len(temp) == 3 and part != 0 and number is not None]):
        days_arg = temp[0] 
    elif any([len(temp) == 2 and part == 0 and number is None, 
              len(temp) == 3 and part == 0 and number is not None,
              len(temp) == 3 and part != 0 and number is None,
              len(temp) == 4 and part != 0 and number is not None]):
        year_arg, days_arg = temp[0:2]
    elif len(temp) == 3 and part == 0 and number is None:
        raise Exception('too many arguments provided or unclear defined part.')
    else:
        raise Exception('incorrect number of arguments provided')
    #parse year, if year argument is given
    if year_arg != '':
        year = parse_year(year_arg)
    #parse and validate the required days argument 
    days_arg = days_arg.split(',') 
    if not days_arg:
        raise Exception('no day provided')
    days = parse_days(days_arg)
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
            template = open('template.py', 'r').read().format(year,int(day))
            fname = '{}/day{:02d}.py'.format(year,int(day))
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
                        f = open('{}/input/day{:02d}.txt'.format(year, int(day)), "w")
                        f.write(html.rstrip())#ignore new_line character at the end
                    else:
                        raise ValueError("Received bad response")
                else:
                        raise ValueError("Received bad response")
        time.sleep(1)#we do not want to spam the website, when fetching input data in bulk
        

def test(year, days, part, number):
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
                (out, err) = run_solution("python {}/day{:02d}.py part_one".format(year, int(day)))
                print(err) if err else print(out)
                (out, err) = run_solution("python {}/day{:02d}.py part_two".format(year, int(day)))
                print(err) if err else print(out)
            case 1:
                (out, err) = run_solution("python {}/day{:02d}.py part_one".format(year, int(day)))
                print(err) if err else print(out)
            case 2:
                (out, err) = run_solution("python {}/day{:02d}.py part_two".format(year, int(day)))
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
    data = urllib.parse.urlencode({'level':part, 'answer':answer}).encode("utf-8")    
    req = urllib.request.Request('https://adventofcode.com/{}/day/{}/answer'.format(year,day),data=data)
    req.add_header('Cookie', 'session='+state['token'])
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")
        #todo extract response msg and return this
        if re.search('That\'s the', html): #assume answer is correct TODO:verify this
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
                (out, err) = run_solution("python {}/day{:02d}.py part_one".format(year, int(day)))
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
                    (out, err) = run_solution("python {}/day{:02d}.py part_two".format(year, int(day)))
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
                (out, err) = run_solution("python {}/day{:02d}.py part_one".format(year, int(day)))
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
                (out, err) = run_solution("python {}/day{}.py part_two".format(year, int(day)))
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
        def run_benchmark(part,save_tag):
            (out, err) = run_solution("python {}/day{:02d}.py benchmark {} {}".format(year, int(day), part, number))
            print(err) if err else print("day {} {} took {} milliseconds".format(day, part, out))
            if number >= 10: #treshold to store benchmark results
                state['data'][year][day][save_tag] = out + ' ms'
            return float(out) if not err else 0.0
        match part:
            case 0:
                total_milliseconds += run_benchmark('part_one','p1_bench')
                total_milliseconds += run_benchmark('part_two','p2_bench')
            case 1:
                total_milliseconds += run_benchmark('part_one','p1_bench')
            case 2:
                total_milliseconds += run_benchmark('part_two','p2_bench')
            case _:
                raise Exception('invalid arguments')
        if number >= 10:
            save()
    print("total average time taken: {} milliseconds".format(total_milliseconds))

def scan_directory():
    with os.scandir('.') as year_iter: #os scan to look for year folders
        solution_counter = 0
        for year_cand in year_iter:
            if not year_cand.name.startswith('.') and year_cand.is_dir():
                #look for valid years
                #TODO replace this with the 'valid_year_function' once parse() has modularised
                res = re.fullmatch(r'(\d{4})', year_cand.name)
                if res is not None:
                    cand = int(res.group(1))
                    if 2015 <= cand <= 2024:
                        year = res.group(1)
                        if year not in state['data']: #unknown year
                            state['data'][year] = {}
                        print('looking for solutions in folder {}...'.format(year))
                        with os.scandir('.\\{}\\'.format(year)) as day_iter: #os scan to look for solutions
                            for day_cand in day_iter:
                                if day_cand.name.startswith('day') and day_cand.is_file():
                                    try:
                                        day = int(day_cand.name[3:-3])
                                        if 1 <= day <= 25:
                                            if day not in state['data'][year]:
                                                state['data'][year][day] = {'answer_p1': None, 'answer_p2': None}
                                            solution_counter += 1
                                    except ValueError as e:
                                        pass #ignore these for now
                            save()
        print('found a total of {} solutions.'.format(solution_counter))                            
        


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
    summary = dict()
    table_rows = ['| Year | Stars | Advent of Code Link |','| :--: | :---: | :--: |']
    badges = []
    for year,solutions in state['data'].items():
        star_count = 0
        for day,solution_data in solutions.items():
            if solution_data['answer_p1'] is not None: star_count += 1
            if solution_data['answer_p2'] is not None: star_count += 1
        summary[year] = star_count
    for y,count in sorted(summary.items()):
        badges.append('[![AoC '+y+'](https://img.shields.io/badge/'+y+'-⭐%20'+str(count)+'-gray?logo=adventofcode&labelColor=8a2be2)](https://adventofcode.com/'+y+')')
        table_rows.append('| ['+y +']('+y+') | ⭐️'+str(count)+' | https://adventofcode.com/'+y+'|')
    with open('README.md','r+', encoding="utf-8") as f:
        current = f.read()
        current = re.sub(r'<!-- sum of stars 1: begin -->.*<!-- sum of stars 1: end -->', '<!-- sum of stars 1: begin -->(⭐ '+str(sum(summary.values()))+')<!-- sum of stars 1: end -->', current)
        current = re.sub(r'(?s)<!-- Badges of stars: begin -->.*<!-- Badges of stars: end -->', '<!-- Badges of stars: begin -->\n'+'\n'.join(badges)+'\n<!-- Badges of stars: end -->', current)
        current = re.sub(r'(?s)<!-- Table summary of years: begin -->.*<!-- Table summary of years: end -->', '<!-- Table summary of years: begin -->\n'+'\n'.join(table_rows)+'\n<!-- Table summary of years: end -->',current)
        f.seek(0)
        f.write(current)
        f.truncate()
            
        



if __name__ == '__main__':
    #sys.stout = Log()
    #load JSON file
    try:
        with open(SAVEFILE_NAME, 'r') as savefile:
            state = json.load(savefile)
    except FileNotFoundError:
        save()
    AoCCLI().cmdloop()
