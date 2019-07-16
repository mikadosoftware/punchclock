"""
The idea behind punchclock is to use the data stored in `git log` to provide
data for developers to fill in timesheets to prove to businesses that they did do 
some actualy f***g work.

It turns out that having actual data to back up timesheets like this has several benefits

* It's easier than making up "err about 3 hours last week" 
* It actually accurately apportions the cost of a developer to different projects
  so it really actually is a valuable accountancy tool (not that developers care)
* Err

I need a practise log - so i need to generate one

/////// Eaxmplae
commit cd6c5b6d86a4758e1edccfd18e2420f3417457a2
Author: Paul Brian <paul@mikadosoftware.com>
Date:   Sun Oct 21 20:55:56 2018 +0100

    do more on reporting
    
    - proejct mgmt / co
///////



"""
import uuid
import hashlib
import datetime


alice = 'alice@example.com'
bob = 'bob@example.com'
charlie = 'charlie@example.com'

fakelog = {'REPO1':
           [(alice,   '20180101 09:01', 'ZEUS-1234'),
            (alice,   '20180101 10:01', 'ZEUS-1234'),
            (alice,   '20180101 11:01', 'AJAX-1234'),
            (bob,     '20180101 12:01', 'AJAX-5678'),
            (charlie, '20180101 13:01', 'ZEUS-5678'),
            (alice,   '20180101 15:01', 'ZEUS-1234'),
            (alice,   '20180102 10:01', 'AJAX-7777'),
            (bob,     '20180102 09:01', 'AJAX-5678'),
            (bob,     '20180101 12:01', 'ZEUS-9999'),
            ],
           
           'REPO2':
           [ (alice,  '20180101 09:30', 'FISH-1234'),
            (alice,   '20180101 10:30', 'FISH-5678'),
            (alice,   '20180101 11:30', 'AJAX-1234'),
            (bob,     '20180101 12:30', 'AJAX-2222'),
            (charlie, '20180101 13:30', 'ZEUS-2222'),
            
           ]}

def mk_revision_number(name, date, ticket):
    """I dont want random numbers changing if I change logs 
    so wil do a hash over the values to be used. 

    >>> mk_revision_number('alice', '20180101 12:00', 'foobar')
    '995c34712e028c1d7a586f856390a47cab1dc485'

    """
    #just get a deterministic string, convert to bytes before handing to hashlib
    plaintext = ''.join((name, date, ticket)).encode('utf-8')
    hsh = hashlib.sha1()
    hsh.update(plaintext)
    return hsh.hexdigest()

def fakedatetodate(fakedate):
    """ 
    >>> dt = '20180101 15:01'
    >>> fakedatetodate(dt)
    datetime.datetime(2018, 1, 1, 15, 1)
    
    """
    dtformat = "%Y%m%d %H:%M"
    dateobj = datetime.datetime.strptime(fakedate, dtformat)
    return dateobj

def logfaker():
    
    template = '''commit {sha1}
Author: {username}
Date:   {formatteddate}

    {msg} Add the flibble meter

    Flibble meters are useful things

'''
    dateformat = "%a %m %d %H:%M:%S %Y +0000"
    for data in fakelog['REPO1']:
        user, dt, msg = data
        print(template.format(sha1=mk_revision_number(user, dt, msg),
                              username=user,
                              formatteddate=fakedatetodate(dt).strftime(dateformat),
                              msg=msg))
    
if __name__ == '__main__':
    #
    logfaker()
    
    #import doctest
    #doctest.testmod()
