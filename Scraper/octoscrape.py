import re
import base64
import os
import autopep8
import time
from dotenv import load_dotenv
from github import Github

load_dotenv()


class Octoscrape:
    def __init__(self, page=0):
        self.g = Github(os.environ['GITHUB_TOKEN'], retry=5)
        self.page = page

    def search_repos(self):
        return self.g.search_repositories(
            query='keras stars:>=1000 fork:true language:python').get_page(self.page)

    def get_contents(self, repo, file_extension):
        try:
            contents = repo.get_contents("")

            f = open("data/python.txt", "a+")
            f.write('<s>\n')
            while len(contents) > 1:
                file_content = contents.pop(0)

                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    if file_content.path.endswith(file_extension):
                        decoded_content = base64.b64decode(
                            file_content.content).decode('utf-8')
                        decoded_content = self._clean_code(decoded_content)
                        print("Code size: ", len(decoded_content))
                        decoded_content += "<eos>\n"
                        if len(decoded_content) > 300:
                            f.write(decoded_content)
            f.close()
        except:
            time.sleep(1)
            pass

    def _clean_code(self, code):
        code = re.sub(r'(?m)^ *#.*\n?', '', code)
        return autopep8.fix_code(code, options={'ignore': ['E501'], 'aggressive': 2})

    def next_page(self):
        self.page += 1
