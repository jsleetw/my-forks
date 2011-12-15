from fabric.api import run, env
from fabric.context_managers import settings, cd
from fabric.contrib import console
from fabric.colors import green, red, blue, cyan, magenta, yellow
from github2.client import Github

code_dir = '~/test_my_forks/'
env.hosts = ["localhost"]


def get_my_fork():
    user_name = raw_input(green("enter your github user name : "))
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
            else:
                my_forks[project_pure_name]["branch"] = "master"

    print green("Will sync your forks as below:")
    for element in my_forks.keys():
        print "%s : from %s branch:%s to %s" % (blue(str(element)),
                                                cyan(str(my_forks[element]["upstream"])),
                                                magenta(str(my_forks[element]["branch"])),
                                                yellow(str(my_forks[element]["origin"])))
    if console.confirm(red("Do you want to continue?"), default=True):
        return my_forks
    else:
        return False


def update():
    my_forks = get_my_fork()
    if my_forks:
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
