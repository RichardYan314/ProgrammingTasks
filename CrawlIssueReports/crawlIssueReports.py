from urllib.request import urlopen
from http.client import HTTPException
from urllib.error import URLError
from bs4 import BeautifulSoup as bs
from html2text import html2text
import codecs
import sys
import time
import csv


toEpoch = lambda str: int(time.mktime(time.strptime(str, '%Y-%m-%dT%H:%M:%S%z')))
unescape = lambda str: (codecs.getdecoder("unicode_escape")(str))[0]

if __name__ == "__main__":
    notExists = "https://issues.apache.org/jira/browse/CAMEL-999999999999"

    issueUrl = "https://issues.apache.org/jira/browse/CAMEL-10597"
    #issueUrl = notExists

    try:
        with urlopen(issueUrl) as f:
            charset = f.headers.get_content_charset('default')
            doc = f.read().decode(charset)
            # print(doc)

            soup = bs(doc, 'html.parser')

            if soup.find('div', 'aui-page-header-main').h1.text == "Issue does not exist":
                sys.stderr.write("Issue does not exist")

            summary = soup.find(id='summary-val').get_text()



            # details
            type = soup.find(id='type-val').get_text().strip()
            priority = soup.find(id='priority-val').get_text().strip()
            affectsVersions = soup.find(id='versions-field').get_text().strip()
            components = soup.find(id='components-field').get_text().strip()
            labels = soup.find(id='labels-13028113-value').get_text().strip()
            patchInfo = soup.find(id='customfield_12310041-field').span.get_text().strip()
            estComplexity = soup.find(id='customfield_12310060-val').get_text().strip()
            status = soup.find(id='status-val').span.get_text().strip()
            resolution = soup.find(id='resolution-val').get_text().strip()
            fixVersion = tuple(a.get_text().strip() for a in soup.find(id='fixVersions-field').find_all('a'))
            fixVersion = ", ".join(fixVersion)

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



            # people
            assignee = soup.find(id='assignee-val').span.get_text().strip()
            reporter = soup.find(id='reporter-val').span.get_text().strip()

            # print(assignee)
            # print(reporter)



            # dates
            created = soup.find(id='create-date').time['datetime']
            updated = soup.find(id='updated-date').time['datetime']
            resolved = soup.find(id='resolved-date').time['datetime']

            # print(created)
            # print(updated)
            # print(resolved)
            # print(toEpoch(created))

            description = soup.find(id='description-val')
            description = html2text(str(description))
            # description = unescape(description)

            #print(description)



            # comments
            comments = soup.find(id='issue_actions_container')

            comments = [str(cmt.find('a', {'class': 'user-hover user-avatar'}).get_text().strip()) + ":" +
                        str(toEpoch(str(cmt.find('span', {'class': 'date user-tz'}).time['datetime']))) + ":" +
                        str(str(cmt.find('span', {'class': 'date user-tz'}).time['datetime'])) + ":``" +
                        str(html2text(str(cmt.find('div', {'class': 'action-body flooded'}))).strip()) + "´´"
                        for cmt in comments.find_all('div', {'class': 'twixi-wrap verbose actionContainer'})]

            # comments = [unescape(cmt) for cmt in comments]

            # print((comments[0]))

            comments = '\\n'.join(comments)



            # write to csv
            with open('report.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(('Type', 'Priority', 'Affects Version/s',
                                 'Component/s', 'Labels', 'Patch Info',
                                 'Estimated Complexity', 'Status', 'Resolution',
                                 'Fix Version/s',
                                 'Assignee', 'Reporter',
                                 'Created', 'Created_Epoch',
                                 'Updated', 'Updated_Epoch',
                                 'Resolved', 'Resolved_Epoch',
                                 'Description', 'Comments'))
                writer.writerow((type, priority, affectsVersions,
                                 components, labels, patchInfo,
                                 estComplexity, status, resolution,
                                 fixVersion,
                                 assignee, reporter,
                                 created, toEpoch(created),
                                 updated, toEpoch(updated),
                                 resolved, toEpoch(resolved),
                                 description, comments))

    except HTTPException as e:
        print(e)
    except URLError as e:
        print(e)
