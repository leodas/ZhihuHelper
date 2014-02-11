#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zhihu
from session import ZhihuSession

if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser()
    parser.add_option('-u', '--user', dest='username')
    parser.add_option('-p', '--password', dest='passwd')
    parser.add_option('-s', '--dest', dest='dest_user')
    parser.add_option('-b', '--backup', action='store_true', dest='backup')
    parser.add_option('-d', '--delete', action='store_true', dest='delete')
    options, args = parser.parse_args()

    # TEST BEGIN ======================================================>
    session = ZhihuSession()
    if not session.login(options.username, options.passwd):
            print 'Login Failed, exit'
            exit(1)

    if options.dest_user:
        answers, answers_size = session.getAnswers(options.dest_user)
    else:
        answers, answers_size = session.getAnswers()

    print '%d answers found' % answers_size

    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if options.backup:
        f = open(session.me.link_name + '-answers', 'w+')
        for answer in answers:
            f.write(u'\n==================================================================\n')
            f.write(answer.question.title + u'\n')
            f.write(answer.question.url + u'\n')
            f.write(u'\n')
            f.write(answer.text + u'\n')
        f.close()
        print '%d answers has saved in %s' % (answers_size, session.me.link_name + '-answers')

    if options.delete and not options.dest_user:
        for answer in answers:
            session.delAnswer(answer)
        print '%d answers has removed'
