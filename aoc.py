import json
import re
import cmd

#puzzle states are stored in a JSON file

class aocCLI(cmd.Cmd):
    prompt = '>>'
    intro = 'Advent of Code command line interface. Type "help" for available commands.'
    
    def do_create(self, arg):
        """
        Add entry to the JSON file.
        Create directory and python file(s) for the defined days according to template if needed.
        DOES NOT OVERWRITE EXISTING FILES
        """
        print("WIP!")
    
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
        #load JSON save file
        pass
    
    def postloop(self):
        #close JSON save file
        pass
    
    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop

def parse(arg):
    """
    parse for most commands.
    """
    year = 2024 #default year
    day = 0
    return tuple(year,day)
    
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

if __name__ == '__main__':
    aocCLI().cmdloop()
