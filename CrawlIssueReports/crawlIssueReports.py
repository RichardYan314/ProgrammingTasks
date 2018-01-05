from urllib.request import urlopen
from http.client import HTTPException
from urllib.error import URLError
from bs4 import BeautifulSoup as bs
from html2text import html2text
import codecs
import sys
import time
import csv

# convert datetime string to epoch seconds
toEpoch = lambda str: '' if str is None else int(time.mktime(time.strptime(str, '%Y-%m-%dT%H:%M:%S%z')))
# util function to unescape special characters
# used during debuging so strings can fit to one line
# unescape = lambda str: (codecs.getdecoder("unicode_escape")(str))[0]
unescape = lambda str: repr(str)
# get text from a DOM element and strip blanks from both end
# deals with the case when the element is `None`
stripText = lambda DomElem : 'None' if DomElem is None else ' '.join(DomElem.get_text().strip().split())


if __name__ == "__main__":
    # example
    issueUrl1 = "https://issues.apache.org/jira/browse/CAMEL-10597"
    # affects none version
    issueUrl2 = "https://issues.apache.org/jira/browse/CAMEL-10596"
    # affects multiple version
    issueUrl3 = "https://issues.apache.org/jira/browse/CAMEL-5381"
    # has labels
    # has environment
    # unassigned
    issueUrl4 = "https://issues.apache.org/jira/browse/CAMEL-7651"
    # unresolved @2001/01/04 22:40 EST
    issueUrl5 = "https://issues.apache.org/jira/browse/CAMEL-12000"

    issueUrl = issueUrl1

    try:
        with urlopen(issueUrl) as f:
            charset = f.headers.get_content_charset('default')
            doc = f.read().decode(charset)
            # print(doc)

            soup = bs(doc, 'html.parser')

            if soup.find('div', 'aui-page-header-main').h1.text == "Issue does not exist":
                sys.stderr.write("Issue does not exist")



            # summary
            summary = soup.find(id='summary-val').get_text()



            # details
            # type = stripText(soup.find(id='type-val'))
            # priority = stripText(soup.find(id='priority-val'))
            # affectsVersions = tuple(stripText(span)
            #                         for versions_field in tuple((soup.find(id='versions-field'),))
            #                             if versions_field is not None
            #                         for span in versions_field.find_all('span'))
            # affectsVersions = 'None' if len(affectsVersions) == 0 else ', '.join(affectsVersions)
            # components = stripText(soup.find(id='components-field'))
            # labels = stripText(soup.find('div', {'class': 'labels-wrap value'}))
            # patchInfo = stripText(soup.find(id='customfield_12310041-field'))
            # estComplexity = stripText(soup.find(id='customfield_12310060-val'))
            # status = stripText(soup.find(id='status-val').span)
            # resolution = stripText(soup.find(id='resolution-val'))
            # fixVersion = tuple(stripText(a) for a in soup.find(id='fixVersions-field').find_all('a'))
            # fixVersion = ", ".join(fixVersion)
            #
            # print(type)
            # print(priority)
            # print(affectsVersions)
            # print(components)
            # print(labels)
            # print(patchInfo)
            # print(estComplexity)
            # print(status)
            # print(resolution)
            # print(fixVersion)

            # this is much more robust!
            details = soup.find(id='issuedetails')
            details = [(stripText(item.find('strong', {'class': 'name'})).rstrip(':'),
                        stripText(item.find(True, {'class': 'value'})))
                       for module in (soup.find(id='issuedetails'), soup.find(id='customfieldmodule'))
                       for item in module.find_all('li', {'class': 'item'})]

            print(details)



            # people
            assignee = soup.find(id='assignee-val').get_text().strip()
            reporter = soup.find(id='reporter-val').get_text().strip()

            print(assignee)
            print(reporter)



            # dates
            created = soup.find(id='create-date').time['datetime']
            updated = soup.find(id='updated-date').time['datetime']
            resolved = soup.find(id='resolved-date')
            if resolved:
                resolved = resolved.time['datetime']

            print(created)
            print(updated)
            print(resolved)
            print(toEpoch(created))

            
            
            # description
            description = soup.find(id='description-val')
            description = html2text(str(description))
            description = unescape(description)

            print(description)



            # comments
            comments = soup.find(id='issue_actions_container')

            comments = [str(cmt.find('a', {'class': 'user-hover user-avatar'}).get_text().strip()) + ":" +
                        str(toEpoch(str(cmt.find('span', {'class': 'date user-tz'}).time['datetime']))) + ":" +
                        str(str(cmt.find('span', {'class': 'date user-tz'}).time['datetime'])) + ":``" +
                        str(html2text(str(cmt.find('div', {'class': 'action-body flooded'}))).strip()) + "´´"
                        for cmt in comments.find_all('div', {'class': 'twixi-wrap verbose actionContainer'})]

            comments = [unescape(cmt) for cmt in comments]

            if comments:
                print((comments[0]))

            comments = '\\n'.join(comments)



            # write to csv
            with open('report.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # writer.writerow(('Type', 'Priority', 'Affects Version/s',
                #                  'Component/s', 'Labels', 'Patch Info',
                #                  'Estimated Complexity', 'Status', 'Resolution',
                #                  'Fix Version/s',
                #                  'Assignee', 'Reporter',
                #                  'Created', 'Created_Epoch',
                #                  'Updated', 'Updated_Epoch',
                #                  'Resolved', 'Resolved_Epoch',
                #                  'Description', 'Comments'))
                # writer.writerow((type, priority, affectsVersions,
                #                  components, labels, patchInfo,
                #                  estComplexity, status, resolution,
                #                  fixVersion,
                #                  assignee, reporter,
                #                  created, toEpoch(created),
                #                  updated, toEpoch(updated),
                #                  resolved, toEpoch(resolved),
                #                  description, comments))

                heading, content = zip(*details)
                heading += ('Assignee', 'Reporter',
                            'Created', 'Created_Epoch',
                            'Updated', 'Updated_Epoch',
                            'Resolved', 'Resolved_Epoch',
                            'Description', 'Comments')
                content += (assignee, reporter,
                            created, toEpoch(created),
                            updated, toEpoch(updated),
                            resolved, toEpoch(resolved),
                            description, comments)
                writer.writerow(heading)
                writer.writerow(content)

    except HTTPException as e:
        print(e)
    except URLError as e:
        print(e)
