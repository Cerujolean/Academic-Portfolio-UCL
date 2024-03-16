#!/usr/bin/env python3
"""Analyse a vampire infiltration.
Student number: 21073274
"""

import sys
import os.path
from format_list import format_list, format_list_or, str_time, is_initial, period_of_time, day_of_time, time_of_day

# Section 2
def file_exists(file_name):    
   """Verify that the file exists.

   Args:
        
      file_name (str): name of the file

   Returns:
      boolean: returns True if the file exists and False otherwise.
   """
   return os.path.isfile(file_name)

# Section 3        
def parse_file(file_name):
   """Read the input file, parse the contents and return some data structures
   that contain the associated data for the vampire infiltration.

   Args:
      file_name (str): Contains the name of the file.

   Returns:
      participants: list of participants.
      days: list of pairs; the first element of a pair is the result of tests
         (dictionary from participants to "H"/"V"); the second is a list of
         contact groups (list of lists of participants)
   """
   try:  
      with open(file_name) as file:
         participants_split = file.readline().split(',')
            
         participants = []
         for name in participants_split:  
            participants.append(name.strip())
         str_all = file.readlines()
         days = []
         i = 0
         while i < len(str_all):
            line = str_all[i].strip()
            if 'H' in line or 'V' in line or '##' in line:
               contact_groups = []
               if 'H' in line or 'V' in line:
                  test_dict = {} 
                  for element in line.split(','):
                     key, value = element.split(':')
                     test_dict[key.strip()] = value.strip() == 'V'
               elif '##' in line:
                  test_dict = {}
                 
               num_pairs = int(str_all[i + 1])
               for j in range (i + 2, i + 2 + num_pairs):
                  contact_group = str_all[j].strip().split(', ')
                  contact_groups.append(contact_group)
               i += num_pairs + 1 
               days.append((test_dict, contact_groups))
            i += 1  

         return participants, days
   except ValueError:  
      print('Error found in file, aborting.')
      sys.exit()

# Section 4
def pretty_print_infiltration_data(data):
   """Print the associated data for the vampire infiltration in a pretty format.
   
   Args:
      data (pair): a pair of two lists defined previously, with the first list 
         to be the participants, and the second list to be a list of pairs, 
         containing a list for vampire test results and a list of contact 
         groups for each day as a pair.
   
   """
   participants, days = data
   participants_format = format_list(participants)
   print("Vampire Infiltration Data")
   title_participant = f'{len(days)} days '\
      f'with the following participants: {participants_format}.'
   print(title_participant)

   for each_day, (tests, contact_group) in enumerate(days, start = 1):
      test_number = len(tests)
      group_number = len(contact_group)
      
      if test_number == 1:
         test_plu = 'test'
      else:
         test_plu = 'tests'
      if group_number == 1:
         group_plu = 'group' 
      else:
         group_plu = 'groups'

      message = f'Day {each_day} has {test_number} vampire '\
         f'{test_plu} and {group_number} contact {group_plu}.'
      print(message)
      test_list = tests.items()
      print(f'  {test_number} {test_plu}')
      for name, test_result in sorted(test_list):
         if test_result is True:
            vampire_or_human = 'a vampire!'
         if test_result is False:
            vampire_or_human = 'human.'
         print(f'    {name} is {vampire_or_human}')

      print(f'  {group_number} {group_plu}')
      for group in contact_group:
         formatted_group = format_list(group)
         print(f'    {formatted_group}')

   print("End of Days")
   pass


# Section 5
def contacts_by_time(participant, time, contacts_daily):
   """Look up the contact group at a given time of the given participant.
   
   Args:
      participant (str): the participant to look up.
      time (int): the time unit.
      contacts_daily (list): a list of the contact groups on each day.

   Returns:
      group (list): the contact group of the participant for the time unit if 
         there is a contact group.
         Return an empty list if there are no contact groups for the time unit.
   
   """
   
   day = day_of_time(time)

   if time == 0:
      
      return []

   else:
      index = day - 1
      
   if 0 <= index < len(contacts_daily):
      contact_group = contacts_daily[index]
   
      for group in contact_group:
         if participant in group:
            return group
   
   return []

# Section 6
def create_initial_vk(participants):
   """Construct the initial vampire knowledge data structure.
   
   Args:
      participants(list): a list of participants.
   Returns:
      dict (dict): a dictionary mapping participants to their vampire status,
         setting initial status as 'U' (unclear).
         
   """
    
   status = 'U'
   dict = {key: status for key in participants}
   return dict

def pretty_print_vampire_knowledge(vk):
   """Print the vampire knowledge data structure in a pretty way.
   Args:
      vk (dict): the vampire knowledge data structure of a day, mapping 
         individuals to different status ('U' / 'V' / 'H').
   
   """
   key_list_H = []
   key_list_V = []
   key_list_U = []
   status_U = 'Unclear individuals:'
   status_H = 'Humans:'
   status_V = 'Vampires:'
   for key, value in vk.items():
      if value == 'U':
         key_list_U.append(key)
      elif value == 'H':
         
         key_list_H.append(key)
      elif value == 'V':
         key_list_V.append(key)

   
   print(f'  {status_H} {format_list(key_list_H)}')
   print(f'  {status_U} {format_list(key_list_U)}')
   print(f'  {status_V} {format_list(key_list_V)}')
   pass

# Done by professors
def pretty_print_vks(vks):
    print(f'Vampire Knowledge Tables')
    for i in range(len(vks)):
        print(f'Day {str_time(i)}:')
        pretty_print_vampire_knowledge(vks[i])
    print(f'End Vampire Knowledge Tables')

# Section 7
def update_vk_with_tests(vk, tests):
   """ Update the vampire knowledge data structure with vampire tests, printing
   error messages if there are any errors.
   
   Args:
      vk (dict): the vampire knowledge data structure of a time unit, mapping
         individuals to different status ('U' / 'V' / 'H').
      tests (dict): the vampire test results of a day, mapping each participant
         to their test results (vampire of human).
         
   Returns:
      vk (dict): the updated vampire knowledge data structure.
   
   """
   participants = list(vk.keys())
   for key, value in tests.items():

      if key not in participants:
         error = f'Error found in data: test subject '\
            f'is not a participant; aborting.'
         print(error)
         sys.exit()
     
      if value is True:
         if vk[key] == 'H':
            print(f'Error found in data: humans cannot be vampires; aborting.')
            sys.exit()
         else:
            vk[key] = 'V'

            
      if value is False:
         if vk[key] == 'V':
            print (f'Error found in data: vampires cannot be humans; aborting.')
            sys.exit()
         else:
            vk[key] = 'H'

   return vk

# Section 8
def update_vk_with_vampires_forward(vk_pre, vk_post):
   """ Update the vampire knowledge data structure, propagating the vampire
      status forward. Print error messages if there are any errors.
      
   Args:
      vk_pre (dict): vampire knowledge data structure of a time unit happened
         previously (before the vk_post).
      
      vk_post (dict):vampire knowledge data structure of a time unit happened
         after the vk_pre.

   Returns:
      vk_post (dict): the vk structure of the later time unit, updated with 
         knowledge of vampire status.
   
   
   """
   for p in vk_pre:
      if vk_pre[p] == 'V':
         if vk_post[p] == 'H':
            print(f'Error found in data: vampires cannot be humans; aborting.')
            sys.exit()
         else:
            vk_post[p] = 'V'     
         
   return vk_post

# Section 9
def update_vk_with_humans_backward(vk_pre, vk_post):
   """ Update the vampire knowledge data structure, propagating humanness 
      backwards.
   
   Args:
      vk_pre (dict): vampire knowledge data structure of the time unit happened
         previously (before the vk_post).
      vk_post (dict):vampire knowledge data structure of the
         time unit happened after the vk_pre.

   Returns:
      vk_pre (dict): the vk structure of the earlier time unit, updated with 
         knowledge of human status.
   
   """
   for p in vk_post:
      if vk_post[p] == 'H':
         if vk_pre[p] == 'V':
            print(f'Error found in data: humans cannot be vampires; aborting.')
            sys.exit()
         else:
            vk_pre[p] = 'H'
         
   return vk_pre

# Section 10
def update_vk_overnight(vk_pre, vk_post):
   """ Update the vampire knowledge data structure propagating the humanness 
      to the next morning.
      In this function, the gap betweeen vk_pre and vk_post is overnight 
      (between a PM and the subsequent AM). 
      Print error messages if there are any errors.
      
      Args:
         vk_pre (dict): vampire knowledge data structure of the time unit 
            happened previously (the PM before the vk_post).
         vk_post (dict):vampire knowledge data structure of the time unit
            (the AM) happened just after the vk_pre.
      
      Returns:
         vk_post (dict): the vk structure of the later time unit, updated 
            with knowledge of human status.
         
      """
   for p in vk_post:
      if vk_pre[p] == 'H':
         if vk_post[p] == 'V':
            print('Error found in data: humans cannot be vampires; aborting.')
            sys.exit()
         else: 
            vk_post[p] = vk_pre[p]
            
      if vk_pre[p] == 'V':
         if vk_post[p] == 'H':
            print('Error found in data: vampires cannot be humans; aborting.')
            sys.exit()
         else:
            vk_post[p] = vk_pre[p]

         
   return vk_post

# Section 11
def update_vk_with_contact_group(vk_pre, contacts, vk_post):
   """ Update vampire knowledge data structure based on analysing data on the 
      same day (AM/PM status and contact groups). 
      Print error messages if there are any errors.
   
   Args:
      vk_pre (dict): vampire knowledge data structure of a time unit happened 
         previously (the AM of the day).
      vk_post (dict):vampire knowledge data structure of the time unit after 
         the vk_pre (the PM of the day).
   
   Returns:
      vk_post (dict): the updated vk structure of the later time unit.
   """
   participant = vk_pre.keys() 
   for p in vk_post:
      if vk_pre[p] == 'V':
         if vk_post[p] == 'H':
            print('Error found in data: vampires cannot be human; aborting.')
            sys.exit()
      if not any(p in group for group in contacts):
         if vk_pre[p] == 'H':
               if vk_post[p] == 'V':
                  error = f'Error found in data: humans cannot '\
                     f'be vampires; aborting.'
                  print(error)
                  sys.exit()
               elif vk_post[p] == 'U':
                  vk_post[p] = 'H'

      for group in contacts:
         group_all_human = all(vk_pre.get(member, 'U') == 'H' \
            for member in group)
        
         for member in group:
            if member not in participant:
               error2 = f'Error found in data: contact subject '\
                  f'is not a participant; aborting.'
               print(error2)
               sys.exit()

            if group_all_human:  
               if vk_post[member] == 'V':
                  error3 = f'Error found in data: humans '\
                     f'cannot be vampires; aborting.'
                  print(error3)
                  sys.exit()
               elif vk_post[member] == 'U':
                  vk_post[member] = 'H'
   return vk_post

# Section 12
def find_infection_windows(vks):
   """ Calculate infection windows for the vampires.
   
   Args:
      vks (list): a list of dictionaries of vampire knowledge data of 
         each time unit.
   
   Returns: 
      windows (dict): a dictionary mapping definite vampires to the possible 
         infection window (a pair, start and end).
      
   """
   windows = {}
   vampires_on_last_day = {participant for participant, status \
      in vks[-1].items() if status == 'V'}
   for vampire in vampires_on_last_day:
      start = 0
      end = None
      time = 0
      for i in vks:
         if i.get(vampire) == 'H':
            start = time
         elif i.get(vampire) == 'V' and end is None:
            end = time   
         time += 1
         windows[vampire] = (start, end)
         
   return windows

def pretty_print_infection_windows(iw):
   """ Print the information of infection windows and the vampires in a pretty
      format.
   
   Args:
      iw (dict): a dictionary mapping definite vampires to the possible 
         infection window (a pair, start and end).
      
   """
   for vampire in sorted(iw.keys()):
      start, end = iw[vampire]
      message = f'  {vampire} was turned between day '\
         f'{str_time(start)} and day {str_time(end)}.'
      print(message)
   pass

# Section 13
def find_potential_sires(iw, vks, groups):
   """ Find who might have sired/infected the vampires potentially.
   
   Args:
      iw (dict): a dictionary mapping definite vampires to the possible 
         infection window (a pair, start and end).
      vks (list): a list of dictionaries of vampire knowledge data of each 
         time unit.
      groups (list): a list of the contact groups indexed by day.
      
   Returns:
      sires (dict): return a potential sire (ps) structure: a dictionary whose
         keys are the vampire participants and whose values are a list. The 
         list contains a pair of a time unit, and a list of contacts of that 
         participant in that time unit.
         
   """
   sires = {}
   for vampire in iw.keys():
      group_list = []
      start, end = iw[vampire]

      for time in range(start, end + 1):
         if time % 2 == 0 and time != 0:
            day = time // 2
            contacts = groups[day - 1]
         
            group_found = False
            for contact_group in contacts:
               if vampire in contact_group:
                  group_list.append((time, contact_group))
                  group_found = True
            if group_found == False:
               group_list.append((time, []))

      if group_list == []:
         sires[vampire] = []
      else:
         sires[vampire] = group_list
 
   return sires

def pretty_print_potential_sires(ps):
   """ Print the information of potential sires of the vampires in a pretty 
      format.
      
      Args:
         ps (dict): the potential sire structure: a dictionary whose
         keys are the vampire participants and whose values are a list. The 
         list contains a pair of a time unit, and a list of contacts of that 
         participant in that time unit.
   """

   for vampire in sorted(ps.keys()):
      
      print(f'  {vampire}:')
      if ps[vampire] == []:
         print(f'    (None)')
      else:
         for time, contact_group in ps[vampire]:
            message = f'    On day {str_time(time)}, '\
               f'met with {format_list(contact_group)}.'
            print(message)
   pass
            
            
# Section 14
def trim_potential_sires(ps,vks):
   """ Update the potential sire structure and narrow down the range of 
      possible sires of the vampires.
      
   Args:
      ps (dict): the potential sire structure: a dictionary whose
         keys are the vampire participants and whose values are a list. The 
         list contains a pair of a time unit, and a list of contacts of that 
         participant in that time unit.
      vks (list): the list of vampire knowledge structures.
   
   Returns:
      ps (dict): the updated potential sire structure.
      
   """
   
   for vampire in list(ps.keys()):
      new_contact = []

      for time, contact in ps[vampire]:
         if contact:
            vampire_test = vks[time]
            trim_contact = []
            for person in contact:
               if person != vampire and vampire_test.get(person) != 'H':
                  trim_contact.append(person)
               
            if trim_contact:
               new_contact.append((time, trim_contact))

      ps[vampire] = new_contact

   return ps

# Section 15
def trim_infection_windows(iw,ps):
   """ Update the infection windows structure based on the trimmed ps 
      structure.
      
   Args:
      iw (dict): a dictionary mapping definite vampires to the possible
         infection window (a pair, start and end).
      ps (dict): the potential sire structure: a dictionary whose
         keys are the vampire participants and whose values are a list. The 
         list contains a pair of a time unit, and a list of contacts of that 
         participant in that time unit.
      
   Returns:
      iw (dict): the updated infection window dictionary.
      
      
   """
   for vampire in iw.keys():
      if ps[vampire] == []:
         iw[vampire] = (0,0)
      else:
         for time, contact in ps[vampire]:
            last_time = time
            start, end = iw[vampire]
            if start % 2 != 0: 
               new_start = start + 1
            else:
               new_start = start
            iw[vampire] = (new_start, last_time)
      
   return iw

# Section 16
def update_vks_with_windows(vks,iw):
   """ Update the vks structure with the latest infection windows.
   
   Args:
      vks (list): the list of time-indexed vk structures.
      iw (dict): a dictionary mapping definite vampires to the possible 
         infection window (a pair, start and end).
   
   Returns:
      (vks, changes): a pair. 
         vks is the updated vks list.
         changes is an integer indicating the number of changes 
         made to the vks list.
   
   """
   changes = 0
   for person, time_window in iw.items():
      start, end = time_window
      for i in range(0, start):
         if vks[i][person] == 'V':
            print(f'Error found in data: humans cannot be vampires; aborting.')
            sys.exit()
         elif vks[i][person] == 'U':
            vks[i][person] = 'H'
            changes += 1
            
      for i in range (end, len(vks)):
         if vks[i][person] == 'H':
            print(f'Error found in data: vampires cannot be human; aborting.')
            sys.exit()
         elif vks[i][person] == 'U':
            vks[i][person] = 'V'
            changes += 1
  
   return (vks,changes)

# Section 17; done by professors
def cyclic_analysis(vks,iw,ps):
    count = 0
    changes = 1
    while(changes != 0):
        ps = trim_potential_sires(ps,vks)
        iw = trim_infection_windows(iw,ps)
        (vks,changes) = update_vks_with_windows(vks,iw)
        count = count + 1
    return (vks,iw,ps,count)

# Section 18: vampire strata
def vampire_strata(iw):
   """ Calculate vampire stratas from infection windows.
   Args:
      iw (dict): a dictionary mapping definite vampires to the possible 
         infection window (a pair, start and end).
      
   Returns:
      (originals,unclear_vamps,newborns): a triple of three sets: 
         original vampires, unknowns, and newborn vampires.
    
   """
   origin_list = []
   unclear_list = []
   new_list = []
   for person, time_windows in iw.items():
      start, end = time_windows
      if start == 0:
         if end == 0:
            origin_list.append(person)
         else:
            unclear_list.append(person)
      else:
         new_list.append(person)
          
                
   originals = set(origin_list)
   unclear_vamps = set(unclear_list)
   newborns = set(new_list)
    
   return (originals,unclear_vamps,newborns)
 
def pretty_print_vampire_strata(originals, unclear_vamps, newborns):
   """ Print the vampire strata calculated in a pretty format.
   Args:
      originals (set): a set of original vampires.
      unclear_vamps (set): a set of unknown vampires (original/newborn).
      newborns (set): a set of newborn vampires.
    
   """
    
   print(f'  Original vampires: {format_list(originals)}')
   print(f'  Unknown strata vampires: {format_list(unclear_vamps)}')
   print(f'  Newborn vampires: {format_list(newborns)}')
   pass

# Section 19: vampire sire sets
def calculate_sire_sets(ps):
   """ Calculate definite sires from the ps structure.
   which takes a ps structure and returns a sire set (ss) structure: 
   a map from vampire names to sets of possible sires (for originals, this will be the empty set).
   
   Args:
      ps (dict): the potential sire structure: a dictionary whose
         keys are the vampire participants and whose values are a list. The 
         list contains a pair of a time unit, and a list of contacts of that 
         participant in that time unit.
         
   Returns:
      ss (dict): a dictionary mapping vampire names to sets of possible sires.
      
   """
   ss = {}
   for vampire, contacts in ps.items():
      sire = set()
      for _, contact_list in contacts:
         sire.update(contact_list)
          
      ss[vampire] = sire
   return ss

def pretty_print_sire_sets(ss,iw,vamps,newb):
   """ Print the potential sires or the definite sires of the vampires
      in a pretty format.
      
   Args:
      ss (dict): a dictionary mapping vampire names to sets of possible sires.
      iw (dict): a dictionary mapping definite vampires to the possible 
         infection window (a pair, start and end).
      vamps (set): a set of vampires (a subset of the vampires in ss).
      newb (Boolean): a Boolean flag (True = newborns; False = unknown status).
      
   """
   if newb is True:
      language = 'was sired by'
      title = 'Newborn vampires'
   if newb is False:
      language = 'could have been sired by'
      title = 'Vampires of unknown strata'
       
   print(f'{title}:')
   if not vamps:
      print('  (None)')
   for vampire in sorted(vamps):
      start, end = iw[vampire]
      if start == end:
         time_print = f'on day {str_time(start)}'
      else:
         time_print = f'between day {str_time(start)} and day {str_time(end)}'
      sire = ss.get(vampire, [])
       

      print(f'  {vampire} {language} {format_list_or(sire)} {time_print}.')

   pass

# Section 20: vampire sire sets
def find_hidden_vampires(ss,iw,vamps,vks):
   """ Find the hidden vampires by logical deduction and update vks structures.
   Print error messages if there are any errors.
   Args:
      ss (dict): a dictionary mapping vampire names to sets of possible sires.
      iw (dict): a dictionary mapping definite vampires to the possible 
         infection window (a pair, start and end).
      vamps (set): a set of vampires (a subset of the vampires in ss).
      vks (list): the list of vampire knowledge structures.
      
   Returns:
      (vks, changes): a pair. 
         vks is the updated vks list.
         changes is an integer indicating the number of changes 
         made to the vks list.

   """
   changes = 0
   for vampire in vamps:
      sires = ss[vampire]
      start, end = iw[vampire]
       
      if sires and len(sires) == 1:
         sire = next(iter(sires))
         for i in range(end - 1, len(vks)):
            if vks[i][sire] == 'H':
               error = f'Error found in data: vampires cannot be '\
                  f'humans; aborting.'
               print(error)
               sys.exit()
            if vks[i][sire] == 'U':
               changes += 1
               vks[i][sire] = 'V'
  

   return (vks,changes)

# Section 21; done by professor
def cyclic_analysis2(vks,groups):
    count = 0
    changes = 1
    while(changes != 0):
        iw = find_infection_windows(vks)
        ps = find_potential_sires(iw, vks, groups)
        vks,iw,ps,countz = cyclic_analysis(vks,iw,ps)
        o,u,n = vampire_strata(iw)
        ss = calculate_sire_sets(ps)
        vks,changes = find_hidden_vampires(ss,iw,n,vks)        
        count = count + 1
    return (vks,iw,ps,ss,o,u,n,count)

def main():
    """Main logic for the program.  Do not change this (although if 
       you do so for debugging purposes that's ok if you later change 
       it back...)
    """
    filename = ""
    # Get the file name from the command line or ask the user for a file name
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()

    # Section 2. Check that the file exists
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    # Section 3. Create contacts dictionary from the file
    # Complete function parse_file().
    data = parse_file(filename)
    participants, days = data
    tests_by_day = [d[0] for d in days]
    groups_by_day = [d[1] for d in days]

    # Section 4. Print contact records
    pretty_print_infiltration_data(data)

    # Section 5. Create helper function for time analysis.
    print("********\nSection 5: Lookup helper function")
    if len(participants) == 0:
        print("  No participants.")
    else:
        p = participants[0]
        if len(days) > 1:
            d = 2
        elif len(days) == 1:
            d = 1
        else:
            d = 0
        t = time_of_day(d,False)
        t2 = time_of_day(d,True)
        print(f"  {p}'s contacts for time unit {t} (day {day_of_time(t)}) are {format_list(contacts_by_time(p,t,groups_by_day))}.")
        print(f"  {p}'s contacts for time unit {t2} (day {day_of_time(t)}) are {format_list(contacts_by_time(p,t2,groups_by_day))}.")
        assert(contacts_by_time(p,t,groups_by_day) == contacts_by_time(p,t2,groups_by_day))

    # Section 6.  Create the initial data structure and pretty-print it.
    print("********\nSection 6: create initial vampire knowledge tables")
    vks = [create_initial_vk(participants) for i in range(1 + (2 * len(days)))]
    pretty_print_vks(vks)

    # Section 7.  Update the VKs with test results.
    print("********\nSection 7: update the vampire knowledge tables with test results")
    for t in range(1,len(vks),2):
        vks[t] = update_vk_with_tests(vks[t],tests_by_day[day_of_time(t)-1])
    pretty_print_vks(vks)

    # Section 8.  Update the VKs to push vampirism forwards in time.
    print("********\nSection 8: update the vampire knowledge tables by forward propagation of vampire status")
    for t in range(1,len(vks)):
        vks[t] = update_vk_with_vampires_forward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Section 9.  Update the VKs to push humanism backwards in time.
    print("********\nSection 9: update the vampire knowledge tables by backward propagation of human status")
    for t in range(len(vks)-1, 0, -1):
        vks[t-1] = update_vk_with_humans_backward(vks[t-1],vks[t])
    pretty_print_vks(vks)

    # Sections 10 and 11.  Update the VKs to account for contact groups and safety at night.
    print("********\nSections 10 and 11: update the vampire knowledge tables by forward propagation of contact results and overnight")
    for t in range(1, len(vks), 2):
        vks[t+1] = update_vk_with_contact_group(vks[t],groups_by_day[day_of_time(t)-1],vks[t+1])
        if t + 2 < len(vks):
            vks[t+2] = update_vk_overnight(vks[t+1],vks[t+2])
    pretty_print_vks(vks)

    # Section 12. Find infection windows for vampires.
    print("********\nSection 12: Vampire infection windows")
    iw = find_infection_windows(vks)
    pretty_print_infection_windows(iw)

    # Section 13. Find possible vampire sires.
    print("********\nSection 13: Find possible vampire sires")
    ps = find_potential_sires(iw, vks, groups_by_day)
    pretty_print_potential_sires(ps)

    # Section 14. Trim the potential sire structure.
    print("********\nSection 14: Trim potential sire structure")
    ps = trim_potential_sires(ps,vks)
    pretty_print_potential_sires(ps)

    # Section 15. Trim the infection windows.
    print("********\nSection 15: Trim infection windows")
    iw = trim_infection_windows(iw,ps)
    pretty_print_infection_windows(iw)

    # Section 16. Update the vk structures with infection windows.
    print("********\nSection 16: Update vampire information tables with infection window data")
    (vks,changes) = update_vks_with_windows(vks,iw)
    pretty_print_vks(vks)
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 17.  Cyclic analysis for sections 14-16 
    print("********\nSection 17: Cyclic analysis for sections 14-16")
    vks,iw,ps,count = cyclic_analysis(vks,iw,ps)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print('Potential sires:')
    pretty_print_potential_sires(ps)
    print('Infection windows:')
    pretty_print_infection_windows(iw)
    pretty_print_vks(vks)       

    # Section 18.  Calculate vampire strata
    print("********\nSection 18: Calculate vampire strata")
    (origs,unkns,newbs) = vampire_strata(iw)
    pretty_print_vampire_strata(origs,unkns,newbs)

    # Section 19.  Calculate definite sires
    print("********\nSection 19: Calculate definite vampire sires")
    ss = calculate_sire_sets(ps)
    pretty_print_sire_sets(ss,iw,unkns,False)
    pretty_print_sire_sets(ss,iw,newbs,True)    

    # Section 20.  Find hidden vampires
    print("********\nSection 20: Find hidden vampires")
    (vks, changes) = find_hidden_vampires(ss,iw,newbs,vks)
    pretty_print_vks(vks)           
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 21.  Cyclic analysis for sections 14-20
    print("********\nSection 21: Cyclic analysis for sections 14-20")
    (vks,iw,ps,ss,o,u,n,count) = cyclic_analysis2(vks,groups_by_day)
    str_s = "" if count == 1 else "s"    
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print("Infection windows:")
    pretty_print_infection_windows(iw)
    print("Vampire potential sires:")
    pretty_print_potential_sires(ps)
    print("Vampire strata:")
    pretty_print_vampire_strata(o,u,n)
    print("Vampire sire sets:")    
    pretty_print_sire_sets(ss,iw,u,False)
    pretty_print_sire_sets(ss,iw,n,True)
    pretty_print_vks(vks)       
    
if __name__ == "__main__":
    main()