from github import Github
from opsbox.settings import GITHUB_USERNAME,GITHUB_PASSWORD = 'a05370385a@3'



# g = Github(GITHUB_USERNAME,GITHUB_PASSWORD)
# repo = g.get_repo("duskxy/gosec")
# # print(list(repo.get_tags()))
#
# for i in repo.get_tags():
#     print(i.name)

class GithubApi:
    def __init__(self):
        self.proj = "duskxy"
        self.username = GITHUB_USERNAME
        self.password = GITHUB_PASSWORD
        self.g = Github(self.username,self.password)
    def get_tag(self,repoorg):
        taglist = []
        repo = self.g.get_repo(self.proj + "/" + repoorg)
        for i,j in enumerate(repo.get_tags()):
            taglist.append({
                "label": i,
                "value": j.name})
        return taglist

if __name__ == "__main__":
    gitserver = GithubApi()
    gitserver.get_tag("gosec")