from fabric.api import run, env
from fabric.context_managers import settings, cd
from github2.client import Github

code_dir = '~/test_my_forks/'
env.hosts = ["localhost"]


def get_my_fork():
    user_name = raw_input("enter your user name : ")
    github = Github()
    repos = github.repos.list(user_name)
    my_forks = {}
    for element in repos:
        project = str(element).replace("<Repository:", "").replace(">", "").strip()
        repo = github.repos.show(project)
        project_pure_name = project.replace(user_name, "").replace("/", "").strip()
        if repo.fork:
            my_forks[project_pure_name] = {}
            my_forks[project_pure_name]["origin"] = "git@github.com:%s.git" % project
            my_forks[project_pure_name]["upstream"] = "git@github.com:%s.git" % str(repo.parent)
            if repo.master_branch:
                my_forks[project_pure_name]["branch"] = str(repo.master_branch)

    return my_forks


def update():
    my_forks = get_my_fork()
    for element in my_forks.keys():
        project = element
        origin = my_forks[element]["origin"]
        upstream = my_forks[element]["upstream"]
        if "branch" in my_forks[element]:
            branch = my_forks[element]["branch"]
        else:
            branch = "master"
        with settings(warn_only=True):
            if run("test -d %s%s" % (code_dir, project)).failed:
                run("git clone %s %s%s" % (origin, code_dir, project))
        with cd("%s%s" % (code_dir, project)):
            with settings(warn_only=True):
                run("git remote add upstream %s" % upstream)
            run("git fetch upstream")
            run("git checkout %s" % branch)
            run("git rebase upstream/%s" % branch)
            run("git push origin %s" % branch)
