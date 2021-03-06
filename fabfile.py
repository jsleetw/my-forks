from fabric.api import run, env, prompt, task
from fabric.context_managers import settings, cd
from fabric.contrib import console
from fabric.utils import abort
import fabric.colors as color
import github2.client
import os

code_dir = '~/test_my_forks/'
env.hosts = ["localhost"]

__all__ = ['update']


def _get_user_name():
    """auto save user_name as .username"""
    user_name = None
    if os.path.isfile("./.username"):
        f = open('./.username', 'r')
        user_name = str(f.readline()).strip()
    user_name = prompt(color.green("Enter your github user name : "), default=user_name)
    f = open('./.username', 'w')
    f.write(user_name)
    f.close()
    return user_name


def _get_github(user_name):
    """load api_token if file exits"""
    api_token = None
    if os.path.isfile("./.api_token"):
        f = open('./.api_token', 'r')
        api_token = str(f.readline()).strip()
        f.close()
    if api_token:
        print "find out .api_token .... load private repos........"
        github = github2.client.Github(username=user_name, api_token=api_token)
    else:
        github = github2.client.Github()
    return github


def _get_my_forks():
    user_name = _get_user_name()
    github = _get_github(user_name)
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
            if repo.private:
                my_forks[project_pure_name]["private"] = True
    print color.green("Will sync your forks as below:")
    for element in my_forks.keys():
        if "private" in my_forks[element]:
            repo_str = color.red(str(element))
        else:
            repo_str = color.blue(str(element))
        print "%s : from %s branch:%s to %s" % (repo_str,
                                                color.cyan(str(my_forks[element]["upstream"])),
                                                color.magenta(str(my_forks[element]["branch"])),
                                                color.yellow(str(my_forks[element]["origin"])))
    if not console.confirm(color.red("Do you want to continue?"), default=True):
        abort("canceled by user")
    return my_forks


@task(default=True)
def update():
    my_forks = _get_my_forks()
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
